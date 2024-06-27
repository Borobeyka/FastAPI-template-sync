.PHONY: all

project := app

help::
	@echo "Available commands:"
	@grep --color=never --extended-regexp --only '^\w[^: ]+:' Makefile | sed -E -e 's/^([^: ]+):/ - \1/'

fmt:: isort black

isort::
	isort $(project) --py 311

black::
	black $(project) --target-version py311

fmt-check::
	isort --check --diff $(project)
	black --check --diff $(project)

flake8::
	flake8 $(project)

prepare::
	pip install -r requirements.txt

prepare-dev::
	pip install -r requirements.dev.txt