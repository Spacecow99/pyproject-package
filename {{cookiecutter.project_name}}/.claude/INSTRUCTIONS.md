# {{ cookiecutter.project_name }}

{{ cookiecutter.package_description }}

## Project conventions

- Keep package code in `{{ cookiecutter.package_name }}` and tests in `tests/`.
- Keep project metadata and tool configuration in `pyproject.toml`.
- Follow the existing project structure and make focused changes.

## Commands

- Run tests with `pytest tests` or the configured Tox environments with `tox`.
- Check formatting with `black --check .`.
- Run Pylint with `pylint {{ cookiecutter.package_name }}`.
- Run Bandit with `bandit -r {{ cookiecutter.package_name }}`.
- Build the package with `flit build`.