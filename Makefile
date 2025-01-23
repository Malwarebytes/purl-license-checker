.DEFAULT_GOAL=help
.PHONY=help

ZIP = zip
PIP3 = python3 -m pip
PYTHON3 = python3
POETRY = poetry
SYFT = syft


clean: ## clean existing builds
	rm -rf ./dist || true
	rm -rf ./src/purl-license-checker/purl-license-checker.egg-info || true
	rm checksums.sha512 || true
	rm checksums.sha512.asc || true

release: ## Build a wheel
	$(POETRY) build
	$(SYFT) scan file:poetry.lock -o spdx-json > dist/sbom.json
	cd dist && sha512sum * > ../checksums.sha512
	gpg --detach-sign --armor checksums.sha512

dev: ## Build for dev
	$(POETRY) build

shell: ## Generate the shell autocompletion
	_GHAS_CLI_COMPLETE=source_bash purl-license-checker > purl-license-checker-complete.sh || true

deps: ## Fetch or update dependencies
	$(POETRY) update

help:
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort


.PHONY: help
