import http.server
import os
import socketserver
import sys
from pathlib import Path
from typing import Iterator, List, Tuple

from docstring_parser import parse
from pdoc import Module


# pdoc.tpl_lookup


def module_list(module_names: List[str]) -> List[Tuple[str, str]]:
    modules = (Module(module=name) for name in module_names)
    return [(mod.name, mod.docstring) for mod in modules]


def recursive_modules(module: Module) -> Iterator[Module]:
    yield module
    for sub_module in module.submodules():
        yield from recursive_modules(module=sub_module)


# def docfilter(doc: pdoc.Doc) -> bool:
#     return True


def write_html_file(path: Path, module: Module, **kwargs) -> None:
    with open(str(path), "w", encoding="utf-8") as file:
        file.write(module.html(show_source_code=False, **kwargs))  # external_links=True


def serve_pdoc(host: str = "localhost", port: int = 8000, web_dir: Path = "."):
    os.chdir(str(web_dir))
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((host, port), handler)
    print(f"documentation served at http://{host}:{port}/index.html")
    sys.stdout.flush()
    httpd.serve_forever()


def make_pdoc(module_names: List[str], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_html_file(path=output_dir / "index.html", module=Module("."), modules=module_list(module_names))

    for name in module_names:
        for module in recursive_modules(module=Module(module=name)):
            module_parts = module.name.split(".")
            if module.is_package:
                output_dir_ = output_dir / "/".join(module_parts)
                output_dir_.mkdir(parents=True, exist_ok=True)
                file_path = output_dir_ / "index.html"
            else:
                file_path = output_dir / "/".join(module_parts[:-1]) / (module_parts[-1] + ".html")
            write_html_file(path=file_path, module=module)


def test_pdoc():
    make_pdoc(module_names=["pkg", "pkg2"], output_dir=Path("../docs"))
    # serve_pdoc(web_dir=Path(__file__).parent.parent / "docs")


def test_parse_alias_from_google_doc_string():
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
    pass
