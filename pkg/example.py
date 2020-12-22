from typing import List

from pydantic import validate_arguments


@validate_arguments
def func_1(arg1: int, arg2: str) -> List[str]:
    """Summary line.

    Extended description of function.

    :param int arg1: Description of arg1.
    :param str arg2: Description of arg2.
    :raise: ValueError if arg1 is equal to arg2
    :return: Description of return value
    :rtype: bool

    :example:

    >>> a=1
    >>> b=2
    >>> func(a,b)
    True
    """
    pass


@validate_arguments
def func_2(arg1: int, arg2: str) -> List[str]:
    """Summary line (Google style).

    Extended description of function.

    Args:
        arg1 (int): Description of arg1
        arg2 (str): Description of arg2

    Returns:
        bool: Description of return value

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `arg2` is equal to `arg1`.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> a=1
        >>> b=2
        >>> func_2(a,b)
        True
    """
    pass


@validate_arguments
def func_3(arg1: int, arg2: str) -> List[str]:
    """Summary line (Numpy style).

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    bool
        Description of return value

    Raises
    ------
    AttributeError
        The ``Raises`` section is a list of all exceptions
        that are relevant to the interface.
    ValueError
        If `arg2` is equal to `arg1`.

    See Also
    --------
    otherfunc: some other related function

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a=1
    >>> b=2
    >>> func_3(a,b)
    True
    """
    pass


def _func_4(arg1: int, arg2: str) -> List[str]:
    pass
