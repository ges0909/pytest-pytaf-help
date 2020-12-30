import os
from pathlib import Path
from typing import Iterator, List, Tuple

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


def get_docstrings(module_names: List[str]) -> List[Tuple[str, str]]:
    """returns a list of tuple consisting of the module name and its docstring from __init__.py"""
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


def write_doc(module_names: List[str], output_dir: Path) -> None:
    # create root index file
    output_dir.mkdir(parents=True, exist_ok=True)
    write_file(path=output_dir / "index", module=Module("."), modules=get_docstrings(module_names))
    # create package index and module documentaion files recursivly
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


def serve_doc(web_dir: Path):
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            pass

    try:
        os.chdir(str(web_dir))
        with TCPServer(server_address=("localhost", 0), RequestHandlerClass=QuietHandler) as httpd:
            print(f"see documentation at http://{httpd.server_address[0]}:{httpd.server_address[1]}/index.html")
            print(f"press ^C to abort")
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
