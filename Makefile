PROJECT_NAME=vedro_cloud_api
DB_DSN=postgresql://vedro_cloud:vedro_cloud@127.0.0.1:6432/vedro_cloud

.PHONY: install
install:
	@pip3 install --quiet --upgrade pip
	@pip3 install --quiet -r requirements.txt -r requirements-dev.txt

.PHONY: dev
dev:
	@python3 -m sanic vedro_cloud_api:create_app --host 127.0.0.1 --port 8080 --dev

.PHONY: migrate
migrate:
	@python3 -m yoyo apply --batch --no-config-file --database ${DB_DSN} ./migrations
	@python3 -m yoyo list --no-config-file --database ${DB_DSN} ./migrations

.PHONY: check-types
check-types:
	@python3 -m mypy ${PROJECT_NAME} --strict

.PHONY: check-imports
check-imports:
	@python3 -m isort ${PROJECT_NAME} --check-only

.PHONY: sort-imports
sort-imports:
	@python3 -m isort ${PROJECT_NAME}

.PHONY: check-style
check-style:
	@python3 -m flake8 ${PROJECT_NAME}

.PHONY: lint
lint: check-types check-style check-imports

.PHONY: all
all: install lint test
