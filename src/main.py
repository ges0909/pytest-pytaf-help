from pathlib import Path

from src.pytaf_pdoc import write_doc, serve_doc

if __name__ == "__main__":
    write_doc(module_names=["pkg", "pkg2"], output_dir=Path("../docs"))
    serve_doc(web_dir=Path(__file__).parent.parent / "docs")
