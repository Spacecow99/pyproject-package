#!/usr/bin/env python3

"""
CLI application entry point for {{ cookiecutter.package_name }}.

{{ cookiecutter.package_description }}
"""

import argparse
import os
import sys

from {{ cookiecutter.package_name }} import __version__


def main():
    parser = argparse.ArgumentParser(prog="{{ cookiecutter.package_name }}")
    parser.add_argument("--version", action="version", version=f"{__version__}")
    args = parser.parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")

