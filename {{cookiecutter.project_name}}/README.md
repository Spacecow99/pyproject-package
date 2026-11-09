# {{ cookiecutter.package_name }}

{{ cookiecutter.package_description }}

`{{ cookiecutter.package_name }}` is a Python package with a small addition helper and a command-line version check.

## Installation

After publishing the package to your package index, install it with:

```shell
python -m pip install {{ cookiecutter.project_name }}
```

To install from a source checkout for development, install Flit and run this from the project root:

```shell
python -m pip install flit
flit install --symlink
```

## Usage

Import the addition helper from Python:

```python
from {{ cookiecutter.package_name }} import sum

print(sum(2, 3))
```

Check the installed package version from the command line:

```shell
python -m {{ cookiecutter.package_name }} --version
```

## Requirements

- Python 3.7 or newer, below Python 4.0.
- No runtime dependencies.

## Development

Run tests with `pytest tests`; use `tox` to test across the supported Python versions when those interpreters are installed.

## Releases

The GitHub Actions workflow in `.github/workflows/ci.yml` runs the tests on Python 3.7 through 3.15 for every push and pull request, and builds the package with `flit build`, uploading the result as a `distributions` workflow artifact.

Publishing happens only when a GitHub Release is published: the `release` job rebuilds the package and attaches the files in `dist/` to that release. No credentials are stored in the repository. The job uses the automatic `GITHUB_TOKEN` with `contents: write` permission, so no repository secrets need to be configured.

To publish to a package index such as PyPI, add a separate publish step to the `release` job. Prefer PyPI trusted publishing (configure the repository as a trusted publisher on PyPI and grant the job `id-token: write`) over storing an API token. If you must use a token, store it as a GitHub Actions repository secret and never commit it. Remove the `Private :: Do Not Upload` classifier from `pyproject.toml` first, because PyPI rejects it.

## Authors

{{ cookiecutter.package_name }} was written by {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>.
