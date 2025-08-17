import pytest
from pathlib import Path
from unittest.mock import patch
from mini_git.commands.init import InitCommand


def test_init_command_initialization():
    """InitCommandが正しく初期化されることをテスト"""
    command = InitCommand()
    assert command is not None


def test_init_command_execute_default_path(tmp_path: Path, monkeypatch):
    """デフォルトパス（カレントディレクトリ）での実行をテスト"""
    monkeypatch.chdir(tmp_path)
    
    command = InitCommand()
    
    with patch('builtins.print') as mock_print:
        command.execute()
    
    # リポジトリ構造が作成されることを確認
    assert (tmp_path / ".git").is_dir()
    assert (tmp_path / ".git" / "objects").is_dir()
    assert (tmp_path / ".git" / "refs" / "heads").is_dir()
    
    # 成功メッセージが出力されることを確認
    mock_print.assert_called_once()
    call_args = mock_print.call_args[0][0]
    assert "Initialized empty Git repository" in call_args
    assert str(tmp_path / ".git") in call_args


def test_init_command_execute_custom_path(tmp_path: Path):
    """カスタムパスでの実行をテスト"""
    repo_path = tmp_path / "my_repo"
    
    command = InitCommand()
    
    with patch('builtins.print') as mock_print:
        command.execute(repo_path)
    
    # リポジトリ構造が作成されることを確認
    assert (repo_path / ".git").is_dir()
    assert (repo_path / ".git" / "objects").is_dir()
    assert (repo_path / ".git" / "refs" / "heads").is_dir()
    
    # 成功メッセージが出力されることを確認
    mock_print.assert_called_once()
    call_args = mock_print.call_args[0][0]
    assert "Initialized empty Git repository" in call_args
    assert str(repo_path / ".git") in call_args


def test_init_command_execute_custom_branch(tmp_path: Path):
    """カスタムブランチ名での実行をテスト"""
    command = InitCommand()
    
    with patch('builtins.print') as mock_print:
        command.execute(tmp_path, default_branch="develop")
    
    # リポジトリ構造が作成されることを確認
    assert (tmp_path / ".git").is_dir()
    assert (tmp_path / ".git" / "objects").is_dir()
    assert (tmp_path / ".git" / "refs" / "heads").is_dir()
    
    # 成功メッセージが出力されることを確認
    mock_print.assert_called_once()


def test_init_command_execute_existing_repo(tmp_path: Path):
    """既存のリポジトリに対する実行をテスト（冪等性）"""
    command = InitCommand()
    
    # 最初の実行
    with patch('builtins.print') as mock_print1:
        command.execute(tmp_path)
    
    # 2回目の実行（既存のリポジトリ）
    with patch('builtins.print') as mock_print2:
        command.execute(tmp_path)
    
    # 両方とも成功することを確認
    assert mock_print1.called
    assert mock_print2.called
    
    # リポジトリ構造が維持されることを確認
    assert (tmp_path / ".git").is_dir()
    assert (tmp_path / ".git" / "objects").is_dir()
    assert (tmp_path / ".git" / "refs" / "heads").is_dir()


def test_init_command_execute_creates_parent_directories(tmp_path: Path):
    """親ディレクトリが存在しない場合に作成されることをテスト"""
    deep_path = tmp_path / "a" / "b" / "c" / "repo"
    
    command = InitCommand()
    
    with patch('builtins.print'):
        command.execute(deep_path)
    
    # 深いパスでもリポジトリが作成されることを確認
    assert (deep_path / ".git").is_dir()
    assert (deep_path / ".git" / "objects").is_dir()
    assert (deep_path / ".git" / "refs" / "heads").is_dir()