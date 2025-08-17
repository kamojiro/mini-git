from pathlib import Path
from mini_git.storage.index_store import IndexStore
from mini_git.models import IndexEntry


def test_index_store_initialization(tmp_path: Path):
    """IndexStoreが正しく初期化されることをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    assert store.git_dir == git_dir
    assert store.index_path == git_dir / "index.json"


def test_add_or_update_creates_entry(tmp_path: Path):
    """エントリの追加・更新が正しく動作することをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    entry = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")
    store.add_or_update(entry)

    # インデックスファイルが作成されることを確認
    assert store.index_path.exists()

    # エントリが正しく保存されることを確認
    entries = list(store.all())
    assert len(entries) == 1
    assert entries[0] == entry


def test_add_or_update_overwrites_existing(tmp_path: Path):
    """既存エントリの上書きが正しく動作することをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    # 最初のエントリを追加
    entry1 = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")
    store.add_or_update(entry1)

    # 同じパスで異なるOIDのエントリを追加（上書き）
    entry2 = IndexEntry(path=Path("test.txt"), mode=100644, oid="def456")
    store.add_or_update(entry2)

    entries = list(store.all())
    assert len(entries) == 1
    assert entries[0].oid == "def456"


def test_remove_existing_entry(tmp_path: Path):
    """エントリの削除が正しく動作することをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    # エントリを追加
    entry = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")
    store.add_or_update(entry)

    # エントリを削除
    store.remove("test.txt")

    entries = list(store.all())
    assert len(entries) == 0


def test_remove_nonexistent_entry(tmp_path: Path):
    """存在しないエントリの削除が例外を発生させないことをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    # 存在しないエントリを削除（例外が発生しないことを確認）
    store.remove("nonexistent.txt")

    entries = list(store.all())
    assert len(entries) == 0


def test_clear_removes_all_entries(tmp_path: Path):
    """全エントリのクリアが正しく動作することをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    # 複数のエントリを追加
    entry1 = IndexEntry(path=Path("test1.txt"), mode=100644, oid="abc123")
    entry2 = IndexEntry(path=Path("test2.txt"), mode=100644, oid="def456")
    store.add_or_update(entry1)
    store.add_or_update(entry2)

    # クリア
    store.clear()

    entries = list(store.all())
    assert len(entries) == 0


def test_all_returns_empty_for_nonexistent_index(tmp_path: Path):
    """インデックスファイルが存在しない場合に空のリストを返すことをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    entries = list(store.all())
    assert len(entries) == 0


def test_multiple_entries_handling(tmp_path: Path):
    """複数エントリの処理が正しく動作することをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    # 複数のエントリを追加
    entries_to_add = [
        IndexEntry(path=Path("file1.txt"), mode=100644, oid="abc123"),
        IndexEntry(path=Path("file2.txt"), mode=100755, oid="def456"),
        IndexEntry(path=Path("dir/file3.txt"), mode=100644, oid="ghi789"),
    ]

    for entry in entries_to_add:
        store.add_or_update(entry)

    # 全エントリを取得して確認
    stored_entries = list(store.all())
    assert len(stored_entries) == 3

    # パスでソートして比較
    stored_entries.sort(key=lambda e: str(e.path))
    entries_to_add.sort(key=lambda e: str(e.path))

    for stored, expected in zip(stored_entries, entries_to_add):
        assert stored == expected


def test_atomic_updates(tmp_path: Path):
    """原子的更新が正しく動作することをテスト"""
    git_dir = tmp_path / ".git"
    store = IndexStore(git_dir)

    # エントリを追加
    entry = IndexEntry(path=Path("test.txt"), mode=100644, oid="abc123")
    store.add_or_update(entry)

    # 一時ファイルが残っていないことを確認
    tmp_files = list(git_dir.glob("*.tmp"))
    assert len(tmp_files) == 0

    # インデックスファイルが存在することを確認
    assert store.index_path.exists()
