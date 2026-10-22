#!/usr/bin/env python3
"""
Setup script for ring-evidence-mcp.
Configuration is defined in pyproject.toml.
"""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        package_dir={"": "src"},
        packages=find_packages(where="src"),
    )
