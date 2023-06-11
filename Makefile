.PHONY: dev lint complex coverage pre-commit yapf sort



dev:
	pip install --upgrade pip pre-commit poetry
	pre-commit install
	poetry shell

lint:
	@echo "Running flake8"
	flake8 tenant_management_integrations/* --exclude patterns='build,cdk.json,cdk.context.json,.yaml'

complex:
	@echo "Running Radon"
	radon cc -e 'tests/*,cdk.out/*' .
	@echo "Running xenon"
	xenon --max-absolute B --max-modules A --max-average A -e 'tests/*,.venv/*,cdk.out/*' .

sort:
	isort ${PWD}

pre-commit:
	pre-commit run -a --show-diff-on-failure


pr: yapf sort pre-commit complex lint

yapf:
	yapf -i -vv --style=./.style --exclude=.venv --exclude=.build --exclude=cdk.out --exclude=.git  -r .
