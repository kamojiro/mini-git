from mini_git.services import RepoContext
from pathlib import Path


class InitCommand:
    def __init__(self):
        pass

    def execute(self, path: Path = None, default_branch: str = "main"):
        if path is None:
            path = Path.cwd()
        repo_context = RepoContext.open_or_init_repo(path, default_branch)
        print(f"Initialized empty Git repository in {repo_context.git_path}")
