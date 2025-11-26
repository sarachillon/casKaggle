from data.data import load_data
from src.eda import eda
from src.preprocessing import preprocessing

def main():
    # Carregar dades
    df = load_data()
    print(df.info())
    eda(df)

    # Netejar dades
    

if __name__ == "__main__":
    main()
