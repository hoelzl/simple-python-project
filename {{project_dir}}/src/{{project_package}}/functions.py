def fun_with_doctest(n: int) -> int:
    """
    >>> fun_with_doctest(1)
    2
    >>> fun_with_doctest(2)
    4
    """
    return n * 2


def say_hi(name: str = "world"):
    print(f"Hello, {name}!")
