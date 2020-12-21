from pathlib import Path
from typing import Iterator, List

import pdoc


# pdoc.tpl_lookup


def find_modules(module: pdoc.Module) -> Iterator[pdoc.Module]:
    yield module
    for sub_module in module.submodules():
        yield from find_modules(module=sub_module)


# def docfilter(doc: pdoc.Doc) -> bool:
#     return True


def make_pdoc(module_names: List[str], output_dir: Path):
    # context = pdoc.Context()
    # pdoc.link_inheritance(context)

    for module_name in module_names:
        module = pdoc.Module(module=module_name)  # context=context, docfilter=docfilter

        for module in find_modules(module=module):
            module_parts = module.name.split(".")
            if module.is_package:
                output_dir_ = output_dir / "/".join(module_parts)
                output_dir_.mkdir(parents=True, exist_ok=True)
                file_name_ = output_dir_ / "index.html"
            else:
                file_name_ = output_dir / "/".join(module_parts[:-1]) / (module_parts[-1] + ".html")
            with open(str(file_name_), "w", encoding="utf-8") as file:
                file.write(module.html(show_source_code=False))


def test_pdoc():
    make_pdoc(module_names=["pkg", "pkg2"], output_dir=Path("../docs"))
