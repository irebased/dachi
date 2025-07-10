test: ## Run tests
	pytest

test-safe: ## Run tests without coverage (prevents terminal crashes)
	pytest --no-cov

test-cov: ## Run tests with coverage
	pytest --cov=dachi --cov-report=html --cov-report=term-missing