from pathlib import Path
from mini_git.storage import ObjectStore, GitDir


class RepoContext:
    worktree: Path
    git_path: Path
    object_store: ObjectStore
    # refs

    def __init__(self, worktree: Path, git_path: Path) -> None:
        self.worktree = worktree
        self.git_path = git_path
        self.object_store = ObjectStore(git_path)

    @classmethod
    def require_repo(cls, start: Path | None = None) -> "RepoContext":
        git_dir = GitDir.discover(start)
        object_dir = git_dir.git_path / "objects"
        if not object_dir.is_dir():
            raise RuntimeError(f"Corrupt repo: missing {object_dir}")
        return cls(git_dir.worktree, git_dir.git_path)

    @classmethod
    def open_or_init_repo(
        cls, path: Path, default_branch: str = "main"
    ) -> "RepoContext":
        git_dir = GitDir.ensure_layout(path)
        # head = git_dir.git_path / "HEAD"
        # if not head.exists():
        #     head.write_text(f"ref: refs/heads/{default_branch}\n", encoding="utf-8")
        return cls(
            worktree=git_dir.worktree,
            git_path=git_dir.git_path,
            # refs=RefStore(gd.git_path),
        )
