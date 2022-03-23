SHELL=/bin/bash
PACKAGE_NAME="pipetory"

publish: publish-pypi

publish-pypi:
	@echo "Building and publishing to PyPi"
	poetry version `git describe --tags --abbrev=0`
	poetry build -f sdist && poetry publish
