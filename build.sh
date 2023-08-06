rm -rf build
rm -rf dist
rm -rf *.egg-info

python setup.py sdist bdist_wheel
twine check dist/*

