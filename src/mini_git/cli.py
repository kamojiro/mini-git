import typer
from pathlib import Path

from mini_git.commands import AddCommand, InitCommand
from mini_git.core.git_repository import GitRepository

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello, {name}!")


@app.command()
def init():
    commnad = InitCommand()
    commnad.execute()


@app.command()
def add(path: Path):
    # TODO: enable directory path
    command = AddCommand()
    command.execute(path)


def main():
    app()


if __name__ == "__main__":
    main()
