# pygrocy
[![Development Build Status](https://api.travis-ci.com/SebRut/pygrocy.svg?branch=develop)](https://travis-ci.com/SebRut/pygrocy)
[![PyPI](https://img.shields.io/pypi/v/pygrocy.svg)](https://pypi.org/project/pygrocy/)
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

## Development testing
You need a Grocy instance running in demo mode at localhost with https (docker or a php server)
You can setup url, port and ssl in test/test_const.py

```
  curl -L https://github.com/grocy/grocy-docker/raw/master/Dockerfile-grocy > Dockerfile-grocy
  docker-compose build grocy
  docker pull grocy/grocy-docker:nginx
  docker-compose up -d
  curl -kX GET https://localhost
```
