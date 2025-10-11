# Projeto: Carga e Análise de Dados de Acidentes (2019–2025)

Este projeto automatiza a importação, extração e análise de dados de acidentes de trânsito da PRF, disponíveis em arquivos CSV compactados em ZIP. Os dados são carregados em pandas DataFrames para posterior análise e utilização no Power BI.

O projeto inclui download automático dos arquivos ZIP do Google Drive, extração dos CSVs mantendo caracteres especiais (á, ã, é), leitura com pandas e exibição das primeiras linhas de cada DataFrame. Os arquivos são organizados por ano, criando variáveis como `acidentes_2019`, `acidentes_2020` até `acidentes_2025`.

## Ferramentas utilizadas
- **pandas**: manipulação de dados tabulares. Comando: `pip install pandas`
- **matplotlib**: geração de gráficos. Comando: `pip install matplotlib`
- **gdown**: download de arquivos do Google Drive. Comando: `pip install gdown`

## Dados abertos
Para acessar os dados abertos da PRF: [Dados Abertos da PRF](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf?utm_source=chatgpt.com)

## Scripts principais
Os scripts realizam:
1. Download dos arquivos ZIP diretamente do Google Drive.
2. Extração dos arquivos CSV para diretório local.
3. Leitura dos arquivos CSV em pandas DataFrames, mantendo separação de colunas e linhas, encoding correto e caracteres especiais.
4. Exibição das primeiras linhas de cada DataFrame para conferência dos dados.

### Exemplo de uso no Python

```python
import gdown
import zipfile
import pandas as pd
import os

ARQUIVOS = {
    2025: "https://drive.google.com/uc?id=1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR",
    2024: "https://drive.google.com/uc?id=14lB0vqMFkaZj8HZ44b0njYgxs9nAN8KO",
    2023: "https://drive.google.com/uc?id=1-WO3SfNrwwZ5_l7fRTiwBKRw7mi1-HUq",
    2022: "https://drive.google.com/uc?id=1PRQjuV5gOn_nn6UNvaJyVURDIfbSAK4-",
    2021: "https://drive.google.com/uc?id=12xH8LX9aN2gObR766YN3cMcuycwyCJDz",
    2020: "https://drive.google.com/uc?id=1esu6IiH5TVTxFoedv6DBGDd01Gvi8785",
    2019: "https://drive.google.com/uc?id=1pN3fn2wY34GH6cY-gKfbxRJJBFE0lb_l",
}

def baixar_arquivo_memoria(url):
    arquivo = f"temp_{url.split('=')[-1]}.zip"
    gdown.download(url, arquivo, quiet=False)
    return arquivo

def extrair_csv(zip_file, pasta_destino="."):
    os.makedirs(pasta_destino, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(pasta_destino)
        for nome in zip_ref.namelist():
            if nome.lower().endswith(".csv"):
                return os.path.join(pasta_destino, nome)
    raise FileNotFoundError("Nenhum CSV encontrado no ZIP.")

acidentes = {}
for ano, url in ARQUIVOS.items():
    zip_local = baixar_arquivo_memoria(url)
    caminho_csv = extrair_csv(zip_local, pasta_destino=f"acidentes_{ano}")
    df = pd.read_csv(caminho_csv, sep=";", encoding="iso-8859-1", header=0)
    acidentes[ano] = df
    print(f"\nAcidentes {ano}:")
    print(df.head())
