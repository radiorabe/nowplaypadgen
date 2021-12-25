.PHONY: init
init: ## Prepare local development environment.
	pip install -r requirements-dev.txt

.PHONY: test
test: ## Run all tests.
	pytest --pylint tests/

.PHONY: docs
docs: api-doc ## Generate documentation.
	make -C docs html

.PHONY: api-doc
api-doc: ## Generate API docs using Sphinx.
	sphinx-apidoc -M -f -o docs/api nowplaypadgen

.PHONY: clean
clean:  ## Clean dist
	rm -rf dist/ build/ .eggs/

.PHONY: dist
dist: clean ## Build dist
	python setup.py sdist bdist_wheel

.PHONY: help
help: ## Display this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
