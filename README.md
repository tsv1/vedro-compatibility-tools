# Vedro Compatibility Tools

## Usage

```python
import vedro
import vedro_compatibility_tools as v

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class SchemaValidator(v.SchemaValidator):
            enabled = True
```
