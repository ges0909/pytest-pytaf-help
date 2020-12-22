from pathlib import Path
from typing import Iterator, List

import pdoc


# pdoc.tpl_lookup


def recursive_modules(module: pdoc.Module) -> Iterator[pdoc.Module]:
    yield module
    for sub_module in module.submodules():
        yield from recursive_modules(module=sub_module)


# def docfilter(doc: pdoc.Doc) -> bool:
#     return True


def make_pdoc(module_names: List[str], output_dir: Path) -> None:
    root_modules_ = (pdoc.Module(module=name) for name in module_names)
    root_modules = ((m.name, m.docstring) for m in root_modules_)
    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = output_dir / "index.html"
    with open(str(file_name), "w", encoding="utf-8") as file:
        file.write(pdoc.Module(module=".").html(show_source_code=False, modules=root_modules))

    for module_name in module_names:
        for module in recursive_modules(module=pdoc.Module(module=module_name)):
            module_parts = module.name.split(".")
            if module.is_package:
                output_dir_ = output_dir / "/".join(module_parts)
                output_dir_.mkdir(parents=True, exist_ok=True)
                file_name_ = output_dir_ / "index.html"
            else:
                file_name_ = output_dir / "/".join(module_parts[:-1]) / (module_parts[-1] + ".html")
            with open(str(file_name_), "w", encoding="utf-8") as file:
                file.write(module.html(show_source_code=False, external_links=True))

    # webbrowser.open(url="file://../docs/index.html")


def test_pdoc():
    make_pdoc(module_names=["pkg", "pkg2"], output_dir=Path("../docs"))
