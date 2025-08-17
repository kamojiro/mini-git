import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from mini_git.commands.add import AddCommand


def test_add_command_initialization():
    """AddCommandが正しく初期化されることをテスト"""
    command = AddCommand()
    assert command is not None


def test_add_command_execute_no_path(mocker: MockerFixture):
    """パスが指定されていない場合の処理をテスト"""
    command = AddCommand()
    mock_print = mocker.patch("builtins.print")

    command.execute(None)

    mock_print.assert_called_with("No files specified to add.")


def test_add_command_execute_empty_path(mocker: MockerFixture):
    """空のパスが指定された場合の処理をテスト"""
    command = AddCommand()
    mock_print = mocker.patch("builtins.print")

    command.execute("")

    mock_print.assert_called_with("No files specified to add.")


def test_add_command_execute_valid_file(mocker: MockerFixture, tmp_path: Path):
    """有効なファイルでの実行をテスト"""
    # テストファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    # モックの設定
    mock_repo_context_class = mocker.patch("mini_git.commands.add.RepoContext")
    mock_add_service_class = mocker.patch("mini_git.commands.add.AddService")
    mock_print = mocker.patch("builtins.print")

    mock_repo_context = mocker.MagicMock()
    mock_object_store = mocker.MagicMock()
    mock_repo_context.object_store = mock_object_store
    mock_repo_context_class.require_repo.return_value = mock_repo_context

    mock_add_service = mocker.MagicMock()
    mock_add_service.add_object.return_value = "abc123"
    mock_add_service_class.return_value = mock_add_service

    command = AddCommand()
    command.execute(test_file)

    # "Add Command"メッセージが出力されることを確認
    mock_print.assert_called_with("Add Command")

    # RepoContextが正しく呼ばれることを確認
    mock_repo_context_class.require_repo.assert_called_once_with(test_file.parent)

    # AddServiceが正しく初期化されることを確認
    mock_add_service_class.assert_called_once_with(mock_object_store)

    # add_objectが正しく呼ばれることを確認
    mock_add_service.add_object.assert_called_once_with(test_file)


def test_add_command_execute_file_not_in_repo(mocker: MockerFixture, tmp_path: Path):
    """リポジトリ外のファイルに対する実行をテスト"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    # RepoContext.require_repoがFileNotFoundErrorを発生させるようにモック
    mock_repo_context_class = mocker.patch("mini_git.commands.add.RepoContext")
    mock_repo_context_class.require_repo.side_effect = FileNotFoundError(
        "Not a git repository"
    )

    command = AddCommand()

    with pytest.raises(FileNotFoundError):
        command.execute(test_file)


def test_add_command_execute_nonexistent_file(mocker: MockerFixture, tmp_path: Path):
    """存在しないファイルに対する実行をテスト"""
    nonexistent_file = tmp_path / "nonexistent.txt"

    # モックの設定
    mock_repo_context_class = mocker.patch("mini_git.commands.add.RepoContext")
    mock_add_service_class = mocker.patch("mini_git.commands.add.AddService")

    mock_repo_context = mocker.MagicMock()
    mock_object_store = mocker.MagicMock()
    mock_repo_context.object_store = mock_object_store
    mock_repo_context_class.require_repo.return_value = mock_repo_context

    mock_add_service = mocker.MagicMock()
    mock_add_service.add_object.side_effect = FileNotFoundError("File not found")
    mock_add_service_class.return_value = mock_add_service

    command = AddCommand()

    with pytest.raises(FileNotFoundError):
        command.execute(nonexistent_file)


def test_add_command_execute_from_subdirectory(mocker: MockerFixture, tmp_path: Path):
    """サブディレクトリからの実行をテスト"""
    # サブディレクトリとファイルを作成
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file = subdir / "test.txt"
    test_file.write_text("Hello from subdir!")

    # モックの設定
    mock_repo_context_class = mocker.patch("mini_git.commands.add.RepoContext")
    mock_add_service_class = mocker.patch("mini_git.commands.add.AddService")
    mock_print = mocker.patch("builtins.print")

    mock_repo_context = mocker.MagicMock()
    mock_object_store = mocker.MagicMock()
    mock_repo_context.object_store = mock_object_store
    mock_repo_context_class.require_repo.return_value = mock_repo_context

    mock_add_service = mocker.MagicMock()
    mock_add_service.add_object.return_value = "def456"
    mock_add_service_class.return_value = mock_add_service

    command = AddCommand()
    command.execute(test_file)

    # "Add Command"メッセージが出力されることを確認
    mock_print.assert_called_with("Add Command")

    # RepoContextが正しく呼ばれることを確認（ファイルの親ディレクトリが渡される）
    mock_repo_context_class.require_repo.assert_called_once_with(test_file.parent)

    # AddServiceが正しく初期化されることを確認
    mock_add_service_class.assert_called_once_with(mock_object_store)

    # add_objectが正しく呼ばれることを確認
    mock_add_service.add_object.assert_called_once_with(test_file)
