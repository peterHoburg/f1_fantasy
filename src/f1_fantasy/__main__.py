import shutil
import time
from datetime import datetime
from pathlib import Path

import typer

from f1_fantasy.consts import ROOT_DIR, CURRENT_DIR
from f1_fantasy.main import drivers_prices_from_csv, constructors_prices_from_csv, finishing_positions_from_csv, \
    special_points_from_csv, set_chips_from_csv, calculations, main

app = typer.Typer()


@app.command()
def setup():
    data_dir = Path() / "data"
    typer.echo(f"Copying data to {data_dir}")
    if data_dir.exists():
        delete = typer.confirm("Data directory already exists. Do you want to overwrite it? (y/n)")
        if not delete:
            typer.echo("Aborting setup")
            raise typer.Abort()
        shutil.rmtree(data_dir)
    shutil.copytree(ROOT_DIR / "data", data_dir)


@app.command()
def run():
    if Path(CURRENT_DIR / "data" / "input" / "price_drivers.csv").exists() is False:
        typer.echo("No input data found. Run setup command first: f1-fantasy setup")
        return

    main(
        drivers_price_csv=Path(CURRENT_DIR / "data" / "input" / "price_drivers.csv"),
        constructors_price_csv=Path(CURRENT_DIR / "data" / "input" / "price_constructors.csv"),
        qualifying_finishing_positions=Path(CURRENT_DIR / "data" / "input" / "finishing_positions_qualifying.csv"),
        racing_finishing_positions= Path(CURRENT_DIR / "data" / "input" / "finishing_positions_race.csv"),
        special_points=Path(CURRENT_DIR / "data" / "input" / "special_points.csv"),
        chips=Path(CURRENT_DIR / "data" / "input" / "chips.csv"),
        output_file=Path(CURRENT_DIR / "data" / "output" / f"{datetime.utcnow()}"),
        ignore_constructors=Path(CURRENT_DIR / "data" / "input" / "ignore_constructors.csv"),
        ignore_drivers=Path(CURRENT_DIR / "data" / "input" / "ignore_drivers.csv"),
    )




def version_callback(value: bool):
    import pkg_resources

    my_version = pkg_resources.get_distribution('f1-fantasy').version
    if value:
        typer.echo(f"{my_version}")
        raise typer.Exit()


@app.callback()
def cli(
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
):
    return


if __name__ == "__main__":
    app()
