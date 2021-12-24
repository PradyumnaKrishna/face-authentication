OS ?= $(shell python -c 'import platform; print(platform.system())')
PORT ?= 8000

all: environment lint start

environment: no-windows
	@echo 🔧 SETUP
	pip3 install 'poetry==1.1.6'
	poetry config virtualenvs.in-project true 
	poetry install

start: no-windows
	poetry run uvicorn app.main:app --reload --port $(PORT)

lint:
	@echo 💚 LINT
	@echo 1.Pylint
	poetry run pylint --extension-pkg-whitelist=pydantic app tests
	@echo 2.Black Formatting
	poetry run black --check app tests

auto-lint:
	@echo 💚 AUTO LINT
	@echo Auto-generating __init__
	poetry run mkinit app/core --write --recursive --black
	poetry run mkinit app/api --write --recursive --black
	@echo Reformatting using Black
	poetry run black .
	make lint

test-integration: no-windows
	@echo ✅ INTEGRATION TESTS
	poetry run pytest -s . -x

build: no-windows
	@echo 🔧 BUILD
	docker build -t face-auth .

# PRIVATE RECIPIES

no-windows:
ifeq ($(OS), Windows_NT)
	@echo Windows is not supported. Instead run this command in WSL2. For more details see README.md.
	exit 1
endif
