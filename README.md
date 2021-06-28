# Vedro Compatibility Tools

## Usage

```python
import vedro
from vedro_compatibility_tools import register, SchemaValidationPlugin, SchemaValidator

if __name__ == "__main__":
    validator = SchemaValidator()
    register(validator)

    vedro.run(plugins=[SchemaValidationPlugin(validator)])

```
