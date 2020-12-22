from pathlib import Path
from typing import Iterator, List, Tuple

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

    # webbrowser.open(url="file://../docs/index.html")


def test_pdoc():
    make_pdoc(module_names=["pkg", "pkg2"], output_dir=Path("../docs"))
