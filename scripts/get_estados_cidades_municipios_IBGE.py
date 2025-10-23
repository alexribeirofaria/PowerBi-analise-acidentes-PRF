import pandas as pd
from io import BytesIO
import gdown

ROWS_PRINT = 5
URL_ESTADOS_IBGE = 'https://drive.google.com/uc?id=1PGHfXCKvylSXDWZXznVQjdhDY22hLaTQ'
pd.set_option("display.max_rows", None)

baixar_tabelas = lambda url: (
    lambda arquivo: pd.read_excel(arquivo, sheet_name=None)
)(
    (lambda b: (b.seek(0), b)[1])(
        (lambda buff: (gdown.download(url, buff, quiet=True), buff)[1])(BytesIO())
    )
)

remover_colunas = lambda df: df.drop(
    columns=[c for c in ["id", "id_grade", "geocodigo"] if c in df.columns], inplace=True
) or df

get_estados = lambda tabelas: tabelas.get("estados")
get_municipios = lambda tabelas: tabelas.get("municipios")
get_cidades  = lambda tabelas: tabelas.get("cidades")

transformar_siglas_em_maiusculas = lambda df: df.assign(
    sigla=df["sigla"].str.upper() if "sigla" in df.columns else None
) if df is not None else None

def imprimir_data_frame(df, mostrar_todas=False):
    if mostrar_todas:
        print(df)
    else:
        print(df.head(ROWS_PRINT))

def main():
    tabelas = baixar_tabelas(URL_ESTADOS_IBGE)
    estados = get_estados(tabelas)
    estados = remover_colunas(estados)
    estados = transformar_siglas_em_maiusculas(estados)
    imprimir_data_frame(estados, "Estados")
    
    municipios = get_municipios(tabelas)
    imprimir_data_frame(municipios, "Municípios")
    cidades = get_cidades(tabelas)
    imprimir_data_frame(cidades, "Cidades")

if __name__ == "__main__":
    main()
