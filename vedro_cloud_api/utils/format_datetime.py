from datetime import datetime

__all__ = ("format_datetime",)


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
