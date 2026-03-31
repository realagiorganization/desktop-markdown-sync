SHELL := /bin/bash

.PHONY: install-dev lint test verify build-deb docker-test predictive-build-test-all act-run act-run-yellow clean

PYTHON := $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else command -v python3; fi)
RUFF := $(PYTHON) -m ruff
PYTEST := $(PYTHON) -m pytest
PREDICTIVE_LOG := REQUESTED.predict_vs_actual.inline.md
ENABLE_DOCKER_SMOKE ?= false

install-dev:
	$(PYTHON) -m pip install -e '.[dev]'

lint:
	@$(RUFF) check .

test:
	@$(PYTEST)

verify: lint test build-deb

docker-test:
	@docker build -t desktop-markdown-sync-test -f docker/Dockerfile .
	@docker run --rm desktop-markdown-sync-test

build-deb:
	@$(PYTHON) scripts/build_deb.py

predictive-build-test-all:
	@mkdir -p .cache
	@printf 'predicted: lint exits 0\n' >> $(PREDICTIVE_LOG)
	@$(RUFF) check . > .cache/predictive-lint.log 2>&1; rc=$$?; \
		printf 'actual: lint exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-lint.log; \
		test "$$rc" -eq 0
	@printf 'predicted: pytest exits 0\n' >> $(PREDICTIVE_LOG)
	@$(PYTEST) > .cache/predictive-test.log 2>&1; rc=$$?; \
		printf 'actual: pytest exits %s\n' "$$rc" >> $(PREDICTIVE_LOG); \
		cat .cache/predictive-test.log; \
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

act-run:
	@act -W .github/workflows/ci.yml -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest

act-run-yellow:
	@act -W .github/workflows/ci.yml -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest || true

clean:
	rm -rf .cache .coverage coverage.xml .pytest_cache .ruff_cache dist src/*.egg-info src/desktop_markdown_sync.egg-info
