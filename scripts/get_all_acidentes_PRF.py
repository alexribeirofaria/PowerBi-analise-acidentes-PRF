from  threading import Thread, Lock
import requests
import zipfile
import pandas as pd
from io import BytesIO

DATA_FRAMES = []
COLUNAS_PADRAO = set()
DATA_FRAMES_LOCK = Lock() 
ARQUIVOS = {
    2025: "https://drive.google.com/uc?id=1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR",
    2024: "https://drive.google.com/uc?id=14lB0vqMFkaZj8HZ44b0njYgxs9nAN8KO",
    2023: "https://drive.google.com/uc?id=1-WO3SfNrwwZ5_l7fRTiwBKRw7mi1-HUq",
    2022: "https://drive.google.com/uc?id=1PRQjuV5gOn_nn6UNvaJyVURDIfbSAK4-",
    2021: "https://drive.google.com/uc?id=12xH8LX9aN2gObR766YN3cMcuycwyCJDz",
    2020: "https://drive.google.com/uc?id=1esu6IiH5TVTxFoedv6DBGDd01Gvi8785",
    2019: "https://drive.google.com/uc?id=1pN3fn2wY34GH6cY-gKfbxRJJBFE0lb_l",
    2018: "https://drive.google.com/uc?id=1cM4IgGMIiR-u4gBIH5IEe3DcvBvUzedi",
    2017: "https://drive.google.com/uc?id=1HPLWt5f_l4RIX3tKjI4tUXyZOev52W0N"
}

f_baixar_arquivo_memoria = lambda url: (
    lambda: (
        print(f"Baixando {url} ..."),
        (r := requests.get(url)),
        r.raise_for_status(),
        BytesIO(r.content)
    )[-1]
)() if (lambda: True)() else None

def extrair_csv_memoria(zip_bytes: BytesIO) -> BytesIO:
    try:
        with zipfile.ZipFile(zip_bytes) as zip_ref:
            for nome in zip_ref.namelist():
                if nome.lower().endswith(".csv"):
                    return BytesIO(zip_ref.read(nome))
    except Exception as e:
        print(f"Erro ao extrair ZIP: {e}")
    return None

def ler_csv_memoria(csv_bytes: BytesIO, sep=";", encoding="iso-8859-1") -> pd.DataFrame:
    try:
        return pd.read_csv(csv_bytes, sep=sep, encoding=encoding, low_memory=False)
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return pd.DataFrame()

def definir_colunas_padrao():
    global COLUNAS_PADRAO
    ano_base = max(ARQUIVOS)
    url = ARQUIVOS[ano_base]
    zip_mem = f_baixar_arquivo_memoria(url)
    if not zip_mem:
        return False
    csv_mem = extrair_csv_memoria(zip_mem)
    if not csv_mem:
        return False
    df = ler_csv_memoria(csv_mem)
    if df.empty:
        return False
    COLUNAS_PADRAO.update(df.columns)
    return True

def carregar_acidentes(ano, url):
    try:
        zip_mem = f_baixar_arquivo_memoria(url)
        if not zip_mem:
            print(f"Falha ao baixar ZIP do ano {ano}")
            return
        csv_mem = extrair_csv_memoria(zip_mem)
        if not csv_mem:
            print(f"Falha ao extrair CSV do ano {ano}")
            return
        df = ler_csv_memoria(csv_mem)
        if df.empty:
            print(f"CSV do ano {ano} está vazio ou inválido")
            return
        nome_var = f"acidentes_{ano}"
        globals()[nome_var] = df
        with DATA_FRAMES_LOCK:
            DATA_FRAMES.append(df)
        print(f" {nome_var} carregado com {df.shape[0]} linhas")
    except Exception as e:
        print(f"Erro ao carregar dados do ano {ano}: {e}")


sucesso = definir_colunas_padrao()
if not sucesso:    
    exit(0)

threads = []
for ano, url in ARQUIVOS.items():
    t = Thread(target=carregar_acidentes, args=(ano, url))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

if not DATA_FRAMES:
    print("Nenhum dado carregado. Encerrando.")
    exit(0)
