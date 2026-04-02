SHELL := /bin/bash

.PHONY: install-dev lint test verify verify-all quality quality-ruff quality-ruff-github quality-format quality-yaml quality-markdown quality-files quality-shell repo-contract coverage static-analysis typecheck package-check build-deb docker-test docker-harness-build docker-harness-test docker-harness-ui-video predictive-build-test-all act-run act-run-yellow clean

PYTHON := $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else command -v python3; fi)
RUFF := $(PYTHON) -m ruff
PYTEST := $(PYTHON) -m pytest
PREDICTIVE_LOG := REQUESTED.predict_vs_actual.inline.md
ENABLE_DOCKER_SMOKE ?= false
COVERAGE_FAIL_UNDER ?= 55
COVERAGE_WARN_UNDER ?= 80
DOCKER_HARNESS_IMAGE ?= desktop-markdown-sync-kali-harness
DOCKER_HARNESS_ARTIFACTS ?= artifacts/outputs/kali-harness

install-dev:
	$(PYTHON) -m pip install -e '.[dev]'

lint:
	@$(RUFF) check .

test:
	@$(PYTEST)

quality: quality-ruff quality-format quality-yaml quality-markdown quality-files quality-shell

quality-ruff:
	@$(RUFF) check .

quality-ruff-github:
	@$(RUFF) check . --output-format=github

quality-format:
	@$(PYTHON) -m ruff format --check .

quality-yaml:
	@$(PYTHON) -m yamllint .

quality-markdown:
	@$(PYTHON) scripts/check_markdown.py

quality-files:
	@$(PYTHON) scripts/check_file_formats.py

quality-shell:
	@$(PYTHON) scripts/check_shell_scripts.py

repo-contract:
	@$(PYTHON) scripts/check_repo_contract.py

coverage:
	@$(PYTEST) --cov-fail-under=$(COVERAGE_FAIL_UNDER)
	@$(PYTHON) scripts/coverage_gate.py coverage.xml --warn-under $(COVERAGE_WARN_UNDER)

static-analysis:
	@mkdir -p .cache
	@$(PYTHON) -m compileall -q src scripts
	@$(PYTHON) -m bandit -q -r src scripts -f json -o .cache/bandit.json --exit-zero
	@$(PYTHON) scripts/bandit_gate.py .cache/bandit.json

typecheck:
	@$(PYTHON) -m mypy

package-check:
	@$(PYTHON) -m pip check
	@$(PYTHON) -m build --sdist --wheel

verify-all: quality repo-contract coverage static-analysis typecheck package-check build-deb

verify: verify-all

docker-test:
	@docker build -t desktop-markdown-sync-test -f docker/Dockerfile .
	@docker run --rm desktop-markdown-sync-test

docker-harness-build:
	@docker build -t $(DOCKER_HARNESS_IMAGE) -f docker/KaliHarness.Dockerfile .

docker-harness-test: docker-harness-build
	@mkdir -p $(DOCKER_HARNESS_ARTIFACTS)
	@docker run --rm \
		-v "$(PWD)/$(DOCKER_HARNESS_ARTIFACTS):/artifacts" \
		$(DOCKER_HARNESS_IMAGE) \
		/opt/desktop-markdown-sync/docker/run-kali-harness.sh /artifacts

docker-harness-ui-video: docker-harness-test
	@ls -l $(DOCKER_HARNESS_ARTIFACTS)/ui/fixture-pack-demo.mp4

build-deb:
	@$(PYTHON) scripts/build_deb.py

predictive-build-test-all:
	@mkdir -p .cache
	@printf 'predicted: quality exits 0\n' >> $(PREDICTIVE_LOG)
	@$(MAKE) quality > .cache/predictive-quality.log 2>&1; rc=$$?; \
		printf 'actual: quality exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-quality.log; \
		test "$$rc" -eq 0
	@printf 'predicted: coverage exits 0\n' >> $(PREDICTIVE_LOG)
	@$(MAKE) coverage > .cache/predictive-coverage.log 2>&1; rc=$$?; \
		printf 'actual: coverage exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-coverage.log; \
		test "$$rc" -eq 0
	@printf 'predicted: static-analysis exits 0\n' >> $(PREDICTIVE_LOG)
	@$(MAKE) static-analysis > .cache/predictive-static-analysis.log 2>&1; rc=$$?; \
		printf 'actual: static-analysis exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-static-analysis.log; \
		test "$$rc" -eq 0
	@printf 'predicted: typecheck exits 0\n' >> $(PREDICTIVE_LOG)
	@$(MAKE) typecheck > .cache/predictive-typecheck.log 2>&1; rc=$$?; \
		printf 'actual: typecheck exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-typecheck.log; \
		test "$$rc" -eq 0
	@printf 'predicted: package-check exits 0\n' >> $(PREDICTIVE_LOG)
	@$(MAKE) package-check > .cache/predictive-package-check.log 2>&1; rc=$$?; \
		printf 'actual: package-check exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-package-check.log; \
		test "$$rc" -eq 0
	@printf 'predicted: deb build exits 0\n' >> $(PREDICTIVE_LOG)
	@$(PYTHON) scripts/build_deb.py > .cache/predictive-build-deb.log 2>&1; rc=$$?; \
		printf 'actual: deb build exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-build-deb.log; \
		test "$$rc" -eq 0
	@printf 'predicted: docker smoke exits 0 when ENABLE_DOCKER_SMOKE=true\n' >> $(PREDICTIVE_LOG)
	@if [ "$(ENABLE_DOCKER_SMOKE)" = "true" ]; then \
		docker build -t desktop-markdown-sync-test -f docker/Dockerfile . > .cache/predictive-docker-build.log 2>&1 && \
		docker run --rm desktop-markdown-sync-test > .cache/predictive-docker-run.log 2>&1; rc=$$?; \
		printf 'actual: docker smoke exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-docker-build.log; \
		cat .cache/predictive-docker-run.log; \
		test "$$rc" -eq 0; \
	else \
		printf 'actual: docker smoke skipped (ENABLE_DOCKER_SMOKE=false)\n' >> $(PREDICTIVE_LOG); \
		echo "docker smoke skipped; set ENABLE_DOCKER_SMOKE=true to enable"; \
	fi
	@printf 'predicted: kali harness exits 0 when ENABLE_DOCKER_SMOKE=true\n' >> $(PREDICTIVE_LOG)
	@if [ "$(ENABLE_DOCKER_SMOKE)" = "true" ]; then \
		$(MAKE) docker-harness-test > .cache/predictive-kali-harness.log 2>&1; rc=$$?; \
		printf 'actual: kali harness exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-kali-harness.log; \
		test "$$rc" -eq 0; \
	else \
		printf 'actual: kali harness skipped (ENABLE_DOCKER_SMOKE=false)\n' >> $(PREDICTIVE_LOG); \
		echo "kali harness skipped; set ENABLE_DOCKER_SMOKE=true to enable"; \
	fi

act-run:
	@act push -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest

act-run-yellow:
	@act push -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest || true

clean:
	rm -rf .cache .coverage coverage.xml .pytest_cache .ruff_cache dist src/*.egg-info src/desktop_markdown_sync.egg-info
