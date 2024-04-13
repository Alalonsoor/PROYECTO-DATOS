import pandas as pd
import getData


def main():
    # Procesar datos del mercado de transferencias
    api_url = "http://localhost:8000"
    la_liga_id = "ES1"
    df_transfer = getData.get_transfer_data(api_url, la_liga_id)
    df_transfer.to_csv("TransferMarket_completo.csv")
    print(df_transfer)


if __name__ == "__main__":
    main()
