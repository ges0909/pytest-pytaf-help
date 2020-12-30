from docstring_parser import parse


def test_parse_google_doc_string():
    google = """Summary line (Google style).

    Extended description of function.

    Use:
        bliblablu

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
    doc_string = parse(google)
    # /Use:\s+(\w+[ \w]*)/
    pattern = re.compile(r"[\n\w]*Use:\s+(\w+[ \w]*)", re.MULTILINE)
    # match = pattern.match(doc_string.long_description)
    match = pattern.match("\nUse: \nabc")
    pass
