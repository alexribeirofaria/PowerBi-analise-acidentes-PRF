import requests
import zipfile
import pandas as pd
from io import BytesIO

# ==============================================================  
# CONFIGURAÇÃO
# ==============================================================  
ARQUIVOS = {
    2025: "https://drive.google.com/uc?id=1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR",
    2024: "https://drive.google.com/uc?id=14lB0vqMFkaZj8HZ44b0njYgxs9nAN8KO",
    2023: "https://drive.google.com/uc?id=1-WO3SfNrwwZ5_l7fRTiwBKRw7mi1-HUq",
    2022: "https://drive.google.com/uc?id=1PRQjuV5gOn_nn6UNvaJyVURDIfbSAK4-",
    2021: "https://drive.google.com/uc?id=12xH8LX9aN2gObR766YN3cMcuycwyCJDz",
    2020: "https://drive.google.com/uc?id=1esu6IiH5TVTxFoedv6DBGDd01Gvi8785",
    2019: "https://drive.google.com/uc?id=1pN3fn2wY34GH6cY-gKfbxRJJBFE0lb_l",
}

# ==============================================================  
# FUNÇÕES
# ==============================================================  
def baixar_arquivo_memoria(url: str) -> BytesIO:
    """Baixa o arquivo do Google Drive diretamente para memória."""
    try:
        print(f"⬇️ Baixando {url} ...")
        response = requests.get(url)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"⚠️ Erro ao baixar {url}: {e}")
        return None

def extrair_csv_memoria(zip_bytes: BytesIO) -> BytesIO:
    """Extrai o primeiro CSV de um ZIP em memória e retorna BytesIO do CSV."""
    try:
        with zipfile.ZipFile(zip_bytes) as zip_ref:
            for nome in zip_ref.namelist():
                if nome.lower().endswith(".csv"):
                    return BytesIO(zip_ref.read(nome))
    except Exception as e:
        print(f"⚠️ Erro ao extrair ZIP em memória: {e}")
    return None

def ler_csv_memoria(csv_bytes: BytesIO) -> pd.DataFrame:
    """Lê o CSV em memória e retorna DataFrame."""
    try:
        return pd.read_csv(csv_bytes, sep=";", encoding="iso-8859-1", header=0)
    except Exception as e:
        print(f"⚠️ Erro ao ler CSV em memória: {e}")
        return pd.DataFrame()

# ==============================================================  
# EXECUÇÃO
# ==============================================================  
acidentes = {}

for ano, url in ARQUIVOS.items():
    zip_mem = baixar_arquivo_memoria(url)
    if zip_mem is None:
        print(f"❌ Falha ao baixar ZIP do ano {ano}")
        continue

    csv_mem = extrair_csv_memoria(zip_mem)
    if csv_mem is None:
        print(f"❌ Falha ao extrair CSV do ano {ano}")
        continue

    df = ler_csv_memoria(csv_mem)
    if df.empty:
        print(f"⚠️ CSV do ano {ano} vazio ou inválido")
        continue
    
    nome_var = f"acidentes_{ano}"
    globals()[nome_var] = df

    print(f"\n✅ {nome_var}:")
    print(globals()[nome_var].head())
    
