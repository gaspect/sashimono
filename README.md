# Sashimono

![Coverage Status](https://github.com/gaspect/sashimono/actions/workflows/coverage.yml/badge.svg)  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

> A lean dependency injection container

This package provides a lean and explicit DI container for code modularization and flexibility in application development.

## Motivation

The main goal of 'sashimono' in it's version `0.1.z` was split application development into multiple packages in a coherent way, allowing each piece to be developed and maintained in isolated environments without compromising the whole application and its integration. This meant that the package lived with two responsibilities, that of being a dependency container and that of being a plugin system. And while the initial idea of sashimono was fine, it made the package awkward to use for those who only wanted to use one of those features. So we decided to split the package into two that would fulfill those responsibilities separately. Since version `1.y.z`Sashimono only responds to the dependency container feature.

For this version we took a bit of inspiration from Bottle, to make the package so small, atomic and dependency-free that you can simply download it to your project folder instead of installing it. Although we will keep both options.

## Example

The idea of using a DI container revolves around the Container object and it's the main and only object that Sashimono explicitly provides.

```python
from sashimono import Container
```

The Container works as a dictionary that binds types and strings with the `function` that holds how the objects must be build using container itself.

```python
from sashimono import Container

c = Container()
c["number"] = Container.singleton(lambda c: 5)
print(c["number"])
```

The output must be 5

**But how do they work?** Sashimono uses the `singleton` and `factory` methods to define the construction expressions. Those expressions are executed when you try to access a specific object by building it. In the example above, the expression `lambda c:5` is executed when called in `print(c['number'])`
resulting in 5. The `c` parameter represents the container itself, so you can perform dependency injection within those build expressions. Because `singleton` was used, if we try to access `c["number"]` once again, it will give us the exact same instance that was already generated.

```python
from sashimono import Container

class Foo:
    def __init__(number):
        self.number  = number


c = Container()
c["number"] = Container.singleton(lambda c: 5)
c[Foo] = Container.factory(lambda c: Foo(c["number"]))
print(c[Foo].number)
```
*The output must be 5*

In this other example some manual DI was made and the `factory` method was used so every time you access to `Foo` through the container it will give you a new instance of `Foo`. The same can be made relaying on automatic injection as you can see in the next example.

```python
from sashimono import Container

class Foo:
    def __init__(number):
        self.number  = number

c = Container()
c["number"] = Container.singleton(5)
c[Foo] = Container.factory(Foo)
print(c[Foo].number)
```
*The output must be 5*

We made a tweak around class inheritance too. When you store a class and ask for it using its parent in the container, if that parent doesn't exist in the container, it'll return the child class that's already stored. Check it out in the next example.

```python
from sashimono import Container

class Foo:
    def __init__(number):
        self.number  = number

class Baa(Foo):
    ...

c = Container()
c["number"] = Container.singleton(5)
c[Baa] = Container.factory(Baa)
print(c[Foo].number)
```
*The output must be 5*

So even if `Foo` wasn't defined inside the container if you ask for it the container will search a child of `Foo`, in this case `Baa`, to return.

> That's all.Happy coding! 👋
