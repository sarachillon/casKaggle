"""
data.py

Descarregar les dades des del dataset de Kaggle 'andrewmvd/data-analyst-jobs'
"""

import pandas as pd
import kagglehub
from pathlib import Path
import numpy as np
from config.log_config import *


def load_data():
    console.rule("[title]Descarrega de dades[/title]")

    # Descarregar des de KaggleHub
    path = kagglehub.dataset_download("andrewmvd/data-analyst-jobs")
    console.print(f"[info]Dataset descarregat en:[/info] {path}")

    csv_path = Path(path) / "DataAnalyst.csv"

    # Carregar el CSV amb pandas
    data = pd.read_csv(csv_path)

    console.print(f"[success]Dades carregades correctament:[/success] "
                  f"{data.shape[0]} files, {data.shape[1]} columnes.")
    return data




def data_description(data):
    """
    Muestra un resumen de los atributos del dataset indicando:
    - Tipo (numérico o no numérico)
    - Número de valores únicos
    - Número de valores nulos
    """
    console.rule("[title]Descripció de les dades[/title]")

    numeric_features = data.select_dtypes(np.number).keys()
    non_numeric = [k for k in data.keys() if k not in numeric_features]

    # Función auxiliar para crear tabla
    def print_table(cols, tipo):
        table = Table(title=f"{tipo}", show_lines=True)
        table.add_column("Atribut", style="cyan")
        table.add_column("Únics", style="green")
        table.add_column("Nulos", style="red")

        for col in cols:
            unique_count = data[col].nunique()
            null_count = data[col].isnull().sum()
            null_count += (data[col] == -1).sum()  # Considerar -1 como nulo
            null_count += (data[col] == "-1").sum()  # Considerar "-1" como nulo
            table.add_row(col, str(unique_count), str(null_count))

        console.print(table)

    # Imprimir tablas
    print_table(numeric_features, "Atributs numèrics")
    print_table(non_numeric, "Atributs no numèrics")


if __name__ == "__main__":
    df = load_data()
    data_description(df)
