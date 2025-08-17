import pytest
from pathlib import Path
from typer.testing import CliRunner
from mini_git.cli import app


def test_cli_hello_command():
    """hello コマンドのテスト"""
    runner = CliRunner()
    result = runner.invoke(app, ["hello", "World"])
    
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout


def test_cli_init_command(tmp_path: Path):
    """init コマンドのテスト"""
    runner = CliRunner()
    
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["init"])
        
        assert result.exit_code == 0
        assert "Initialized empty Git repository" in result.stdout
        
        # リポジトリ構造が作成されることを確認
        assert Path(".git").is_dir()
        assert Path(".git/objects").is_dir()
        assert Path(".git/refs/heads").is_dir()


def test_cli_add_command(tmp_path: Path):
    """add コマンドのテスト"""
    runner = CliRunner()
    
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # まずリポジトリを初期化
        init_result = runner.invoke(app, ["init"])
        assert init_result.exit_code == 0
        
        # テストファイルを作成
        test_file = Path("test.txt")
        test_file.write_text("Hello, World!")
        
        # ファイルを追加
        add_result = runner.invoke(app, ["add", str(test_file)])
        
        assert add_result.exit_code == 0
        assert "Add Command" in add_result.stdout
        
        # オブジェクトが作成されることを確認
        objects_dir = Path(".git/objects")
        object_files = list(objects_dir.rglob("*"))
        object_files = [f for f in object_files if f.is_file()]
        assert len(object_files) > 0


def test_cli_add_command_nonexistent_file(tmp_path: Path):
    """存在しないファイルに対するadd コマンドのテスト"""
    runner = CliRunner()
    
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # まずリポジトリを初期化
        init_result = runner.invoke(app, ["init"])
        assert init_result.exit_code == 0
        
        # 存在しないファイルを追加しようとする
        add_result = runner.invoke(app, ["add", "nonexistent.txt"])
        
        # エラーで終了することを確認
        assert add_result.exit_code != 0


def test_cli_add_command_no_repo(tmp_path: Path):
    """リポジトリが初期化されていない状態でのadd コマンドのテスト"""
    runner = CliRunner()
    
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # テストファイルを作成
        test_file = Path("test.txt")
        test_file.write_text("Hello, World!")
        
        # リポジトリを初期化せずにファイルを追加しようとする
        add_result = runner.invoke(app, ["add", str(test_file)])
        
        # エラーで終了することを確認
        assert add_result.exit_code != 0


def test_cli_workflow_init_and_add(tmp_path: Path):
    """init -> add の完全なワークフローのテスト"""
    runner = CliRunner()
    
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # 1. リポジトリを初期化
        init_result = runner.invoke(app, ["init"])
        assert init_result.exit_code == 0
        assert "Initialized empty Git repository" in init_result.stdout
        
        # 2. 複数のファイルを作成
        files_to_add = ["file1.txt", "file2.txt", "file3.txt"]
        for filename in files_to_add:
            Path(filename).write_text(f"Content of {filename}")
        
        # 3. 各ファイルを追加
        for filename in files_to_add:
            add_result = runner.invoke(app, ["add", filename])
            assert add_result.exit_code == 0
            assert "Add Command" in add_result.stdout
        
        # 4. 全てのオブジェクトが作成されることを確認
        objects_dir = Path(".git/objects")
        object_files = list(objects_dir.rglob("*"))
        object_files = [f for f in object_files if f.is_file()]
        assert len(object_files) == len(files_to_add)


def test_cli_help_commands():
    """ヘルプコマンドのテスト"""
    runner = CliRunner()
    
    # メインのヘルプ
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "hello" in result.stdout
    assert "init" in result.stdout
    assert "add" in result.stdout
    
    # 個別コマンドのヘルプ
    hello_help = runner.invoke(app, ["hello", "--help"])
    assert hello_help.exit_code == 0
    
    init_help = runner.invoke(app, ["init", "--help"])
    assert init_help.exit_code == 0
    
    add_help = runner.invoke(app, ["add", "--help"])
    assert add_help.exit_code == 0