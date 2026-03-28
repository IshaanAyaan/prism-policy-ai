from pathlib import Path


FORBIDDEN_TERMS = ["isef", "azsef", "judge", "school fair", "poster"]


def test_public_docs_strip_science_fair_language():
    root = Path(__file__).resolve().parents[1]
    targets = [root / "README.md", *sorted((root / "docs").glob("*.md"))]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in targets)
    for term in FORBIDDEN_TERMS:
        assert term not in text
