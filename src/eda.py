"""
eda.py

Funcions per anàlisi exploratori visual del dataset Data Analyst Jobs.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from config.log_config import console
from data.data import load_data


def plot_column_distribution(df: pd.DataFrame, cols: list = None, max_per_page: int = 2):
    """
    Genera gràfics de barres per a variables categòriques/discretes i histogrames per a variables contínues
    de les columnes seleccionades del DataFrame.

    Args:
        df (pd.DataFrame): Conjunt de dades.
        cols (list, optional): Llista de columnes a graficar. Si és None, s'utilitzen totes.
        ncols (int): Nombre de columnes de subgràfics.
    """
    if cols is None:
        cols = df.columns.tolist()

    # Filtrar columnas que realmente existen
    cols = [c for c in cols if c in df.columns]

    total_cols = len(cols)
    pages = (total_cols + max_per_page - 1) // max_per_page

    for page in range(pages):
        start_idx = page * max_per_page
        end_idx = min(start_idx + max_per_page, total_cols)
        page_cols = cols[start_idx:end_idx]

        fig, axes = plt.subplots(len(page_cols), 1, figsize=(10, 5 * len(page_cols)))
        if len(page_cols) == 1:
            axes = [axes]  # Asegurar lista para iterar

        for ax, col in zip(axes, page_cols):
            if df[col].dtype == "object" or df[col].nunique() < 10:
                # Categórica o discreta → barras
                df[col].value_counts().plot(kind="bar", ax=ax, color="skyblue", edgecolor="black")
                ax.set_ylabel("Número")
            else:
                # Numérica continua → histograma
                df[col].plot(kind="hist", ax=ax, bins=20, color="salmon", edgecolor="black")
                ax.set_ylabel("Frecuencia")
            ax.set_title(f"Distribución de {col} (únicos: {df[col].nunique()}, nulos: {df[col].isnull().sum()})")
            ax.set_xlabel(col)

        plt.tight_layout()
        
        # Guardar figura
        file_path = Path("outputs/eda") / f"eda_page_{page+1}.png"
        fig.savefig(file_path, dpi=300)
        console.print(f"[info]Figura guardada en:[/info] {file_path}")

        # Mostrar figura
        #plt.show()


def plot_eda(df: pd.DataFrame):
    """
    Funció principal per fer l'EDA complet
    """
    console.rule("[title]Anàlisi exploratori visual[/title]")

    # Atributs per veure en histogrames
    cols = ["Rating", "Founded", "Salary Estimate", "Size", "Type of ownership", "Industry", "Sector", "Revenue", "Easy Apply"]

    plot_column_distribution(df, cols=cols, max_per_page=2)
    console.print("[success]EDA complet.[/success]")

if __name__ == "__main__":
    df = load_data()
    plot_eda(df)

