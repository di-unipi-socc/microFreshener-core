echo "Creating distribution for release..."
python3 setup.py sdist bdist_wheel
echo "Done"

echo "Releasing new MicroFreshener core release."
echo "The user and pass credentials are no longer supported."
echo "If you want to use the PyPI token, use  __token__ as username and the entire token value as password."
twine upload dist/*
