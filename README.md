# Pyproject.toml Package Cookiecutter

A minimal cookiecutter template for Python packages leveraging the pypackage.toml configuration file along with a standardized set of development tools.

Based heavily on the [cookiecutter-package-minimal template](https://github.com/kragniz/cookiecutter-pypackage-minimal).

## Usage

```
pip install cookiecutter
git clone https://github.com/Spacecow99/pyproject-package.git
cookiecutter pyproject-package/
```

## Explanations

### Python

The minimally supported Python version is set to Python3.7 by default.

### pyproject.toml

Package dependencies along with any tool configurations should be defined using the `pyproject.toml` file format. This helps cut down on the number of non-source files within the repository.

### Flit

Flit is used as the build-system for the package. Note that this comes with certain limitations, especially for a package that depends on C bindings. 

### Pylint

Linting is performed with pylint using the Google Python Styleguide as a base. Styleguide defined within `pyproject.toml` should override any system/user pylint settings.

### Black

Black is used for formatting should there be a requirement to enforce a standardized code structure/form.

### Sphinx

Sphinx is used to configure and build any external package documentation. All documentation should be markdown format except for inline code documentation.

In addition to the core Sphinx extensions, several others listed below are also configured.

#### Myst

The myst-parser extension is used to enable Sphinx to build markdown format documentation.

#### ReadTheDocs Theme

Sphinx should use the ReadTheDocs theme to provided consistent documentation look and feel whether the documentation is local or hosted on rtd.

### Bandit

Bandit is used as a rudementary security scanner to detect potential security defects during local development. 

### Pytest

Pytest is the testing framework used for building test cases.

### Tox

Tox is used to manage package tests across different python versions.
 
