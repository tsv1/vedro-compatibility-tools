from typing import Optional

from blahblah import Substitutor
from district42 import SchemaType
from valeera import AbstractFormatter, AbstractValidator, Formatter, Validator
from vedro.core import Dispatcher, Plugin
from vedro.events import ExceptionRaisedEvent


def register(validator: Optional[AbstractValidator] = None,
             substitutor: Optional[Substitutor] = None) -> None:
    if validator is None:
        validator = Validator(Formatter())
    if substitutor is None:
        substitutor = Substitutor()
    SchemaType.__eq__ = lambda a, b: validator.validate(b, a).passes()
    SchemaType.__mod__ = lambda self, val: self.accept(substitutor, val)


class SchemaValidator(Validator):
    def __init__(self, formatter: Optional[AbstractFormatter] = None) -> None:
        super().__init__(formatter if formatter else Formatter())

    def reset(self) -> None:
        self._errors = []


class SchemaValidationPlugin(Plugin):
    def __init__(self, validator: SchemaValidator) -> None:
        self._validator = validator

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ExceptionRaisedEvent, self.on_excpetion_raised)

    def on_excpetion_raised(self, event: ExceptionRaisedEvent) -> None:
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


__all__ = ("SchemaValidator", "SchemaValidationPlugin", "register",)
__version__ = "0.1.2"
