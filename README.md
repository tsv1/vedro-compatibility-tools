# Vedro Compatibility Tools

## Usage

```python
import vedro
from vedro.plugins.validator import Validator
from vedro_compatibility_tools import SchemaValidator, patch_config, patch_schema

from config import Config

if __name__ == "__main__":
    validator = SchemaValidator()
    patch_schema(validator)
    patch_config(Config)

    vedro.run(validator=Validator(validator))
```
