from d42 import schema

__all__ = ("ProjectIdSchema",)

ProjectIdSchema = schema.str.regex(r"[a-z][a-z0-9-]{2,39}")
