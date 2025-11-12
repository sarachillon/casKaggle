import pandas as pd


def clean_data(df):
    df = df.dropna(subset=["Salary Estimate"])
    df["Company Name"] = df["Company Name"].str.replace("\n", "")
    return df

