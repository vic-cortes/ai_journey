import marimo

__generated_with = "0.11.17"
app = marimo.App(width="full")


@app.cell
def libraries():
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
    df = pl.read_csv(
        filename,
        separator="|",
    )
    return (df,)


@app.cell
def _(df):
    df.head()
    df.columns
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Busqueda

        Es importanre filtrar la información por entidad, y municipio. Es necesario hacer uso de los datos abiertos del INEGI
        """
    )
    return


if __name__ == "__main__":
    app.run()
