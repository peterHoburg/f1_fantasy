import shutil
from pathlib import Path

import typer
from f1_fantasy.main import main
from f1_fantasy.consts import ROOT_DIR

app = typer.Typer()


@app.command()
def setup():
    current_dir = Path(".") / "data"
    typer.echo(f"Copying data to {current_dir}")
    shutil.copytree(ROOT_DIR / "data", current_dir)


@app.command()
def run():
    main()



if __name__ == "__main__":
    app()
