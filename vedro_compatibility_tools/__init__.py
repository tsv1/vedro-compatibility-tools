def validator_factory():
    from valeera import Formatter, Validator
    return Validator(Formatter())


def patch_schema(validator=None, substitutor=None):
    if validator is None:
        validator = validator_factory()
    if substitutor is None:
        from blahblah import Substitutor
        substitutor = Substitutor()
    from district42 import SchemaType
    SchemaType.__eq__ = lambda a, b: validator.validate(b, a)
    SchemaType.__mod__ = lambda self, val: self.accept(substitutor, val)


def patch_config(config):
    import vedro
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


__all__ = ("SchemaValidator", "patch_schema", "patch_config",)
__version__ = "0.0.1"
