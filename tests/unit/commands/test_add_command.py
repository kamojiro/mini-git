import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from mini_git.commands.add import AddCommand
from mini_git.services.repo_context import RepoContext
from mini_git.storage.git_dir import GitDir


def test_add_command_initialization():
    """AddCommandが正しく初期化されることをテスト"""
    command = AddCommand()
    assert command is not None


def test_add_command_execute_no_path():
    """パスが指定されていない場合の処理をテスト"""
    command = AddCommand()
    
    with patch('builtins.print') as mock_print:
        command.execute(None)
    
    mock_print.assert_called_with("No files specified to add.")


def test_add_command_execute_empty_path():
    """空のパスが指定された場合の処理をテスト"""
    command = AddCommand()
    
    with patch('builtins.print') as mock_print:
        command.execute("")
    
    mock_print.assert_called_with("No files specified to add.")


def test_add_command_execute_valid_file(tmp_path: Path):
    """有効なファイルでの実行をテスト"""
    # リポジトリを初期化
    GitDir.ensure_layout(tmp_path)
    
    # テストファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    
    command = AddCommand()
    
    with patch('builtins.print') as mock_print:
        command.execute(test_file)
    
    # "Add Command"メッセージが出力されることを確認
    mock_print.assert_called_with("Add Command")
    
    # オブジェクトが作成されることを確認
    objects_dir = tmp_path / ".git" / "objects"
    object_files = list(objects_dir.rglob("*"))
    # ディレクトリ以外のファイルが存在することを確認
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) > 0


def test_add_command_execute_file_not_in_repo(tmp_path: Path):
    """リポジトリ外のファイルに対する実行をテスト"""
    # リポジトリを作成しない
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    
    command = AddCommand()
    
    with patch('builtins.print') as mock_print:
        with pytest.raises(FileNotFoundError):
            command.execute(test_file)


def test_add_command_execute_nonexistent_file(tmp_path: Path):
    """存在しないファイルに対する実行をテスト"""
    # リポジトリを初期化
    GitDir.ensure_layout(tmp_path)
    
    nonexistent_file = tmp_path / "nonexistent.txt"
    
    command = AddCommand()
    
    with patch('builtins.print') as mock_print:
        with pytest.raises(FileNotFoundError):
            command.execute(nonexistent_file)


def test_add_command_execute_from_subdirectory(tmp_path: Path):
    """サブディレクトリからの実行をテスト"""
    # リポジトリを初期化
    GitDir.ensure_layout(tmp_path)
    
    # サブディレクトリとファイルを作成
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file = subdir / "test.txt"
    test_file.write_text("Hello from subdir!")
    
    command = AddCommand()
    
    with patch('builtins.print') as mock_print:
        command.execute(test_file)
    
    # "Add Command"メッセージが出力されることを確認
    mock_print.assert_called_with("Add Command")
    
    # オブジェクトが作成されることを確認
    objects_dir = tmp_path / ".git" / "objects"
    object_files = list(objects_dir.rglob("*"))
    object_files = [f for f in object_files if f.is_file()]
    assert len(object_files) > 0


@patch('mini_git.commands.add.RepoContext')
@patch('mini_git.commands.add.AddService')
def test_add_command_execute_service_integration(mock_add_service_class, mock_repo_context_class, tmp_path: Path):
    """サービス層との統合をテスト"""
    # モックの設定
    mock_repo_context = MagicMock()
    mock_object_store = MagicMock()
    mock_repo_context.object_store = mock_object_store
    mock_repo_context_class.require_repo.return_value = mock_repo_context
    
    mock_add_service = MagicMock()
    mock_add_service.add_object.return_value = "abc123"
    mock_add_service_class.return_value = mock_add_service
    
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    
    command = AddCommand()
    
    with patch('builtins.print'):
        command.execute(test_file)
    
    # RepoContextが正しく呼ばれることを確認（ファイルの親ディレクトリが渡される）
    mock_repo_context_class.require_repo.assert_called_once_with(test_file.parent)
    
    # AddServiceが正しく初期化されることを確認
    mock_add_service_class.assert_called_once_with(mock_object_store)
    
    # add_objectが正しく呼ばれることを確認
    mock_add_service.add_object.assert_called_once_with(test_file)