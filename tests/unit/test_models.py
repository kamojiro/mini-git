import pytest
from pathlib import Path
from mini_git.models import IndexEntry


def test_index_entry_creation():
    """IndexEntryが正しく作成されることをテスト"""
    entry = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")

    assert entry.path == Path("test.txt")
    assert entry.mode == 100644
    assert entry.oid == "abc123"


def test_index_entry_immutable():
    """IndexEntryがimmutableであることをテスト"""
    entry = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")

    with pytest.raises(Exception):  # pydantic frozen model
        entry.path = Path("other.txt")


def test_index_entry_equality():
    """IndexEntryの等価性テスト"""
    entry1 = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")
    entry2 = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")
    entry3 = IndexEntry(path=Path("test.txt"), mode=100644, oid="def456")

    assert entry1 == entry2
    assert entry1 != entry3
