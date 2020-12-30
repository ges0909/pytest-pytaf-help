import os
import re
from pathlib import Path
from typing import Iterator, List, Tuple

from docstring_parser import parse
from pdoc import Module


# pdoc.tpl_lookup
# """
# A mako.lookup.TemplateLookup object that knows how to load templates from the file system.
# You may add additional paths by modifying the object's directories attribute.
# """


# def docfilter(doc: Doc) -> bool:
#     """
#
#     'docfilter' is an optional predicate that controls which documentation objects are
#     shown in the output. It is a function that takes a single argument (a documentatio
#     object) and returns True or False. If False, that object will not be documented.
#
#     Args:
#         doc:
#
#     Returns:
#
#     """
#     return True


def module_list(module_names: List[str]) -> List[Tuple[str, str]]:
    """for each module returns a tuple consisting of module name and docstring of module's __init__.py"""
    modules = (Module(module=name) for name in module_names)
    return [(module.name, module.docstring) for module in modules]


def get_modules_recursively(module: Module) -> Iterator[Module]:
    yield module
    for sub_module in module.submodules():
        yield from get_modules_recursively(module=sub_module)


def write_file(path: Path, module: Module, ext: str = "html", **kwargs) -> None:
    assert ext in ("html", "md")
    with open(str(path) + "." + ext, "w", encoding="utf-8") as stream:
        if ext == "html":
            stream.write(module.html(show_source_code=False, **kwargs))  # external_links=True
        else:
            stream.write(module.text(**kwargs))  # external_links=True


def write_module_doc(module_names: List[str], output_dir: Path) -> None:
    # create root index file
    output_dir.mkdir(parents=True, exist_ok=True)
    write_file(path=output_dir / "index", module=Module("."), modules=module_list(module_names))
    #
    for name in module_names:
        for module in get_modules_recursively(module=Module(module=name)):
            module_name_parts = module.name.split(".")
            if module.is_package:
                output_dir_ = output_dir / "/".join(module_name_parts)
                output_dir_.mkdir(parents=True, exist_ok=True)
                file_path = output_dir_ / "index"
            else:
                file_path = output_dir / "/".join(module_name_parts)
            write_file(path=file_path, module=module)


def serve_module_doc(web_dir: Path):
    import http.server
    import socketserver

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            pass

    os.chdir(str(web_dir))
    with socketserver.TCPServer(server_address=("localhost", 0), RequestHandlerClass=QuietHandler) as httpd:
        print(f"see documentation at http://{httpd.server_address[0]}:{httpd.server_address[1]}/index.html")
        httpd.serve_forever()


def test_pdoc():
    write_module_doc(module_names=["pkg", "pkg2"], output_dir=Path("../docs"))
    serve_module_doc(web_dir=Path(__file__).parent.parent / "docs")


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
