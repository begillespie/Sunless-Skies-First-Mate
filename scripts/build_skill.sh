#!/usr/bin/env bash
set -euo pipefail

GREEN="\033[1;32m"
NC="\033[0m"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Resolve Python binary
if [[ -z "${PYTHON_BIN:-}" ]]; then
    if [[ -x ".venv/bin/python3" ]]; then
        PYTHON_BIN="${REPO_ROOT}/.venv/bin/python3"
    else
        PYTHON_BIN="python3"
    fi
elif [[ "$PYTHON_BIN" != /* ]]; then
    PYTHON_BIN="${REPO_ROOT}/${PYTHON_BIN}"
fi

SKILL_NAME="sunless-skies-first-mate"
BUILD_DIR="dist/${SKILL_NAME}"
ARCHIVE_NAME="${SKILL_NAME}.zip"
ARCHIVE_PATH="dist/${ARCHIVE_NAME}"
HASH_PATH="${ARCHIVE_PATH}.sha256"

echo "  [1/3] Assembling skill bundle & compiling inline Data Package..."
rm -rf "$BUILD_DIR" "$ARCHIVE_PATH" "$HASH_PATH"
mkdir -p "${BUILD_DIR}/references"
mkdir -p "${BUILD_DIR}/tools"

cp src/SKILL.md "${BUILD_DIR}/SKILL.md"
cp src/Sunless_Skies.md "${BUILD_DIR}/references/Sunless_Skies.md"
cp src/logbook.md "${BUILD_DIR}/references/logbook.md"

# Copy decoupled Python tools into the deployable skill package
if [[ -d "src/tools" ]]; then
    cp src/tools/*.py "${BUILD_DIR}/tools/"
fi

"$PYTHON_BIN" scripts/compile_datapackage.py \
    "data/data_package.json" \
    "${BUILD_DIR}/references/data_package.json"

echo "  [2/3] Verifying compiled skill bundle integrity..."
for req_file in \
    "${BUILD_DIR}/SKILL.md" \
    "${BUILD_DIR}/references/Sunless_Skies.md" \
    "${BUILD_DIR}/references/logbook.md" \
    "${BUILD_DIR}/references/data_package.json"; do
    if [[ ! -s "$req_file" ]]; then
        echo "Error: Missing or empty required build artifact: ${req_file}" >&2
        exit 1
    fi
    echo -e "    ${GREEN}✓ [Verify]${NC} Found required build artifact: ${req_file}"
done
echo -e "    ${GREEN}✓ [Compile]${NC} All required build artifacts are present and non-empty."

echo "  [3/3] Packaging distributable zip archive & SHA-256 digest..."
cd dist 

"$PYTHON_BIN" -m zipfile -c "${SKILL_NAME}.zip" "${SKILL_NAME}"
sha256sum "${SKILL_NAME}.zip" > "${SKILL_NAME}.zip.sha256"

echo -e "    ${GREEN}✓ [Package]${NC} Built ${SKILL_NAME}.zip successfully."
echo -e "    ${GREEN}✓ [Package]${NC} SHA256 Checksum: $(cat ${SKILL_NAME}.zip.sha256)"