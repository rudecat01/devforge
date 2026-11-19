import sys
import tempfile
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools" / "productivity"))

from code_stats import analyze_directory, detect_language
from json_toolkit import flatten_json, unflatten_json, diff_json
from project_scaffolder import scaffold_project

def test_detect_language():
    assert detect_language(".py") == "Python"
    assert detect_language(".js") == "JavaScript"
    assert detect_language(".cpp") == "C++"
    assert detect_language(".xyz") == "Other"

def test_code_stats_analysis():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        code_file = tmp_path / "sample.py"
        code_file.write_text("# Comment\n\nx = 1\ny = 2\n")

        stats = analyze_directory(tmp_dir)
        assert "Python" in stats
        py_stat = stats["Python"]
        assert py_stat["files"] == 1
        assert py_stat["comment"] == 1
        assert py_stat["blank"] == 1
        assert py_stat["code"] == 2

def test_json_toolkit_flatten_unflatten():
    nested = {
        "server": {
            "port": 8080,
            "host": "localhost"
        },
        "enabled": True
    }
    flat = flatten_json(nested)
    assert flat["server.port"] == 8080
    assert flat["server.host"] == "localhost"
    assert flat["enabled"] is True

    restored = unflatten_json(flat)
    assert restored == nested

def test_json_toolkit_diff():
    a = {"name": "app", "version": "1.0", "active": True}
    b = {"name": "app", "version": "1.1", "debug": True}
    res = diff_json(a, b)
    assert res["identical"] is False
    assert "debug" in res["added"]
    assert "active" in res["removed"]
    assert "version" in res["changed"]

def test_project_scaffolder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest = scaffold_project("my_cli", "python", tmp_dir)
        assert dest.exists()
        assert (dest / "main.py").exists()
        assert (dest / "test_main.py").exists()
        assert (dest / "README.md").exists()
