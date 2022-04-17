from typing import Optional, Type

import valeera
from blahblah import Substitutor
from district42 import SchemaType
from valeera import AbstractFormatter, Formatter

from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import ExceptionRaisedEvent


class Validator(valeera.Validator):
    def __init__(self, formatter: Optional[AbstractFormatter] = None) -> None:
        super().__init__(formatter if formatter else Formatter())

    def reset(self) -> None:
        self._errors = []


class SchemaValidationPlugin(Plugin):
    def __init__(self, config: Type["SchemaValidator"]) -> None:
        super().__init__(config)
        self._validator = Validator()
        self._substitutor = Substitutor()

    def subscribe(self, dispatcher: Dispatcher) -> None:
        SchemaType.__eq__ = lambda a, b: self._validator.validate(b, a).passes()
        SchemaType.__mod__ = lambda s, v: s.accept(self._substitutor, v)

        dispatcher.listen(ExceptionRaisedEvent, self.on_exception_raised)

    def on_exception_raised(self, event: ExceptionRaisedEvent) -> None:
        if event.exc_info.type is not AssertionError:
            return
        errors = self._validator.errors()
        if len(errors) == 0:
            return
        self._validator.reset()
        message = "\n - " + "\n - ".join(errors)
        exception = AssertionError(message)
        event.exc_info.value = exception
        event.exc_info.type = type(exception)


class SchemaValidator(PluginConfig):
    plugin = SchemaValidationPlugin


__all__ = ("SchemaValidator", "SchemaValidationPlugin",)
__version__ = "0.2.0"
