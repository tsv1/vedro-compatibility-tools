import vedro
from blahblah import Substitutor
from district42 import SchemaType
from vedro._core import ExcInfo
from vedro._events import StepFailEvent
from vedro.plugins import Plugin


def validator_factory():
    from valeera import Formatter, Validator
    return Validator(Formatter())


def patch_schema(validator=None, substitutor=None):
    if validator is None:
        validator = validator_factory()
    if substitutor is None:
        substitutor = Substitutor()
    SchemaType.__eq__ = lambda a, b: validator.validate(b, a)
    SchemaType.__mod__ = lambda self, val: self.accept(substitutor, val)


def patch_config(config):
    vedro.config = config


class SchemaValidator:
    def __init__(self, factory=validator_factory):
        self._factory = factory
        self._validator = factory()

    def validate(self, actual, expected):
        self._validator.validate(actual, expected)
        return self._validator.passes()

    def errors(self):
        return self._validator.errors()

    def reset(self):
        self._validator = self._factory()


class SchemaValidationPlugin(Plugin):
    def __init__(self, validator):
        self._validator = validator

    def subscribe(self, dispatcher):
        dispatcher.listen(StepFailEvent, self.on_step_fail)

    def on_step_fail(self, event):
        errors = self._validator.errors()
        if len(errors) == 0:
            return
        self._validator.reset()
        message = "\n - " + "\n - ".join(errors)
        exception = AssertionError(message)
        exc_info = ExcInfo(type(exception), exception, event.step_result.exc_info.traceback)
        event.step_result.set_exc_info(exc_info)


__all__ = ("SchemaValidator", "SchemaValidationPlugin", "patch_schema", "patch_config",)
__version__ = "0.1.0"
