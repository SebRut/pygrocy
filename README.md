# pygrocy
[![Development Build Status](https://api.travis-ci.com/SebRut/pygrocy.svg?branch=develop)](https://travis-ci.com/SebRut/pygrocy)
[![PyPI](https://img.shields.io/pypi/v/pygrocy.svg)](https://pypi.org/project/pygrocy/)
![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.8%20%7C%203.9-blue)
![Grocy Version](https://img.shields.io/badge/grocy-3.1.0-yellow)
[![Coverage Status](https://coveralls.io/repos/github/SebRut/pygrocy/badge.svg?branch=master)](https://coveralls.io/github/SebRut/pygrocy?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/sebrut/pygrocy/badge)](https://www.codefactor.io/repository/github/sebrut/pygrocy)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[Documentation](https://sebrut.github.io/pygrocy/)

## Installation

`pip install pygrocy`

## Usage
Import the package: 
```python
from pygrocy import Grocy
```

Obtain a grocy instance:
```python
grocy = Grocy("https://example.com", "GROCY_API_KEY")
```
or
```python
grocy = Grocy("https://example.com", "GROCY_API_KEY", port = 9192, verify_ssl = True)
```

Get current stock:
```python
for entry in grocy.stock():
    print("{} in stock for product id {}".format(entry.available_amount, entry.id))
```

# Support

If you need help using pygrocy check the [discussions](https://github.com/SebRut/pygrocy/issues) section. Feel free to create an issue for feature requests, bugs and errors in the library.

## Development testing
You need tox and Python 3.6/8/9 to run the tests. Navigate to the root dir of `pygrocy` and execute `tox` to run the tests.
