.PHONY: clear-log
clear-log:
	rm -rf ./logs/*
	mkdir -p ./logs
.PHONY: isort
isort:
	ruff check --select I --fix
.PHONY: check
check:
	ruff check
.PHONY: check-fix
check-fix:isort check-imports
	ruff check --fix 
.PHONY: check-imports
check-imports:
	ruff check --select F401 --fix
.PHONY:clean
clean:clear-log
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf ./.ruff_cache
	rm -rf ./.pytest_cache
	rm -rf ./.coverage
	rm -rf ./htmlcov
.PHONY:create-secret-key
create-secret-key:
	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
.PHONY:lint
lint:format isort check-imports
	djlint templates --reformat --format-css --format-js --indent 4 --profile django
.PHONY: format
format:
	ruff format
.PHONY:get-uid
get-uid:
	@echo UID=$$UID
	@echo GID=$$GID