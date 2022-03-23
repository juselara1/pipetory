from typing import Callable

def compose(f1: Callable, f2: Callable) -> Callable:
    """
    Compose two functions.

    Parameters
    ----------
    f1 : Func
        The first function.
    f2 : Func
        The second function.

    Returns
    -------
    Func
        The composed function.
    """
    return lambda data: f1(f2(data))
