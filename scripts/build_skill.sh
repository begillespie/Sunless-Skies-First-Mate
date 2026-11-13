#!/usr/bin/env bash
# scripts/build_skill.sh
set -euo pipefail

SKILL_NAME="sunless-skies-first-mate"
DIST_DIR="dist"
BUILD_DIR="${DIST_DIR}/${SKILL_NAME}"
REF_DIR="${BUILD_DIR}/references"
ZIP_FILE="${DIST_DIR}/${SKILL_NAME}.zip"
SCHEMA_FILE="data/data_package.json"
MODE="${1:-full}"

PYTHON_BIN="${PYTHON_BIN:-.venv/bin/python}"
FRICTIONLESS_BIN="${FRICTIONLESS_BIN:-.venv/bin/frictionless}"

if [[ ! -x "$PYTHON_BIN" ]]; then
    PYTHON_BIN="$(command -v python3)"
fi

echo -e "==> [1/5] Checking required source files..."
REQUIRED_FILES=(
    "src/SKILL.md"
    "src/Sunless_Skies.md"
    "src/logbook.md"
    "${SCHEMA_FILE}"
)
for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo -e -e "\033[1;31mERROR\033[0m: Missing required file: $file" >&2
        exit 1
    fi
done

echo -e -e "==> [2/5] Validating JSON syntax and Ref_Compatibility_Contract.csv synchronization..."
"$PYTHON_BIN" - << 'EOF'
import csv, json, re, sys
from pathlib import Path

def semver(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.strip().split("."))

def extract_md_meta(path: str) -> tuple[str, str]:
    text = Path(path).read_text(encoding="utf-8")
    sub = re.search(r"@subsystem:\s*([a-z0-9_]+)", text)
    ver = re.search(r"@version:\s*([0-9]+\.[0-9]+\.[0-9]+)", text)
    if not sub or not ver:
        sys.exit(f"\033[1;31mERROR\033[0m: {path} is missing '@subsystem:' or '@version:' header tags.")
    return sub.group(1), ver.group(1)

# 1. Load authoritative contract table
contract_path = Path("data/tables/Ref_Compatibility_Contract.csv")
with contract_path.open(encoding="utf-8") as f:
    contracts = {row["target_subsystem"]: row for row in csv.DictReader(f)}

# 2. Verify current_version >= minimum_version across all contract rows
for sub, row in contracts.items():
    cur, min_v = row["current_version"], row["minimum_version"]
    if semver(cur) < semver(min_v):
        sys.exit(f"\033[1;31mERROR\033[0m: Contract violation for '{sub}': current_version ({cur}) < minimum_version ({min_v})")

# 3. Map project files to their declared (subsystem, version)
pkg = json.loads(Path("data/data_package.json").read_text(encoding="utf-8"))
artifacts = {
    "data/data_package.json": ("data_package", pkg["version"]),
    "src/SKILL.md":           extract_md_meta("src/SKILL.md"),
    "src/Sunless_Skies.md":   extract_md_meta("src/Sunless_Skies.md"),
    "src/logbook.md":         extract_md_meta("src/logbook.md"),
}

# 4. Assert each artifact matches Ref_Compatibility_Contract.csv
for filepath, (sub, file_ver) in artifacts.items():
    if sub not in contracts:
        sys.exit(f"\033[1;31mERROR\033[0m: Subsystem '{sub}' (in {filepath}) is missing from {contract_path}")
    expected_ver = contracts[sub]["current_version"]
    if file_ver != expected_ver:
        sys.exit(
            f"\033[1;31mERROR\033[0m: Version drift in {filepath} ({sub}): "
            f"file declares '{file_ver}', but Ref_Compatibility_Contract.csv expects '{expected_ver}'"
        )
    print(f"      \033[1;32m[OK]\033[0m {sub:<18} v{file_ver} (min >= v{contracts[sub]['minimum_version']}) -> {filepath}")
EOF

echo -e -e "==> [3/5] Validating data/tables/*.csv against ${SCHEMA_FILE}..."
if [[ ! -x "$FRICTIONLESS_BIN" ]]; then
    if command -v frictionless >/dev/null 2>&1; then
        FRICTIONLESS_BIN="$(command -v frictionless)"
    else
        echo -e -e "\033[1;31mERROR\033[0m: frictionless binary not found at '${FRICTIONLESS_BIN}' or in PATH. Run 'make venv' first." >&2
        exit 1
    fi
fi

"$FRICTIONLESS_BIN" validate "${SCHEMA_FILE}"

if [[ "$MODE" == "--validate-only" ]]; then
    echo -e -e "\033[1;32mSUCCESS\033[0m: Validation passed."
    exit 0
fi

echo -e "==> [4/5] Staging skill directory in ${BUILD_DIR}..."
rm -rf "${DIST_DIR}"
mkdir -p "${REF_DIR}"

tr -d '\r' < src/SKILL.md       > "${BUILD_DIR}/SKILL.md"
tr -d '\r' < src/Sunless_Skies.md > "${REF_DIR}/Sunless_Skies.md"
tr -d '\r' < src/logbook.md     > "${REF_DIR}/logbook.md"
tr -d '\r' < "${SCHEMA_FILE}"   > "${REF_DIR}/data_package.json"

echo -e "==> [5/5] Packaging ${ZIP_FILE}..."
(
    cd "${DIST_DIR}"
    "$OLDPWD/$PYTHON_BIN" -m zipfile -c "${SKILL_NAME}.zip" "${SKILL_NAME}/"
    sha256sum "${SKILL_NAME}.zip" > "${SKILL_NAME}.zip.sha256"
)

echo -e -e "\033[1;32mSUCCESS\033[0m: Built ${ZIP_FILE} ($(du -h "${ZIP_FILE}" | cut -f1))"
