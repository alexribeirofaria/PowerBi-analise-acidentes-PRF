import pandas as pd
import gdown
from io import BytesIO

# URL do arquivo no Google Drive
url = 'https://drive.google.com/uc?id=1PGHfXCKvylSXDWZXznVQjdhDY22hLaTQ'

# Baixa o arquivo em memória
arquivo_excel = BytesIO()
gdown.download(url, arquivo_excel, quiet=False)
arquivo_excel.seek(0)  # IMPORTANTE: voltar ao início do arquivo

# Lê todas as abas
tabelas = pd.read_excel(arquivo_excel, sheet_name=None)

# Lista todas as abas 1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR
print("Abas disponíveis:", list(tabelas.keys()))

# Acessa as tabelas individualmente
estados = tabelas.get('estados')      # ou usar o nome exato da aba
municipios = tabelas.get('municipios')
cidades = tabelas.get('cidades')

# Mostra as primeiras linhas de cada tabela
print("=== Estados ===")
print(estados.head())

print("\n=== Municípios ===")
print(municipios.head())

print("\n=== Cidades ===")
print(cidades.head())
