from d42 import schema
from district42_exp_types.uuid_str import schema_uuid_str

__all__ = ("NewTokenSchema",)

NewTokenSchema = schema.dict({
    "token": schema_uuid_str,
    "description": schema.str.len(1, ...),
})
