from setuptools import find_packages, setup

setup(
    name="nanoSQLite",
    version="1.1.4",
    packages=find_packages(),
    description="A lightweight wrapper for the SQLite3 Python module.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stefanluth/nanoSQLite",
    license="MIT",
    author="Stefan Luthardt",
)
