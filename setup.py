from setuptools import setup, find_packages

setup(
    name="nanoSQLite",
    version="1.0.1",
    packages=find_packages("./nanoSQLite"),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stefanluth/nanoSQLite",
    license="MIT",
    author="Stefan Luthardt",
)
