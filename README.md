# Vedro Compatibility Tools

## Usage

```python
import vedro
from vedro_compatibility_tools import SchemaValidationPlugin, SchemaValidator, patch_config, patch_schema

from config import Config

if __name__ == "__main__":
    validator = SchemaValidator()
    patch_schema(validator)
    patch_config(Config)

    vedro.run(plugins=[SchemaValidationPlugin(validator)])
```
