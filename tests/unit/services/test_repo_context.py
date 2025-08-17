import pytest
from pathlib import Path
from mini_git.services.repo_context import RepoContext
from mini_git.storage.git_dir import GitDir


def test_repo_context_initialization(tmp_path: Path):
    """RepoContextが正しく初期化されることをテスト"""
    worktree = tmp_path / "repo"
    git_path = worktree / ".git"

    repo = RepoContext(worktree, git_path)

    assert repo.worktree == worktree
    assert repo.git_path == git_path
    assert repo.object_store is not None


def test_require_repo_with_valid_repo(tmp_path: Path):
    """有効なリポジトリでrequire_repoが正しく動作することをテスト"""
    # リポジトリ構造を作成
    GitDir.ensure_layout(tmp_path)

    repo = RepoContext.require_repo(tmp_path)

    assert repo.worktree == tmp_path.resolve()
    assert repo.git_path == tmp_path / ".git"
    assert (repo.git_path / "objects").is_dir()


def test_require_repo_discovers_from_subdirectory(tmp_path: Path, monkeypatch):
    """サブディレクトリからリポジトリを発見できることをテスト"""
    # ルートにリポジトリを作成
    GitDir.ensure_layout(tmp_path)

    # サブディレクトリを作成
    subdir = tmp_path / "subdir"
    subdir.mkdir()

    repo = RepoContext.require_repo(subdir)

    assert repo.worktree == tmp_path.resolve()
    assert repo.git_path == tmp_path / ".git"


def test_require_repo_raises_when_no_git_found(tmp_path: Path):
    """gitディレクトリが見つからない場合に例外を発生させることをテスト"""
    with pytest.raises(FileNotFoundError):
        RepoContext.require_repo(tmp_path)


def test_require_repo_raises_when_objects_missing(tmp_path: Path):
    """objectsディレクトリが欠けている場合に例外を発生させることをテスト"""
    # .gitディレクトリのみ作成（objectsディレクトリなし）
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    with pytest.raises(RuntimeError, match="Corrupt repo: missing"):
        RepoContext.require_repo(tmp_path)


def test_open_or_init_repo_creates_new_repo(tmp_path: Path):
    """新しいリポジトリの作成が正しく動作することをテスト"""
    repo = RepoContext.open_or_init_repo(tmp_path)

    assert repo.worktree == tmp_path.resolve()
    assert repo.git_path == tmp_path / ".git"
    assert (repo.git_path / "objects").is_dir()
    assert (repo.git_path / "refs" / "heads").is_dir()


def test_open_or_init_repo_opens_existing_repo(tmp_path: Path):
    """既存のリポジトリを開くことが正しく動作することをテスト"""
    # 最初にリポジトリを作成
    repo1 = RepoContext.open_or_init_repo(tmp_path)

    # 同じパスで再度開く
    repo2 = RepoContext.open_or_init_repo(tmp_path)

    assert repo1.worktree == repo2.worktree
    assert repo1.git_path == repo2.git_path


def test_open_or_init_repo_with_custom_branch(tmp_path: Path):
    """カスタムブランチ名でリポジトリを作成できることをテスト"""
    repo = RepoContext.open_or_init_repo(tmp_path, default_branch="develop")

    # 基本構造が作成されることを確認
    assert repo.worktree == tmp_path.resolve()
    assert repo.git_path == tmp_path / ".git"
    assert (repo.git_path / "objects").is_dir()
    assert (repo.git_path / "refs" / "heads").is_dir()


def test_require_repo_without_start_uses_cwd(tmp_path: Path, monkeypatch):
    """start引数なしでカレントディレクトリを使用することをテスト"""
    # リポジトリを作成
    GitDir.ensure_layout(tmp_path)

    # カレントディレクトリを変更
    monkeypatch.chdir(tmp_path)

    repo = RepoContext.require_repo()

    assert repo.worktree == tmp_path.resolve()
    assert repo.git_path == tmp_path / ".git"
