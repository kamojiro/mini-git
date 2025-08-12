# test_repository_path.py
from pathlib import Path
import pytest

from mini_git.core.git_repository import get_git_repository_path


def test_returns_git_dir_when_in_root(tmp_path: Path, monkeypatch):
    # .git ディレクトリを作る
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    # CWD を tmp_path に切り替える
    monkeypatch.chdir(tmp_path)

    result = get_git_repository_path()
    assert result == git_dir
    assert result.is_dir()


def test_returns_git_dir_when_in_subdir(tmp_path: Path, monkeypatch):
    # .git はルートに作る
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    # サブディレクトリを作ってそこから探索させる
    sub_dir = tmp_path / "a" / "b" / "c"
    sub_dir.mkdir(parents=True)
    monkeypatch.chdir(sub_dir)

    result = get_git_repository_path()
    assert result == git_dir


def test_raises_when_no_git_found(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # .git がない状態
    with pytest.raises(FileNotFoundError) as exc_info:
        get_git_repository_path()
    assert ".git" in str(exc_info.value)


def test_stops_at_filesystem_root(tmp_path: Path, monkeypatch):
    # 疑似的に root 直下に移動し、.git なし
    # （ここでは tmp_path 自体が root として扱われる想定）
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        get_git_repository_path()


def test_prefers_nearest_git_dir(tmp_path: Path, monkeypatch):
    # ルートとその下に別々の .git を用意
    root_git = tmp_path / ".git"
    root_git.mkdir()
    sub_dir = tmp_path / "nested"
    sub_dir.mkdir()
    sub_git = sub_dir / ".git"
    sub_git.mkdir()

    # サブディレクトリから呼び出した場合、sub_git を返すはず
    monkeypatch.chdir(sub_dir)
    result = get_git_repository_path()
    assert result == sub_git
