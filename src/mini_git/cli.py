import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello, {name}!")


def main():
    app()


# def entrypoint():
#     typer.run(main)

if __name__ == "__main__":
    main()
