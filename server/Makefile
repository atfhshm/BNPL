.DEFAULT_GOAL := dev

.PHONY: dev
dev:
	uv run manage.py runserver

.PHONY: makemigrations
makemigrations:
	uv run manage.py makemigrations

.PHONY: migrate
migrate: makemigrations
	uv run manage.py migrate

.PHONY: shell
shell:
	uv run manage.py shell

.PHONY: createsuperuser
createsuperuser:
	uv run manage.py createsuperuser

.PHONY: collectstatic
collectstatic:
	uv run manage.py collectstatic --noinput

.PHONY: clean
clean:
	uv run pyclean .

.PHONY: format
format:
	uv run ruff format

.PHONY: lint
lint:
	uv run ruff check .