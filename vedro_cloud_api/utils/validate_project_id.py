import string

__all__ = ("validate_project_id",)


def validate_project_id(project_id: str) -> bool:
    alphabet = set(string.ascii_lowercase + string.digits + "_")
    return all(x in alphabet for x in project_id)
