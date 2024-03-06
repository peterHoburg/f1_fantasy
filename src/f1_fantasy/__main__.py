import shutil
import time
from pathlib import Path

import typer

from f1_fantasy.consts import CURRENT_DIR, ROOT_DIR
from f1_fantasy.main import main

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
def update_prices():
    current_price_drivers = Path(CURRENT_DIR / "data" / "input" / "price_drivers.csv")
    new_price_drivers = Path(ROOT_DIR / "data" / "input" / "price_drivers.csv")
    shutil.copy(new_price_drivers, current_price_drivers)

    current_price_constructors = Path(CURRENT_DIR / "data" / "input" / "price_constructors.csv")
    new_price_constructors = Path(ROOT_DIR / "data" / "input" / "price_constructors.csv")
    shutil.copy(new_price_constructors, current_price_constructors)


@app.command()
def run():
    if Path(CURRENT_DIR / "data" / "input" / "price_drivers.csv").exists() is False:
        typer.echo("No input data found. Run setup command first: f1-fantasy setup")
        return

    main(
        chips_path=Path(CURRENT_DIR / "data" / "input" / "chips.csv"),
        finishing_positions_qualifying_path=Path(CURRENT_DIR / "data" / "input" / "finishing_positions_qualifying.csv"),
        finishing_positions_race_path=Path(CURRENT_DIR / "data" / "input" / "finishing_positions_race.csv"),
        ignore_constructors_path=Path(CURRENT_DIR / "data" / "input" / "ignore_constructors.csv"),
        ignore_drivers_path=Path(CURRENT_DIR / "data" / "input" / "ignore_drivers.csv"),
        price_constructors_path=Path(CURRENT_DIR / "data" / "input" / "price_constructors.csv"),
        price_drivers_path=Path(CURRENT_DIR / "data" / "input" / "price_drivers.csv"),
        special_points_path=Path(CURRENT_DIR / "data" / "input" / "special_points.csv"),
        output_file_path=Path(CURRENT_DIR / "data" / "output" / f"{time.time()}"),
        current_team_csv=Path(CURRENT_DIR / "data" / "input" / "current_team.csv"),
    )


def version_callback(value: bool):
    import pkg_resources

    my_version = pkg_resources.get_distribution("f1-fantasy").version
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
