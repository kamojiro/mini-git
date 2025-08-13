from pathlib import Path


def get_git_repository_path():
    current_path = Path.cwd()
    while current_path != current_path.parent:
        git_path = current_path / ".git"
        if git_path.is_dir():
            return git_path
        current_path = current_path.parent
    raise FileNotFoundError(
        "No .git directory found in the current path or its parents."
    )


class GitRepository:
    def __init__(self):
        self.git_path = get_git_repository_path()

    @classmethod
    def init(cls, path: Path = Path.cwd()):
        git_dir = path / ".git"
        object_dir = git_dir / "objects"
        if git_dir.is_dir():
            print(f"Repository already initialized at {git_dir}")
        else:
            git_dir.mkdir(parents=True, exist_ok=True)
            object_dir.mkdir(parents=True, exist_ok=True)
            print(f"Initialized empty Git repository in {git_dir}")
        return cls()

