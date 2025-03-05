import typing
import inspect
import pkg_resources
from functools import cache
from typing import Callable, Any

class _Binder:

    def __init__(self, klass: typing.Type):
        self._klass = klass

    def __call__(self, services: "Container"):
        try:
            # Obtener el método __init__ de la clase
            init_method = next(
                member
                for name, member in inspect.getmembers(self._klass, inspect.isfunction)
                if name == "__init__"
            )
            # Obtener las anotaciones y argumentos del método __init__
            annotations = init_method.__annotations__
            args = [
                arg
                for arg in inspect.signature(init_method).parameters
                if arg != "self"
            ]

            # Crear un diccionario con los servicios
            kwargs = {k: services[v] for k, v in annotations.items()}
            kwargs.update({k: services[k] for k in args if k not in kwargs})

            # Retornar la clase con los servicios inyectados
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

    def __init__(self, container: dict = None):
        from sashimono.abc import Plugin  # avoid circular import     

        self._container = container or {}
        for entry_point in pkg_resources.iter_entry_points("sashimono.plugins"):
            klass = entry_point.load()
            if issubclass(klass, Plugin):
                klass().setup(self)

    def _find_key(self, key: type) -> type | None:
        if key in self._container:
            return key

        for k in self._container:
            if inspect.isclass(key) and inspect.isclass(k) and issubclass(k, key):
                return k

        return None

    def __getitem__[T](self, key: str | type[T]) -> T | typing.Any:
        key = self._find_key(key) or key
        if isinstance(self._container[key], _Factory):
            return self._container[key](self)
        return self._container[key]

    def __setitem__[
        T
    ](self, key: str | type[T], value: T | typing.Callable[["Container"], T]):
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

    def __iter__(self):
        return self._container.__iter__()

    def __xor__(self, other: "Container"):
        container = self._container | other._container
        return Container(container)
