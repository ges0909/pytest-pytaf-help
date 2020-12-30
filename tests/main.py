from pathlib import Path

from tests.test_pdoc import write_module_doc, serve_module_doc

if __name__ == "__main__":
    write_module_doc(module_names=["pkg", "pkg2"], output_dir=Path("../docs"))
    serve_module_doc(web_dir=Path(__file__).parent.parent / "docs")
