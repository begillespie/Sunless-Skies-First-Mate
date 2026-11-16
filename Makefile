SHELL := /usr/bin/env bash
SKILL_NAME := sunless-skies-first-mate
DIST_DIR   := dist
VENV_DIR   := .venv

# Stamp files for incremental tracking
VENV_STAMP  := $(VENV_DIR)/.installed
VAL_STAMP   := $(VENV_DIR)/.validated
TEST_STAMP  := $(VENV_DIR)/.tested

# Source files governing incremental rebuilds
SRC_FILES   := $(shell find src data scripts -type f 2>/dev/null)
TEST_FILES  := $(shell find tests -type f 2>/dev/null)

.PHONY: all venv validate test build rebuild clean clean-all

all: build

## 1. Bootstrap Python virtual environment
venv: $(VENV_STAMP)

$(VENV_STAMP): requirements-dev.txt
	@echo "==> Bootstrapping Python virtual environment in $(VENV_DIR)..."
	@python3 -m venv $(VENV_DIR)
	@$(VENV_DIR)/bin/pip install --upgrade --quiet pip
	@echo "==> Installing Python dependencies from requirements-dev.txt..."
	@$(VENV_DIR)/bin/pip install --quiet -r requirements-dev.txt
	@touch $(VENV_STAMP)

## 2. Incremental Schema & SemVer Validation
validate: $(VAL_STAMP)

$(VAL_STAMP): $(VENV_STAMP) $(shell find data scripts -type f)
	@echo "==> [VALIDATE] Validating compatibility contracts..."
	@$(VENV_DIR)/bin/python3 scripts/validate_semver.py
	@echo "==> [VALIDATE] Validating Frictionless data package..."
	@$(VENV_DIR)/bin/frictionless validate data/data_package.json
	@touch $(VAL_STAMP)

## 3. Incremental Tier 2 Unit Tests
test: $(TEST_STAMP)

$(TEST_STAMP): $(VENV_STAMP) $(VAL_STAMP) $(shell find src/tools tests -type f 2>/dev/null)
	@echo "==> [TEST] Running unit test suite..."
	@$(VENV_DIR)/bin/coverage run --source=src -m unittest discover -s tests -v
	@echo "==> [TEST] Test Coverage Report"
	@$(VENV_DIR)/bin/coverage report
	@touch $(TEST_STAMP)

## 4. Incremental Build & Packaging (.zip + .sha256)
build: $(TEST_STAMP) $(DIST_DIR)/$(SKILL_NAME).zip

$(DIST_DIR)/$(SKILL_NAME).zip: $(VAL_STAMP) $(TEST_STAMP) $(SRC_FILES)
	@echo "==> [BUILD] Assembling and packaging skill bundle..."
	@PYTHON_BIN="$(VENV_DIR)/bin/python3" ./scripts/build_skill.sh

## Force a full rebuild by clearing all stamps
rebuild: clean all

## Remove build artifacts, test caches, and Python bytecode
clean:
	rm -rf $(DIST_DIR) $(VENV_DIR)/.validated $(VENV_DIR)/.tested
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@$(VENV_DIR)/bin/coverage erase
	rm -rf htmlcov

## Remove build artifacts and the entire Python virtual environment
clean-all: clean
	rm -rf $(VENV_DIR)