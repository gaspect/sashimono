def test_injection():
    from sashimono import Container

    class A:
        pass

    class B:
        def __init__(self, a: A):
            self.a = a

    c = Container()
    c[A] = Container.singleton(A)
    c[B] = Container.singleton(B)
    assert c[B].a is c[A]


def test_factory():
    from sashimono import Container

    c = Container()
    c["foo"] = Container.factory(object)
    assert isinstance(c["foo"], object)
    assert c["foo"] is not c["foo"]


def test_singleton():
    from sashimono import Container

    c = Container()
    c["foo"] = Container.singleton(object)
    assert isinstance(c["foo"], object)
    assert c["foo"] is c["foo"]


def test_injection_by_inheritance():
    from sashimono import Container

    class A: ...

    class Inherit(A): ...

    class B:
        def __init__(self, a: A):
            self.a = a

    c = Container()
    c[Inherit] = Container.singleton(Inherit)
    c[B] = Container.singleton(B)

    assert c[B].a is c[Inherit]


def test_injection_by_lambda():
    from sashimono import Container

    c = Container()
    c["number"] = Container.singleton(lambda _: 4)
    assert c["number"] == 4


def test_injection_by_annotation():
    from sashimono import Container

    class A:
        pass

    class B:
        def __init__(self, a):
            self.a = a

    c = Container()

    c["a"] = Container.singleton(A)
    c[B] = Container.singleton(B)

    assert c[B].a is c["a"]
