from pathlib import Path


def test_repo_metadata_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "CITATION.cff").exists()
    assert (root / "notebooks" / "quickstart_prism.ipynb").exists()
    assert (root / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").exists()
    assert (root / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").exists()
