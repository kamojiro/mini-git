import pytest
from pathlib import Path
from mini_git.services.add_service import AddService
from mini_git.storage.object_store import ObjectStore


def test_add_service_initialization(tmp_path: Path):
    """AddServiceが正しく初期化されることをテスト"""
    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)
    service = AddService(object_store)

    assert service.object_store == object_store


def test_add_object_reads_file_and_stores_blob(tmp_path: Path):
    """ファイルを読み込んでblobオブジェクトとして保存することをテスト"""
    # テスト用ファイルを作成
    test_file = tmp_path / "test.txt"
    test_content = b"Hello, World!\n"
    test_file.write_bytes(test_content)

    # AddServiceでファイルを追加
    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)
    service = AddService(object_store)

    oid = service.add_object(test_file)

    # オブジェクトが正しく保存されることを確認
    assert isinstance(oid, str)
    assert len(oid) == 40  # SHA-1ハッシュの長さ

    # 保存されたオブジェクトを読み込んで確認
    obj_type, content = object_store.read(oid)
    assert obj_type == "blob"
    assert content == test_content


def test_add_object_returns_consistent_oid(tmp_path: Path):
    """同じ内容のファイルに対して一貫したOIDを返すことをテスト"""
    # 同じ内容のファイルを2つ作成
    test_file1 = tmp_path / "test1.txt"
    test_file2 = tmp_path / "test2.txt"
    test_content = b"Same content\n"
    test_file1.write_bytes(test_content)
    test_file2.write_bytes(test_content)

    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)
    service = AddService(object_store)

    oid1 = service.add_object(test_file1)
    oid2 = service.add_object(test_file2)

    # 同じ内容なので同じOIDが返される
    assert oid1 == oid2


def test_add_object_handles_empty_file(tmp_path: Path):
    """空ファイルの処理が正しく動作することをテスト"""
    # 空ファイルを作成
    empty_file = tmp_path / "empty.txt"
    empty_file.write_bytes(b"")

    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)
    service = AddService(object_store)

    oid = service.add_object(empty_file)

    # 空ファイルでも正しくOIDが生成される
    assert isinstance(oid, str)
    assert len(oid) == 40

    # 保存されたオブジェクトを確認
    obj_type, content = object_store.read(oid)
    assert obj_type == "blob"
    assert content == b""


def test_add_object_handles_binary_file(tmp_path: Path):
    """バイナリファイルの処理が正しく動作することをテスト"""
    # バイナリファイルを作成
    binary_file = tmp_path / "binary.dat"
    binary_content = bytes(range(256))  # 0-255のバイト列
    binary_file.write_bytes(binary_content)

    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)
    service = AddService(object_store)

    oid = service.add_object(binary_file)

    # バイナリファイルでも正しく処理される
    assert isinstance(oid, str)
    assert len(oid) == 40

    # 保存されたオブジェクトを確認
    obj_type, content = object_store.read(oid)
    assert obj_type == "blob"
    assert content == binary_content


def test_add_object_raises_when_file_not_found(tmp_path: Path):
    """存在しないファイルに対して例外を発生させることをテスト"""
    nonexistent_file = tmp_path / "nonexistent.txt"

    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)
    service = AddService(object_store)

    with pytest.raises(FileNotFoundError):
        service.add_object(nonexistent_file)


def test_add_object_handles_large_file(tmp_path: Path):
    """大きなファイルの処理が正しく動作することをテスト"""
    # 大きなファイルを作成（1MB）
    large_file = tmp_path / "large.txt"
    large_content = b"A" * (1024 * 1024)
    large_file.write_bytes(large_content)

    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)
    service = AddService(object_store)

    oid = service.add_object(large_file)

    # 大きなファイルでも正しく処理される
    assert isinstance(oid, str)
    assert len(oid) == 40

    # 保存されたオブジェクトを確認
    obj_type, content = object_store.read(oid)
    assert obj_type == "blob"
    assert content == large_content
