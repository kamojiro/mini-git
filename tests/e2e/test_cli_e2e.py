"""E2E tests for mgit CLI - testing the full command line interface"""

import subprocess
from pathlib import Path


def run_mgit_command(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run mgit command and return the result"""
    cmd = ["uv", "run", "mgit"] + args
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def test_mgit_help_command():
    """mgit --help コマンドのテスト"""
    result = run_mgit_command(["--help"], Path.cwd())

    assert result.returncode == 0
    assert "hello" in result.stdout
    assert "init" in result.stdout
    assert "add" in result.stdout


def test_mgit_hello_command():
    """mgit hello コマンドのテスト"""
    result = run_mgit_command(["hello", "World"], Path.cwd())

    assert result.returncode == 0
    assert "Hello, World!" in result.stdout


def test_mgit_init_command(tmp_path: Path):
    """mgit init コマンドのテスト"""
    result = run_mgit_command(["init"], tmp_path)

    assert result.returncode == 0
    assert "Initialized empty Git repository" in result.stdout

    # リポジトリ構造が作成されることを確認
    assert (tmp_path / ".git").is_dir()
    assert (tmp_path / ".git" / "objects").is_dir()
    assert (tmp_path / ".git" / "refs" / "heads").is_dir()


def test_mgit_add_command_success(tmp_path: Path):
    """mgit add コマンドの成功ケースのテスト"""
    # まずリポジトリを初期化
    init_result = run_mgit_command(["init"], tmp_path)
    assert init_result.returncode == 0

    # テストファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    # ファイルを追加
    add_result = run_mgit_command(["add", str(test_file)], tmp_path)

    assert add_result.returncode == 0
    assert "Add Command" in add_result.stdout

    # オブジェクトが作成されることを確認
    objects_dir = tmp_path / ".git" / "objects"
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) > 0


def test_mgit_add_command_nonexistent_file(tmp_path: Path):
    """存在しないファイルに対するmgit add コマンドのテスト"""
    # まずリポジトリを初期化
    init_result = run_mgit_command(["init"], tmp_path)
    assert init_result.returncode == 0

    # 存在しないファイルを追加しようとする
    add_result = run_mgit_command(["add", "nonexistent.txt"], tmp_path)

    # エラーで終了することを確認
    assert add_result.returncode != 0


def test_mgit_add_command_no_repo(tmp_path: Path):
    """リポジトリが初期化されていない状態でのmgit add コマンドのテスト"""
    # テストファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    # リポジトリを初期化せずにファイルを追加しようとする
    add_result = run_mgit_command(["add", str(test_file)], tmp_path)

    # エラーで終了することを確認
    assert add_result.returncode != 0


def test_mgit_workflow_init_and_add(tmp_path: Path):
    """mgit init -> add の完全なワークフローのテスト"""
    # 1. リポジトリを初期化
    init_result = run_mgit_command(["init"], tmp_path)
    assert init_result.returncode == 0
    assert "Initialized empty Git repository" in init_result.stdout

    # 2. 複数のファイルを作成
    files_to_add = ["file1.txt", "file2.txt", "file3.txt"]
    for filename in files_to_add:
        (tmp_path / filename).write_text(f"Content of {filename}")

    # 3. 各ファイルを追加
    for filename in files_to_add:
        add_result = run_mgit_command(["add", filename], tmp_path)
        assert add_result.returncode == 0
        assert "Add Command" in add_result.stdout

    # 4. 全てのオブジェクトが作成されることを確認
    objects_dir = tmp_path / ".git" / "objects"
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) == len(files_to_add)


def test_mgit_add_relative_path(tmp_path: Path):
    """相対パスでのmgit add コマンドのテスト"""
    # まずリポジトリを初期化
    init_result = run_mgit_command(["init"], tmp_path)
    assert init_result.returncode == 0

    # サブディレクトリとファイルを作成
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file = subdir / "test.txt"
    test_file.write_text("Hello from subdir!")

    # 相対パスでファイルを追加
    add_result = run_mgit_command(["add", "subdir/test.txt"], tmp_path)

    assert add_result.returncode == 0
    assert "Add Command" in add_result.stdout

    # オブジェクトが作成されることを確認
    objects_dir = tmp_path / ".git" / "objects"
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) > 0


def test_mgit_add_absolute_path(tmp_path: Path):
    """絶対パスでのmgit add コマンドのテスト"""
    # まずリポジトリを初期化
    init_result = run_mgit_command(["init"], tmp_path)
    assert init_result.returncode == 0

    # テストファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    # 絶対パスでファイルを追加
    add_result = run_mgit_command(["add", str(test_file.absolute())], tmp_path)

    assert add_result.returncode == 0
    assert "Add Command" in add_result.stdout

    # オブジェクトが作成されることを確認
    objects_dir = tmp_path / ".git" / "objects"
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) > 0
