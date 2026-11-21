import sys
from pathlib import Path

# Add project root and tools to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools" / "git"))

from commit_formatter import validate_commit_message, format_commit_message

def test_validate_commit_message_valid():
    valid, msg = validate_commit_message("feat(auth): add jwt authentication token support")
    assert valid is True

def test_validate_commit_message_uppercase_start():
    valid, msg = validate_commit_message("feat: Add jwt token")
    assert valid is False
    assert "start with a lowercase" in msg

def test_validate_commit_message_trailing_period():
    valid, msg = validate_commit_message("fix: resolve null pointer exception.")
    assert valid is False
    assert "not end with a period" in msg

def test_validate_commit_message_unknown_type():
    valid, msg = validate_commit_message("random: unknown type")
    assert valid is False
    assert "Unknown commit type" in msg

def test_format_commit_message():
    formatted = format_commit_message(
        commit_type="feat",
        description="Support multi-tenant configs",
        scope="core",
        breaking=True,
        body="Detailed description of changes",
        footer="Closes #42"
    )
    assert formatted.startswith("feat(core)!: support multi-tenant configs")
    assert "BREAKING CHANGE:" in formatted
    assert "Detailed description" in formatted
    assert "Closes #42" in formatted

def test_multiline_footer_support():
    msg = 'chore(ci): update release matrix\n\nSigned-off-by: DevForge Bot'
    valid, _ = validate_commit_message(msg)
    assert valid is True
