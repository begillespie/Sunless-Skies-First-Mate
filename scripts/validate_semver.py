#!/usr/bin/env python3
"""
scripts/validate_semver.py
Validates SemVer syntax and compatibility contracts by extracting
@subsystem and @version tags across source files and comparing them
against data/tables/ref_compatibility_contract.csv.
"""
import csv
import json
import re
import sys
from pathlib import Path

GREEN = "\033[1;32m"
RED = "\033[1;31m"
NC = "\033[0m"

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
SUBSYSTEM_RE = re.compile(r"^\s*(?:<!--\s*)?@subsystem:\s*([a-z0-9_]+)", re.MULTILINE)
VERSION_RE = re.compile(r"^\s*(?:<!--\s*)?@version:\s*([0-9]+\.[0-9]+\.[0-9]+)", re.MULTILINE)

# External subsystems tracked in ref_compatibility_contract.csv that do not have local source files
EXTERNAL_SUBSYSTEMS = {"sunless_skies_game"}


def parse_semver(version_str: str, context: str, errors: list[str]) -> tuple[int, int, int] | None:
    match = SEMVER_RE.match(version_str.strip())
    if not match:
        errors.append(f"Invalid SemVer '{version_str}' in {context}")
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def extract_declarations(file_path: Path, rel_name: str, errors: list[str]) -> list[tuple[str, str]]:
    """Extracts (subsystem, version) pairs from a file."""
    text = file_path.read_text(encoding="utf-8")

    # JSON files: check for @subsystem/@version tags first, or fallback to top-level/resource version
    if file_path.suffix == ".json":
        subs = SUBSYSTEM_RE.findall(text)
        vers = VERSION_RE.findall(text)

        if subs and len(subs) == len(vers):
            return list(zip(subs, vers))

        pkg = json.loads(text)
        decls: list[tuple[str, str]] = []
        if "name" in pkg and "version" in pkg:
            decls.append((pkg.get("subsystem", pkg["name"]), str(pkg["version"])))
        for res in pkg.get("resources", []):
            if "name" in res and "version" in res:
                parse_semver(str(res["version"]), f"{rel_name}[{res['name']}.version]", errors)
        return decls

    # Markdown / text files: extract @subsystem and @version lines in order
    subs = SUBSYSTEM_RE.findall(text)
    vers = VERSION_RE.findall(text)

    if not subs and not vers:
        errors.append(f"Missing @subsystem / @version tags in {rel_name}")
        return []

    if len(subs) != len(vers):
        errors.append(
            f"Mismatched tag count in {rel_name}: found {len(subs)} @subsystem tag(s) "
            f"and {len(vers)} @version tag(s)"
        )
        return []

    return list(zip(subs, vers))


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    contract_path = repo_root / "data" / "tables" / "ref_compatibility_contract.csv"

    target_files = [
        repo_root / "src" / "SKILL.md",
        repo_root / "src" / "Sunless_Skies.md",
        repo_root / "src" / "logbook.md",
        repo_root / "data" / "data_package.json",
    ]

    errors: list[str] = []

    if not contract_path.exists():
        print(
            f"  {RED}✗ [SemVer] Missing contract table: {contract_path.relative_to(repo_root)}{NC}",
            file=sys.stderr,
        )
        return 1

    # 1. Load & validate ref_compatibility_contract.csv keyed by target_subsystem
    contracts: dict[str, dict[str, str]] = {}
    with contract_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            subsystem = row["target_subsystem"].strip()
            cur_v = row["current_version"].strip()
            min_v = row["minimum_version"].strip()

            cur_t = parse_semver(cur_v, f"ref_compatibility_contract[{subsystem}].current_version", errors)
            min_t = parse_semver(min_v, f"ref_compatibility_contract[{subsystem}].minimum_version", errors)

            if cur_t and min_t and cur_t < min_t:
                errors.append(
                    f"  Contract table violation for '{subsystem}': "
                    f"  current_version ({cur_v}) < minimum_version ({min_v})"
                )
            contracts[subsystem] = row

    # 2. Loop over files, extract @subsystem and @version, and compare to contract rows
    verified_subsystems: dict[str, str] = {}

    for file_path in target_files:
        if not file_path.exists():
            continue
        rel_name = str(file_path.relative_to(repo_root))
        declarations = extract_declarations(file_path, rel_name, errors)

        for subsystem, declared_ver in declarations:
            decl_t = parse_semver(declared_ver, f"{rel_name} (@subsystem: {subsystem})", errors)

            # Allow data_package.json fallback to match a contract row if named differently
            if subsystem not in contracts and file_path.name == "data_package.json":
                for candidate in ("data_package", "data_package.json", "schema", "datastore"):
                    if candidate in contracts:
                        subsystem = candidate
                        break

            if subsystem not in contracts:
                errors.append(
                    f"{rel_name} declares unknown @subsystem '{subsystem}' "
                    f"(not found in ref_compatibility_contract.csv)"
                )
                continue

            contract_row = contracts[subsystem]
            expected_cur = contract_row["current_version"].strip()
            expected_min = contract_row["minimum_version"].strip()
            min_t = SEMVER_RE.match(expected_min)

            if declared_ver != expected_cur:
                errors.append(
                    f"Version mismatch for '{subsystem}' in {rel_name}: "
                    f"declared @version ({declared_ver}) != contract current_version ({expected_cur})"
                )

            if decl_t and min_t:
                min_tuple = (int(min_t.group(1)), int(min_t.group(2)), int(min_t.group(3)))
                if decl_t < min_tuple:
                    errors.append(
                        f"Incompatible version for '{subsystem}' in {rel_name}: "
                        f"declared @version ({declared_ver}) < contract minimum_version ({expected_min})"
                    )

            verified_subsystems[subsystem] = declared_ver

    # 3. Verify every internal row in ref_compatibility_contract.csv was accounted for
    for subsystem in contracts:
        if subsystem in EXTERNAL_SUBSYSTEMS:
            continue
        if subsystem not in verified_subsystems:
            errors.append(
                f"Subsystem '{subsystem}' in ref_compatibility_contract.csv was not declared in any source file"
            )

    if errors:
        for err in errors:
            print(f"  {RED}✗ [SemVer] {err}{NC}", file=sys.stderr)
        return 1

    # 4. Build concise status output with target game build remark
    summary = "\n".join(f"{sub} v{ver}" for sub, ver in verified_subsystems.items())
    game_remark = ""
    if "sunless_skies_game" in contracts:
        game_row = contracts["sunless_skies_game"]
        game_cur = game_row["current_version"].strip()
        game_min = game_row["minimum_version"].strip()
        if game_cur == game_min:
            game_remark = f"Target Game Build: Sunless Skies v{game_cur}"
        else:
            game_remark = f"Target Game Build: {GREEN}Sunless Skies v{game_cur} (min v{game_min}){NC}"

    print(f"  {GREEN}✓ [SemVer]{NC} Verified {len(verified_subsystems)} subsystem contract(s)")
    for sub, ver in verified_subsystems.items():
        print(f"    {GREEN}✓{NC} {sub} v{ver}") 
    print(f"  {game_remark}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())