import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from mini_git.services.add_service import AddService
from mini_git.storage.object_store import ObjectStore
from mini_git.types import ObjectType


def test_add_service_initialization(mocker: MockerFixture):
    """AddServiceが正しく初期化されることをテスト"""
    mock_object_store = mocker.Mock(spec=ObjectStore)
    service = AddService(mock_object_store)

    assert service.object_store == mock_object_store


def test_add_object_reads_file_and_stores_blob(mocker: MockerFixture, tmp_path: Path):
    """ファイルを読み込んでblobオブジェクトとして保存することをテスト"""
    # テスト用ファイルを作成
    test_file = tmp_path / "test.txt"
    test_content = b"Hello, World!\n"
    test_file.write_bytes(test_content)

    # AddServiceでファイルを追加
    object_store = mocker.Mock(spec=ObjectStore)
    mock_object_store_write = mocker.patch.object(
        object_store, "write", return_value="1234567890abcdef1234567890abcdef12345678"
    )
    service = AddService(object_store)

    oid = service.add_object(test_file)

    # オブジェクトが正しく保存されることを確認
    assert isinstance(oid, str)
    assert len(oid) == 40  # SHA-1ハッシュの長さ
    mock_object_store_write.assert_called_once_with(ObjectType.BLOB, test_content)


def test_add_object_returns_consistent_oid(mocker: MockerFixture, tmp_path: Path):
    """同じ内容のファイルに対して一貫したOIDを返すことをテスト"""
    # 同じ内容のファイルを2つ作成
    test_file1 = tmp_path / "test1.txt"
    test_file2 = tmp_path / "test2.txt"
    test_content = b"Same content\n"
    test_file1.write_bytes(test_content)
    test_file2.write_bytes(test_content)

    object_store = mocker.Mock(spec=ObjectStore)
    expected_oid = "abcdef1234567890abcdef1234567890abcdef12"
    mock_object_store_write = mocker.patch.object(
        object_store, "write", return_value=expected_oid
    )
    service = AddService(object_store)

    oid1 = service.add_object(test_file1)
    oid2 = service.add_object(test_file2)

    # 同じ内容なので同じOIDが返される
    assert oid1 == expected_oid
    assert oid2 == expected_oid
    assert mock_object_store_write.call_count == 2
    # 両方とも同じ内容で呼ばれることを確認
    for call in mock_object_store_write.call_args_list:
        assert call == mocker.call(ObjectType.BLOB, test_content)


def test_add_object_handles_empty_file(mocker: MockerFixture, tmp_path: Path):
    """空ファイルの処理が正しく動作することをテスト"""
    # 空ファイルを作成
    empty_file = tmp_path / "empty.txt"
    empty_file.write_bytes(b"")

    object_store = mocker.Mock(spec=ObjectStore)
    expected_oid = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
    mock_object_store_write = mocker.patch.object(
        object_store, "write", return_value=expected_oid
    )
    service = AddService(object_store)

    oid = service.add_object(empty_file)

    # 空ファイルでも正しくOIDが生成される
    assert isinstance(oid, str)
    assert len(oid) == 40
    assert oid == expected_oid
    mock_object_store_write.assert_called_once_with(ObjectType.BLOB, b"")


def test_add_object_handles_binary_file(mocker: MockerFixture, tmp_path: Path):
    """バイナリファイルの処理が正しく動作することをテスト"""
    # バイナリファイルを作成
    binary_file = tmp_path / "binary.dat"
    binary_content = bytes(range(256))  # 0-255のバイト列
    binary_file.write_bytes(binary_content)

    object_store = mocker.Mock(spec=ObjectStore)
    expected_oid = "abcdef1234567890abcdef1234567890abcdef12"
    mock_object_store_write = mocker.patch.object(
        object_store, "write", return_value=expected_oid
    )
    service = AddService(object_store)

    oid = service.add_object(binary_file)

    # バイナリファイルでも正しく処理される
    assert isinstance(oid, str)
    assert len(oid) == 40
    assert oid == expected_oid
    mock_object_store_write.assert_called_once_with(ObjectType.BLOB, binary_content)


def test_add_object_raises_when_file_not_found(mocker: MockerFixture, tmp_path: Path):
    """存在しないファイルに対して例外を発生させることをテスト"""
    nonexistent_file = tmp_path / "nonexistent.txt"

    object_store = mocker.Mock(spec=ObjectStore)
    service = AddService(object_store)

    with pytest.raises(FileNotFoundError):
        service.add_object(nonexistent_file)

    # object_store.writeが呼ばれないことを確認
    object_store.write.assert_not_called()


def test_add_object_handles_large_file(mocker: MockerFixture, tmp_path: Path):
    """大きなファイルの処理が正しく動作することをテスト"""
    # 大きなファイルを作成（1MB）
    large_file = tmp_path / "large.txt"
    large_content = b"A" * (1024 * 1024)
    large_file.write_bytes(large_content)

    object_store = mocker.Mock(spec=ObjectStore)
    expected_oid = "fedcba0987654321fedcba0987654321fedcba09"
    mock_object_store_write = mocker.patch.object(
        object_store, "write", return_value=expected_oid
    )
    service = AddService(object_store)

    oid = service.add_object(large_file)

    # 大きなファイルでも正しく処理される
    assert isinstance(oid, str)
    assert len(oid) == 40
    assert oid == expected_oid
    mock_object_store_write.assert_called_once_with(ObjectType.BLOB, large_content)
