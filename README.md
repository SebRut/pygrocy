# pygrocy
[![Build Status](https://travis-ci.com/SebRut/pygrocy.svg?branch=master)](https://travis-ci.com/SebRut/pygrocy)
[![Coverage Status](https://coveralls.io/repos/github/SebRut/pygrocy/badge.svg?branch=master)](https://coveralls.io/github/SebRut/pygrocy?branch=master)
![PyPI](https://img.shields.io/pypi/v/pygrocy.svg)

## Example
```
from pygrocy import Grocy

# get a grocy instance
grocy = Grocy("https://example.com/api/", "GROCY_API_KEY")

# get current stock
for entry in grocy.stock():
    print("{} in stock for product id {}".format(entry.product_id, entry.amount))
```
