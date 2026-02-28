# DataEngineerToolbox
1. Set up virtual environment
```
python -m venv venv
venv\Scripts\activate
```
2. Install build dependencies

```
pip install build
```
3. Install package dependencies
```
pip install -e .
```
4. Build the wheel
```
python -m build
```
This will generate two files in the dist folder:

- dataeng_toolbox-0.1.0.tar.gz (source distribution)
- dataeng_toolbox-0.1.0-py3-none-any.whl (wheel)

5. (Optional) Publish to PyPI

```
pip install twine
twine upload dist/*
```

You will be prompted for your PyPI username and password.