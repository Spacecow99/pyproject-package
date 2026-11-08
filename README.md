# Pyproject.toml Package Cookiecutter

A Cookiecutter template for creating small Python packages. Generated projects
use `pyproject.toml` for build metadata and tool configuration, and include a
package module, a command-line version check, tests, and a Sphinx documentation
scaffold.

The template is based on
[cookiecutter-pypackage-minimal](https://github.com/kragniz/cookiecutter-pypackage-minimal).

## Requirements

- Python 3.7 or newer, below Python 4.0, for generated packages.
- Cookiecutter to generate a project.

The generated package has no runtime dependencies. Development tools are
declared as optional dependency groups so you can install only the tools you
need.

## Create a project

Install Cookiecutter and generate a package directly from this repository:

```shell
python -m pip install cookiecutter
cookiecutter https://github.com/Spacecow99/pyproject-package.git
```

Cookiecutter prompts for the project details:

| Prompt | Purpose | Default |
| --- | --- | --- |
| `author_name` | Package author and maintainer name | `First Last` |
| `author_email` | Author and maintainer email | `first.last@example.com` |
| `project_name` | Distribution name and generated project directory | `pyproject-package` |
| `package_name` | Importable Python module name | Derived from `project_name`, with hyphens and spaces replaced by underscores |
| `package_version` | Initial package version | `0.0.1` |
| `package_description` | Short package description | `A pyproject compliant cookiecutter template for Python packages.` |
| `package_url` | Source URL recorded in package metadata | A PyPI project URL for `project_name` |

Enter values appropriate for your package; the defaults are examples. For
example, a project named `example-package` gets an import name of
`example_package`. Cookiecutter creates the generated project directory in the
current working directory.

To generate from a local clone instead, clone this repository and pass its
directory to Cookiecutter:

```shell
git clone https://github.com/Spacecow99/pyproject-package.git
python -m pip install cookiecutter
cookiecutter pyproject-package/
```

## Use the generated package

Change to the generated project directory before running package commands.
Install from its source checkout with pip:

```shell
cd <project-name>
python -m pip install .
```

The generated package provides a small `sum` helper and a module entry point
that prints the installed package version:

```python
from example_package import sum

print(sum(2, 3))  # 5
```

Here `example_package` is an example import name; replace it with the module
name you chose. To check the version from the command line (again, substituting
your module name):

```shell
python -m <package_name> --version
```

The project is configured for Flit. To install it as a linked development
checkout, install the development tools and run Flit's symlink installation:

```shell
python -m pip install ".[dev]"
flit install --symlink
```

## Development and documentation tools

Generated projects configure these tools in `pyproject.toml`.

| Tool | Purpose | Typical usage |
| --- | --- | --- |
| [Flit](https://flit.pypa.io/) | Builds and installs the package from its `pyproject.toml` metadata. It is a lightweight fit for pure-Python packages; projects with C extensions may need a different build backend. | `flit install --symlink` for a linked development install; `flit build` to build distributions. |
| [Pylint](https://pylint.readthedocs.io/) | Checks Python code for errors and style issues. The configuration uses Google Python Styleguide conventions as its basis and is stored in `pyproject.toml`. | `pylint <package_name>` |
| [Black](https://black.readthedocs.io/) | Formats Python code consistently, with an 80-character line length configured by default. | `black <package_name> tests` |
| [Bandit](https://bandit.readthedocs.io/) | Performs a basic static scan for common security issues in Python code. It is a development aid, not a substitute for a security review. | `bandit -r <package_name>` |
| [Pytest](https://docs.pytest.org/) | Runs the package's tests. The generated template includes a sample test. | `pytest tests` |
| [Tox](https://tox.wiki/) | Creates isolated test environments to run the test suite across configured Python versions. | `tox` |
| [Sphinx](https://www.sphinx-doc.org/) | Builds the project's external documentation. | `make -C docs html` |
| [MyST Parser](https://myst-parser.readthedocs.io/) | Lets Sphinx parse Markdown documentation. | Write Markdown pages under `docs/source/`, then build with Sphinx. |
| [Read the Docs theme](https://sphinx-rtd-theme.readthedocs.io/) | Applies the Read the Docs theme to local and hosted Sphinx documentation. | Enabled in the Sphinx configuration; build with `make -C docs html`. |

Install the optional tools by task. The groups are defined in the generated
project's `pyproject.toml`:

```shell
python -m pip install ".[dev]"       # Flit, Black, Pylint, Bandit
python -m pip install ".[test]"      # Tox, Pytest
python -m pip install ".[docs]"      # Sphinx, theme, MyST Parser
python -m pip install ".[dev,test,docs]"  # All optional tools
```

Run the sample tests with `pytest tests`. Tox is configured with environments
for Python 3.7 through 3.15; each interpreter must be available on your system
to run its corresponding environment. Build the documentation with
`make -C docs html`; generated HTML is placed under `docs/build/html/`.
