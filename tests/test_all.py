from pathlib import Path

from f1_fantasy.consts import ROOT_DIR
from f1_fantasy.main import run


def test_run():
    test_data_root = Path("/Users/peterhoburg/Documents/projects/f1_fantasy") / "tests" / "test_data" / "min_price_perfect_score"
    run(test_data_root)

    root, parents, files = next((test_data_root / "data" / "output").walk())
    output_file = root / files[0]
    with open(output_file) as f:
        run_output = f.read()
    output_file.unlink()

    with (test_data_root / "expected_output").open("r") as f:
        expected_output = f.read()

    assert run_output == expected_output
