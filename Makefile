SHELL := /usr/bin/env bash
SKILL_NAME := sunless-skies-first-mate
DIST_DIR   := dist
VENV_DIR   := .venv
STAMP_FILE := $(VENV_DIR)/.installed

.PHONY: all venv validate build clean clean-all

all: validate build

## Automatically create .venv and install dependencies if missing or outdated
venv: $(STAMP_FILE)

$(STAMP_FILE): requirements-dev.txt
	@echo "==> Bootstrapping Python virtual environment in $(VENV_DIR)..."
	@python3 -m venv $(VENV_DIR)
	@$(VENV_DIR)/bin/pip install --upgrade --quiet pip
	@echo "==> Installing Python dependencies from requirements-dev.txt..."
	@$(VENV_DIR)/bin/pip install --quiet -r requirements-dev.txt
	@touch $(STAMP_FILE)

## Validate data_package.json and CSV seed tables using .venv Frictionless
validate: venv
	@FRICTIONLESS_BIN="$(VENV_DIR)/bin/frictionless" ./scripts/build_skill.sh --validate-only

## Build and package the deployable skill archive into dist/
build: venv
	@FRICTIONLESS_BIN="$(VENV_DIR)/bin/frictionless" ./scripts/build_skill.sh

## Remove build artifacts (preserves .venv for fast rebuilds)
clean:
	rm -rf $(DIST_DIR)

## Remove both build artifacts and the Python virtual environment
clean-all: clean
	rm -rf $(VENV_DIR)