import pandas as pd
import gdown
from io import BytesIO

# URL do arquivo estados IBGE
url = 'https://geoftp.ibge.gov.br/informacoes_ambientais/estudos_ambientais/grade_estatistica_de_dados_ambientais/dados_tabulares/estados/estados.csv'

# Baixa o arquivo em memória
arquivo_excel = BytesIO()
gdown.download(url, arquivo_excel, quiet=False)
arquivo_excel.seek(0)  # IMPORTANTE: voltar ao início do arquivo

estados = pd.read_csv(arquivo_excel, sep=',', encoding='iso-8859-1', header=0)

print(estados.head())
