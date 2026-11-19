import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools" / "python"))

from file_organizer import determine_category, organize_directory
from duplicate_finder import find_duplicates

def test_determine_category():
    assert determine_category(".png") == "images"
    assert determine_category(".pdf") == "documents"
    assert determine_category(".py") == "code"
    assert determine_category(".json") == "data"
    assert determine_category(".unknownext") == "other"

def test_file_organizer_workflow():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        (tmp_path / "test.png").write_text("dummy image")
        (tmp_path / "notes.txt").write_text("some notes")
        (tmp_path / "script.py").write_text("print(1)")

        # Dry run first
        dry_actions = organize_directory(tmp_dir, dry_run=True)
        assert len(dry_actions) == 3
        # Ensure files didn't move
        assert (tmp_path / "test.png").exists()

        # Actual execution
        real_actions = organize_directory(tmp_dir, dry_run=False)
        assert len(real_actions) == 3
        assert (tmp_path / "images" / "test.png").exists()
        assert (tmp_path / "documents" / "notes.txt").exists()
        assert (tmp_path / "code" / "script.py").exists()

def test_duplicate_finder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        content_a = "Unique content Alpha"
        content_dup = "Duplicate content Beta"

        (tmp_path / "file1.txt").write_text(content_dup)
        (tmp_path / "file2.txt").write_text(content_dup)
        (tmp_path / "file3.txt").write_text(content_a)

        dups = find_duplicates(tmp_dir)
        assert len(dups) == 1
        dup_paths = list(dups.values())[0]
        assert len(dup_paths) == 2
        names = {Path(p).name for p in dup_paths}
        assert names == {"file1.txt", "file2.txt"}
