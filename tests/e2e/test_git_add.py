import pytest
from pathlib import Path
from mini_git.commands.init import InitCommand
from mini_git.commands.add import AddCommand
from mini_git.services.repo_context import RepoContext


def test_git_add_workflow_single_file(tmp_path: Path, monkeypatch):
    """単一ファイルのgit addワークフローをテスト"""
    monkeypatch.chdir(tmp_path)
    
    # 1. リポジトリを初期化
    init_command = InitCommand()
    init_command.execute()
    
    # 2. テストファイルを作成
    test_file = tmp_path / "hello.txt"
    test_content = "Hello, World!\n"
    test_file.write_text(test_content)
    
    # 3. ファイルを追加
    add_command = AddCommand()
    add_command.execute(test_file)
    
    # 4. オブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo()
    objects_dir = repo.git_path / "objects"
    
    # オブジェクトファイルが存在することを確認
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) == 1
    
    # オブジェクトの内容を確認
    obj_file = object_files[0]
    oid = obj_file.parent.name + obj_file.name
    obj_type, content = repo.object_store.read(oid)
    
    assert obj_type == "blob"
    assert content.decode() == test_content


def test_git_add_workflow_multiple_files(tmp_path: Path, monkeypatch):
    """複数ファイルのgit addワークフローをテスト"""
    monkeypatch.chdir(tmp_path)
    
    # 1. リポジトリを初期化
    init_command = InitCommand()
    init_command.execute()
    
    # 2. 複数のテストファイルを作成
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
    
    # 3. 各ファイルを追加
    add_command = AddCommand()
    for file_path, _ in created_files:
        add_command.execute(file_path)
    
    # 4. 全てのオブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo()
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


def test_git_add_workflow_same_content_deduplication(tmp_path: Path, monkeypatch):
    """同じ内容のファイルが重複排除されることをテスト"""
    monkeypatch.chdir(tmp_path)
    
    # 1. リポジトリを初期化
    init_command = InitCommand()
    init_command.execute()
    
    # 2. 同じ内容の複数ファイルを作成
    same_content = "Same content\n"
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text(same_content)
    file2.write_text(same_content)
    
    # 3. 両方のファイルを追加
    add_command = AddCommand()
    add_command.execute(file1)
    add_command.execute(file2)
    
    # 4. オブジェクトが1つだけ作成されることを確認（重複排除）
    repo = RepoContext.require_repo()
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


def test_git_add_workflow_binary_file(tmp_path: Path, monkeypatch):
    """バイナリファイルのgit addワークフローをテスト"""
    monkeypatch.chdir(tmp_path)
    
    # 1. リポジトリを初期化
    init_command = InitCommand()
    init_command.execute()
    
    # 2. バイナリファイルを作成
    binary_file = tmp_path / "binary.dat"
    binary_content = bytes(range(256))
    binary_file.write_bytes(binary_content)
    
    # 3. バイナリファイルを追加
    add_command = AddCommand()
    add_command.execute(binary_file)
    
    # 4. オブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo()
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


def test_git_add_workflow_empty_file(tmp_path: Path, monkeypatch):
    """空ファイルのgit addワークフローをテスト"""
    monkeypatch.chdir(tmp_path)
    
    # 1. リポジトリを初期化
    init_command = InitCommand()
    init_command.execute()
    
    # 2. 空ファイルを作成
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    
    # 3. 空ファイルを追加
    add_command = AddCommand()
    add_command.execute(empty_file)
    
    # 4. オブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo()
    objects_dir = repo.git_path / "objects"
    
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) == 1
    
    # オブジェクトの内容を確認
    obj_file = object_files[0]
    oid = obj_file.parent.name + obj_file.name
    obj_type, content = repo.object_store.read(oid)
    
    assert obj_type == "blob"
    assert content == b""


def test_git_add_workflow_subdirectory_file(tmp_path: Path, monkeypatch):
    """サブディレクトリ内のファイルのgit addワークフローをテスト"""
    monkeypatch.chdir(tmp_path)
    
    # 1. リポジトリを初期化
    init_command = InitCommand()
    init_command.execute()
    
    # 2. サブディレクトリとファイルを作成
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file = subdir / "test.txt"
    test_content = "File in subdirectory\n"
    test_file.write_text(test_content)
    
    # 3. サブディレクトリのファイルを追加
    add_command = AddCommand()
    add_command.execute(test_file)
    
    # 4. オブジェクトが正しく保存されていることを確認
    repo = RepoContext.require_repo()
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