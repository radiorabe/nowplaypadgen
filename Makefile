.PHONY: install-tox
install-tox: ## Install tox into local python environment.
	pip install tox

.PHONY: init
init: ## Prepare local development environment.
	pip install -r requirements.txt

.PHONY: test
test: ## Run all tests.
	python setup.py test

.PHONY: api-doc
api-doc: ## Generate API docs using Sphinx.
	sphinx-apidoc -M -f -o docs/api nowplaypadgen

.PHONY: tox
tox: install-tox ## Run tests in multiple venvs using tox.
	tox

.PHONY: help
help: ## Display this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
