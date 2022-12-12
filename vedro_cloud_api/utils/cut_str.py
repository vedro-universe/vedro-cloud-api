__all__ = ("cut_str",)


def cut_str(string: str, length: int, separator: str = "..") -> str:
    assert length > len(separator)

    if len(string) <= length:
        return string

    length -= len(separator)
    return string[:length // 2] + separator + string[-length // 2:]
