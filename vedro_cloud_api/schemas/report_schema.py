from d42 import schema

__all__ = ("ReportIdSchema",)

ReportIdSchema = schema.str.len(1, 40)
