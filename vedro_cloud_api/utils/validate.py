from typing import Any, List

import valera
from district42.types import GenericSchema

__all__ = ("validate",)


def validate(value: Any, schema: GenericSchema) -> List[str]:
    result = valera.validate(schema, value)
    formatter = valera.Formatter()
    errors = [e.format(formatter) for e in result.get_errors()]
    return errors
