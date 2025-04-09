import typing
import inspect
from functools import cache
from typing import Callable, Any


class _Binder:

    def __init__(self, klass: typing.Type):
        self._klass = klass

    def __call__(self, container: "Container"):
        try:
            # Get the __init__ method of the class
            init_method = next(
                member
                for name, member in inspect.getmembers(self._klass, inspect.isfunction)
                if name == "__init__"
            )
            # Get the annotations and arguments of the __init__ method
            annotations = init_method.__annotations__
            args = [
                arg
                for arg in inspect.signature(init_method).parameters
                if arg != "self"
            ]

            # Create a dictionary with the values of the container using the annotations and arguments
            kwargs = {k: container[v] for k, v in annotations.items()}
            kwargs.update({k: container[k] for k in args if k not in kwargs})

            # Return the class instance with the injected values
            return self._klass(**kwargs)
        except StopIteration:
            return self._klass()


class _Factory:

    def __init__(self, f: Callable):
        self.f = f

    def __call__(self, s: "Container"):
        if callable(self.f):
            return self.f(s)
        return self.f


class _Singleton(_Factory):
    @cache
    def __call__(self, s: "Container"):
        return super().__call__(s)


class Container:

    def __init__(self, default: "Container" = None):

        self._container = default._container.copy() if default else {}

    def _find_key(self, key: type) -> type | None:
        if key in self._container:
            return key
        klass = inspect.isclass(key)
        for k in self._container:
            if klass and inspect.isclass(k) and issubclass(k, key):
                return k

        return None

    def __getitem__[T](self, key: str | type[T]) -> T | typing.Any:
        key = self._find_key(key) or key
        return self._container[key](self)

    def __setitem__[T](
        self, key: str | type[T], value: _Factory
    ):
        assert isinstance(value, _Factory), "Use Container.singleton or Container.factory"
        self._container[key] = value

    @staticmethod
    def _create_obj(item: type | Callable | Any) -> Callable:
        if inspect.isclass(item):
            return _Binder(item)
        elif inspect.isfunction(item):
            return item
        else:
            return lambda _: item

    @staticmethod
    def factory(item: type | Callable | Any):
        return _Factory(Container._create_obj(item))

    @staticmethod
    def singleton(item: type | Callable | Any):
        return _Singleton(Container._create_obj(item))

    def __xor__(self, other: "Container"):
        container = self._container | other._container
        return Container(container)
