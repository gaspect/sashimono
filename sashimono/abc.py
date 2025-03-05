from sashimono.di import Container
from typing import final, Protocol, runtime_checkable

@runtime_checkable
class Plugin(Protocol):

    @final
    def __init__(self):
        pass
    
    def setup(self, container: Container):
        raise NotImplementedError("You must implement the setup method")
