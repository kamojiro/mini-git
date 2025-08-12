import typer
from pathlib import Path

from mini_git.commands import AddCommand
from mini_git.core.git_repository import GitRepository

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello, {name}!")


@app.command()
def init(path: Path = Path.cwd()):
    git_dir = path / ".git"
    object_dir = git_dir / "objects"
    if git_dir.is_dir():
        print(f"Repository already initialized at {git_dir}")
    else:
        git_dir.mkdir(parents=True, exist_ok=True)
        object_dir.mkdir(parents=True, exist_ok=True)
        print(f"Initialized empty Git repository in {git_dir}")


@app.command()
def add(path: Path):
    # TODO: enable directory path
    git_repository = GitRepository()
    command = AddCommand(git_repository=git_repository)
    command.execute(path)


def main():
    app()


if __name__ == "__main__":
    main()
