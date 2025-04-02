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
    DATABASE_FOLDER = Path.cwd() / "database.db"
    filename = DATA_FOLDER / "asg-2025-02-28.csv"
    return DATABASE_FOLDER, DATA_FOLDER, filename


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
    ", ".join([el for el in df.columns])
    return


@app.cell
def _(df):
    df["cve_municipio"].unique().sort()
    return


@app.cell
def _(df):
    # Filter bt cve_delegacion == 5 and cve_subdelegacion == 17
    df_mva = df.filter(
        (df["cve_delegacion"] == 5) & (df["cve_subdelegacion"] == 17)
    )
    return (df_mva,)


@app.cell
def _(DATABASE_FOLDER):
    import sqlite3


    conn = sqlite3.connect(DATABASE_FOLDER)
    return conn, sqlite3


@app.cell
def _(conn, df_mva):
    # Convert the polars DataFrame to a pandas DataFrame
    # Since polars does not support writing to sqlite
    df_mva_pandas = df_mva.to_pandas()
    df_mva_pandas.to_sql("asegurados", conn, if_exists="replace", index=False)
    return (df_mva_pandas,)


@app.cell
def _(df_mva):
    df_mva
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
