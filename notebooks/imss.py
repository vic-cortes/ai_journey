import marimo

__generated_with = "0.11.17"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    import polars as pl
    return Path, pl


@app.cell
def _(Path):
    # Use Path to get the data folder
    DATA_FOLDER = Path.cwd() / "data"
    filename = DATA_FOLDER / "asg-2025-02-28.csv"
    return DATA_FOLDER, filename


@app.cell
def _(filename, pl):
    df = pl.read_csv(filename, separator="|")
    return (df,)


if __name__ == "__main__":
    app.run()
