.PHONY: coverage coverage-term test install-dependencies

coverage: install-dependencies
	pytest --cov-report=xml --cov=../ --cov-branch
	rm -rf .coverage

coverage-term: install-dependencies
	pytest --cov-report=term --cov=../ --cov-branch
	rm -rf .coverage

test:
	pytest

install-dependencies:
	pip3 install -r dev-requirements.txt

commit-bump-version:
	git add openstep_parser/__init__.py
	git commit -m "chore: bump version to $(shell python3 -c 'import openstep_parser; print(openstep_parser.__version__)')"
	git tag -f "$(shell python3 -c 'import openstep_parser; print(openstep_parser.__version__)')"
	git push origin master --tags
