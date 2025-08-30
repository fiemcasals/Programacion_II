# 14_doctest_examples.py — Doctests dentro de docstrings
def cuadrado(x: int) -> int:
    """Devuelve x^2.

    >>> cuadrado(3)
    9
    >>> cuadrado(-2)
    4
    """
    return x * x

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
