# {{ cookiecutter.package_name }}

{{ cookiecutter.package_description }}

`{{ cookiecutter.package_name }}` is a Python package with a small addition helper and a command-line version check.

## Installation

After publishing the package to your package index, install it with:

```shell
python -m pip install {{ cookiecutter.project_name }}
```

To install from a source checkout, run this from the project root:

```shell
python -m pip install .
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

For a linked installation from a source checkout, run `flit install --symlink` from the project root. Run tests with `pytest tests`; use `tox` to test across the supported Python versions when those interpreters are installed.

## Authors

{{ cookiecutter.package_name }} was written by {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>.
