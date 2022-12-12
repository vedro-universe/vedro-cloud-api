from hashlib import blake2b

__all__ = ("make_hash",)


def make_hash(value: str) -> str:
    return blake2b(value.encode(), digest_size=20).hexdigest()
