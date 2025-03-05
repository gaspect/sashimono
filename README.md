# Sashimono

![Coverage Status](https://github.com/gaspect/sashimono/actions/workflows/coverage.yml/badge.svg)  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

> A dependency injection container with a plugin approach

This package provides a DI container that can be populated using a plugin approach. This allows for code modularization and flexibility in application development.

## Motivation

The main goal of 'sashimono' is to split application development into multiple packages in a coherent way, allowing each piece to be developed and maintained in isolated environments without compromising the whole application and its integration.

## Architecture Notes

- **DI Container**: Acts as a centralized registry of components. It takes care of dependency injection.
- **Plugins System**: Acts as an entry point for container population. It allows for the integration of new features without modifying existing code.

## Example

### Defining Plugins

```python
# Imagine this in the plugin/number.py file in a package named 'plugin'
class NumberPlugin:
    def setup(self, container):
        container['number'] = container.singleton(5)
```

### Defining Package Configuration for Plugin Setup

```toml
[project]
name = "plugin"
version = "0.1.0"
description = "A sashimono plugin"
readme = "README.md"
requires-python = ">=3.12"
dependencies = ["setuptools>=75.8.2", "sashimono"]

[project.entry-points."sashimono.plugins"]
number = "plugin.number:NumberPlugin"

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

### How to Use It

We need to load the sashimono container:

```python
from sashimono import Container

c = Container()
print(c["number"])
```

The output must be '5'.

## Benefits

- **Modularity**: Allows for independent maintainability and development of application shards.
- **Extensibility**: Allows for the addition of new features without editing existing code.
- **Flexibility**: Eases configuration management and application personalization.

> Happy coding! 👋
