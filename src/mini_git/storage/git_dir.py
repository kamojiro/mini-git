from pathlib import Path


class GitDir:
    def __init__(self, worktree: Path, git_path: Path):
        self.worktree = worktree
        self.git_path = git_path

    @classmethod
    def discover(cls, start: Path | None = None) -> "GitDir":
        cur = (start or Path.cwd()).resolve()
        while True:
            git = cur / ".git"
            if git.is_dir():
                return cls(cur, git)
            if cur == cur.parent:
                break
            cur = cur.parent
        raise FileNotFoundError("No .git directory found.")

    @classmethod
    def ensure_layout(cls, path: Path) -> "GitDir":
        wt = path.resolve()
        git = wt / ".git"
        (git / "objects").mkdir(parents=True, exist_ok=True)
        (git / "refs" / "heads").mkdir(parents=True, exist_ok=True)
        return cls(wt, git)
