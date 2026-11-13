#!/usr/bin/env bash
set -euo pipefail

GREEN="\033[1;32m"
RED="\033[1;31m"
NC="\033[0m"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Resolve binaries (honor Makefile env vars, fallback to .venv if present, then system PATH)
if [[ -z "${PYTHON_BIN:-}" ]]; then
    if [[ -x ".venv/bin/python3" ]]; then
        PYTHON_BIN=".venv/bin/python3"
    else
        PYTHON_BIN="python3"
    fi
fi

if [[ -z "${FRICTIONLESS_BIN:-}" ]]; then
    if [[ -x ".venv/bin/frictionless" ]]; then
        FRICTIONLESS_BIN=".venv/bin/frictionless"
    else
        FRICTIONLESS_BIN="frictionless"
    fi
fi

VALIDATE_ONLY=false
if [[ "${1:-}" == "--validate-only" ]]; then
    VALIDATE_ONLY=true
fi

SKILL_NAME="sunless-skies-first-mate"
BUILD_DIR="dist/${SKILL_NAME}"
ARCHIVE_PATH="dist/${SKILL_NAME}.skill"

echo "[1/5] Validating source Frictionless Data Package..."
if "$FRICTIONLESS_BIN" validate data/data_package.json > /dev/null; then
    echo -e "  ${GREEN}✓ [Schema]${NC} Source data/data_package.json and CSV tables are valid."
else
    echo -e "  ${RED}✗ [Schema]${NC} Validation failed on source data/data_package.json." >&2
    "$FRICTIONLESS_BIN" validate data/data_package.json || true
    exit 1
fi

echo "[2/5] Validating SemVer & Compatibility Contracts..."
"$PYTHON_BIN" scripts/validate_semver.py

if [[ "$VALIDATE_ONLY" == true ]]; then
    echo -e "  ${GREEN}✓ [Validate]${NC} Validation passed. Exiting due to --validate-only flag."
    exit 0
fi

echo "[3/5] Assembling skill bundle & compiling inline Data Package..."
rm -rf "$BUILD_DIR" "$ARCHIVE_PATH"
mkdir -p "${BUILD_DIR}/references"

cp src/SKILL.md "${BUILD_DIR}/SKILL.md"
cp src/Sunless_Skies.md "${BUILD_DIR}/references/Sunless_Skies.md"
cp src/logbook.md "${BUILD_DIR}/references/logbook.md"

"$PYTHON_BIN" scripts/compile_datapackage.py \
    "data/data_package.json" \
    "${BUILD_DIR}/references/data_package.json"

echo "[4/5] Verifying compiled skill bundle integrity..."
for req_file in \
    "${BUILD_DIR}/SKILL.md" \
    "${BUILD_DIR}/references/Sunless_Skies.md" \
    "${BUILD_DIR}/references/logbook.md" \
    "${BUILD_DIR}/references/data_package.json"; do
    if [[ ! -s "$req_file" ]]; then
        echo -e "  ${RED}✗ [Verify]${NC} Missing or empty required build artifact: ${req_file}" >&2
        exit 1
    fi
done
echo -e "  ${GREEN}✓ [Verify]${NC} All skill bundle files present and non-empty."

echo "[5/5] Packaging distributable skill archive..."
cd dist 
"$OLDPWD/$PYTHON_BIN" -m zipfile -c "${SKILL_NAME}.zip" "${SKILL_NAME}"
sha256sum "${SKILL_NAME}.zip" > "${SKILL_NAME}.zip.sha256"

echo -e "  ${GREEN}✓ [Package]${NC} Built ${SKILL_NAME}.zip successfully."
echo -e "  ${GREEN}✓ [Package]${NC} SHA256 Checksum: $(cat ${SKILL_NAME}.zip.sha256)"