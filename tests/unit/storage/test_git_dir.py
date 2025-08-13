from pathlib import Path
import pytest
from mini_git.storage.git_dir import GitDir  # 推奨配置


# -------- ensure_layout のテスト --------


def test_ensure_layout_creates_minimal_structure(tmp_path: Path):
    gd = GitDir.ensure_layout(tmp_path)

    # 返り値の一貫性
    assert gd.worktree == tmp_path.resolve()
    assert gd.git_path == tmp_path.resolve() / ".git"

    # .git 配下の最小構造
    assert (gd.git_path / "objects").is_dir()
    assert (gd.git_path / "refs" / "heads").is_dir()
    # HEAD は RepoContext 側で作る想定のため、ここでは必須にしない


def test_ensure_layout_is_idempotent(tmp_path: Path):
    gd1 = GitDir.ensure_layout(tmp_path)
    gd2 = GitDir.ensure_layout(tmp_path)  # 2回目でも例外なく動く
    assert gd1.git_path == gd2.git_path
    assert (gd2.git_path / "objects").is_dir()
    assert (gd2.git_path / "refs" / "heads").is_dir()


# -------- discover のテスト --------


def test_discover_returns_git_dir_when_in_root(tmp_path: Path, monkeypatch):
    # ルートに .git（最小構造）を作る
    GitDir.ensure_layout(tmp_path)
    monkeypatch.chdir(tmp_path)

    gd = GitDir.discover()
    assert gd.git_path == tmp_path / ".git"
    assert gd.worktree == tmp_path.resolve()


def test_discover_returns_git_dir_when_in_subdir(tmp_path: Path, monkeypatch):
    # ルートに .git（最小構造）を作る
    GitDir.ensure_layout(tmp_path)

    # サブディレクトリから探索
    sub = tmp_path / "a" / "b" / "c"
    sub.mkdir(parents=True)
    monkeypatch.chdir(sub)

    gd = GitDir.discover()
    assert gd.git_path == tmp_path / ".git"
    assert gd.worktree == tmp_path.resolve()


def test_discover_prefers_nearest_git_dir(tmp_path: Path, monkeypatch):
    # ルートにも .git、ネスト先にも .git を用意（近い方を返すべき）
    GitDir.ensure_layout(tmp_path)
    nested = tmp_path / "nested"
    nested.mkdir()
    GitDir.ensure_layout(nested)

    monkeypatch.chdir(nested)
    gd = GitDir.discover()
    assert gd.git_path == nested / ".git"
    assert gd.worktree == nested.resolve()


def test_discover_raises_when_no_git_found(tmp_path: Path, monkeypatch):
    # .git がどこにもない
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError) as exc:
        GitDir.discover()
    assert "No .git directory" in str(exc.value)


def test_discover_with_explicit_start_argument(tmp_path: Path):
    # start 引数が CWD に依存せず優先されること
    GitDir.ensure_layout(tmp_path)
    gd = GitDir.discover(
        start=tmp_path / "x" / "y" / "z"
    )  # まだ存在しない下層を指定してもOK
    assert gd.git_path == tmp_path / ".git"
    assert gd.worktree == tmp_path.resolve()
