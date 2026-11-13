#!/usr/bin/env python3
"""
scripts/compile_datapackage.py
Compiles non-inline package resources into inline table resources using
native Frictionless Resource.write(format="inline", datatype="table").
"""
import sys
from pathlib import Path
from frictionless import Package #type: ignore

GREEN = "\033[1;32m"
RED = "\033[1;31m"
NC = "\033[0m"


def compile_datapackage(src_path: Path, dst_path: Path) -> int:
    # 1. Load the data package
    pkg = Package(str(src_path))

    # 2. Build filtered list of non-inline resource names
    resource_names = [res.name for res in pkg.resources if res.format != "inline"]

    # 3. Convert each external resource to inline
    for name in resource_names:
        csv_resource = pkg.get_resource(name)
        inline_resource = csv_resource.write(format="inline", datatype="table")
        inline_resource.name = csv_resource.name
        inline_resource.schema = csv_resource.schema

        pkg.remove_resource(name)
        pkg.add_resource(inline_resource)

    # 4. Validate new data_package
    report = pkg.validate()
    if not report.valid:
        errors = [
            f"  [{task.name}] {err.title}: {err.message}"
            for task in report.tasks
            for err in task.errors
        ]
        raise ValueError("Compiled package failed validation:\n  - " + "\n  - ".join(errors))

    # 5. Write compiled package to new location
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    pkg.to_json(str(dst_path))

    return len(resource_names)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    src_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else repo_root / "data" / "data_package.json"
    dst_path = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) > 2
        else repo_root / "dist" / "sunless-skies-first-mate" / "references" / "data_package.json"
    )

    if not src_path.exists():
        print(f"  {RED}✗ [Compile]{NC} Source data package not found: {src_path}", file=sys.stderr)
        return 1

    try:
        inlined_count = compile_datapackage(src_path, dst_path)
    except Exception as exc:
        print(f"  {RED}✗ [Compile]{NC} {exc}", file=sys.stderr)
        return 1

    rel_dst = dst_path.relative_to(repo_root) if dst_path.is_relative_to(repo_root) else dst_path
    print(f"  {GREEN}✓ [Compile]{NC} Inlined & validated {inlined_count} resources into {rel_dst}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())