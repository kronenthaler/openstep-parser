.PHONY: coverage coverage-term test

coverage:
	pytest --cov-report=xml --cov=./openstep_parser --cov-branch
	rm -rf tests/.coverage

coverage-term:
	pytest --cov-report=term --cov=./openstep_parser --cov-branch
	rm -rf tests/.coverage

test:
	pytest