"""Integration tests for add workflow - testing multiple components working together"""

from pathlib import Path
from mini_git.commands.init import InitCommand
from mini_git.commands.add import AddCommand
from mini_git.services.repo_context import RepoContext
from mini_git.storage.object_store import ObjectStore
from mini_git.services.add_service import AddService


def test_add_service_with_object_store_integration(tmp_path: Path):
    """AddServiceとObjectStoreの統合テスト"""
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


def test_add_command_with_services_integration(tmp_path: Path):
    """AddCommandとサービス層の統合テスト"""
    # リポジトリを初期化
    init_command = InitCommand()
    init_command.execute(tmp_path)

    # テストファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    # AddCommandでファイルを追加
    add_command = AddCommand()
    add_command.execute(test_file)

    # オブジェクトが作成されることを確認
    repo = RepoContext.require_repo(tmp_path)
    objects_dir = repo.git_path / "objects"
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) > 0


def test_multiple_files_add_integration(tmp_path: Path):
    """複数ファイルの追加統合テスト"""
    # リポジトリを初期化
    init_command = InitCommand()
    init_command.execute(tmp_path)

    # 複数のテストファイルを作成
    files_and_contents = [
        ("file1.txt", "Content of file 1\n"),
        ("file2.txt", "Content of file 2\n"),
        ("file3.txt", "Content of file 3\n"),
    ]

    created_files = []
    for filename, content in files_and_contents:
        file_path = tmp_path / filename
        file_path.write_text(content)
        created_files.append((file_path, content))

    # 各ファイルを追加
    add_command = AddCommand()
    for file_path, _ in created_files:
        add_command.execute(file_path)

    # 全てのオブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo(tmp_path)
    objects_dir = repo.git_path / "objects"

    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) == len(created_files)

    # 各オブジェクトの内容を確認
    stored_contents = set()
    for obj_file in object_files:
        oid = obj_file.parent.name + obj_file.name
        obj_type, content = repo.object_store.read(oid)
        assert obj_type == "blob"
        stored_contents.add(content.decode())

    expected_contents = {content for _, content in files_and_contents}
    assert stored_contents == expected_contents


def test_same_content_deduplication_integration(tmp_path: Path):
    """同じ内容のファイルが重複排除される統合テスト"""
    # リポジトリを初期化
    init_command = InitCommand()
    init_command.execute(tmp_path)

    # 同じ内容の複数ファイルを作成
    same_content = "Same content\n"
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text(same_content)
    file2.write_text(same_content)

    # 両方のファイルを追加
    add_command = AddCommand()
    add_command.execute(file1)
    add_command.execute(file2)

    # オブジェクトが1つだけ作成されることを確認（重複排除）
    repo = RepoContext.require_repo(tmp_path)
    objects_dir = repo.git_path / "objects"

    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) == 1

    # オブジェクトの内容を確認
    obj_file = object_files[0]
    oid = obj_file.parent.name + obj_file.name
    obj_type, content = repo.object_store.read(oid)

    assert obj_type == "blob"
    assert content.decode() == same_content


def test_binary_file_integration(tmp_path: Path):
    """バイナリファイルの統合テスト"""
    # リポジトリを初期化
    init_command = InitCommand()
    init_command.execute(tmp_path)

    # バイナリファイルを作成
    binary_file = tmp_path / "binary.dat"
    binary_content = bytes(range(256))
    binary_file.write_bytes(binary_content)

    # バイナリファイルを追加
    add_command = AddCommand()
    add_command.execute(binary_file)

    # オブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo(tmp_path)
    objects_dir = repo.git_path / "objects"

    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) == 1

    # オブジェクトの内容を確認
    obj_file = object_files[0]
    oid = obj_file.parent.name + obj_file.name
    obj_type, content = repo.object_store.read(oid)

    assert obj_type == "blob"
    assert content == binary_content


def test_subdirectory_file_integration(tmp_path: Path):
    """サブディレクトリ内のファイルの統合テスト"""
    # リポジトリを初期化
    init_command = InitCommand()
    init_command.execute(tmp_path)

    # サブディレクトリとファイルを作成
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file = subdir / "test.txt"
    test_content = "File in subdirectory\n"
    test_file.write_text(test_content)

    # サブディレクトリのファイルを追加
    add_command = AddCommand()
    add_command.execute(test_file)

    # オブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo(tmp_path)
    objects_dir = repo.git_path / "objects"

    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) == 1

    # オブジェクトの内容を確認
    obj_file = object_files[0]
    oid = obj_file.parent.name + obj_file.name
    obj_type, content = repo.object_store.read(oid)

    assert obj_type == "blob"
    assert content.decode() == test_content
