from typer.testing import CliRunner
from src.main import app

runner = CliRunner()


def test_cli_sort_bubble() -> None:
    result = runner.invoke(app, ["sort", "bubble", "[3, 1, 2]"])
    assert result.exit_code == 0
    assert "[1, 2, 3]" in result.stdout


def test_cli_sort_bucket_float() -> None:
    result = runner.invoke(app, ["sort", "bucket", "[0.2, 0.1, 0.9, 0.4]", "--buckets", "5"])
    assert result.exit_code == 0
    assert "[0.1, 0.2, 0.4, 0.9]" in result.stdout


def test_cli_math_fibo_iter() -> None:
    result = runner.invoke(app, ["math", "fibo", "10", "iter"])
    assert result.exit_code == 0
    assert "55" in result.stdout


def test_cli_sort_counting_non_int_fails() -> None:
    result = runner.invoke(app, ["sort", "counting", "[1.0, 2.0]"])
    assert result.exit_code != 0
    assert "counting_sort работает только с целыми числами" in result.output
