rm -r ./dist/*
python -m build
pip uninstall rajan_nse -y
pip install "./dist/rajan_nse-$VERSION-py3-none-any.whl"