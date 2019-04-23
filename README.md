# pygrocy
[![Build Status](https://travis-ci.com/SebRut/pygrocy.svg?branch=master)](https://travis-ci.com/SebRut/pygrocy)
[![PyPI](https://img.shields.io/pypi/v/pygrocy.svg)](https://pypi.org/project/pygrocy/)
[![Coverage Status](https://coveralls.io/repos/github/SebRut/pygrocy/badge.svg?branch=master)](https://coveralls.io/github/SebRut/pygrocy?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/sebrut/pygrocy/badge)](https://www.codefactor.io/repository/github/sebrut/pygrocy)

[Documentation](https://sebrut.github.io/pygrocy/pygrocy/grocy.html)

## Installation

`pip install pygrocy`

## Usage
Import the package: 
```python
from pygrocy import Grocy
```

Obtain a grocy instance:
```python
grocy = Grocy("https://example.com/api/", "GROCY_API_KEY")
```

Get current stock:
```python
for entry in grocy.stock():
    print("{} in stock for product id {}".format(entry.product_id, entry.amount))
```
