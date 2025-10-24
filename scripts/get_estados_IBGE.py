import pandas as pd
import gdown
from io import BytesIO


URL_ESTADOS = "https://geoftp.ibge.gov.br/informacoes_ambientais/estudos_ambientais/grade_estatistica_de_dados_ambientais/dados_tabulares/estados/estados.csv"

def transformar_siglas_em_maiusculas(df):
    if 'sigla' in df.columns:
        df['sigla'] = df['sigla'].str.upper()
    return df

file = BytesIO()
gdown.download(URL_ESTADOS, file, quiet=False)
file.seek(0)

estados = pd.read_csv(file, sep=",", encoding="UTF-8-sig", header=0)
estados = transformar_siglas_em_maiusculas(estados)
print(estados.head())