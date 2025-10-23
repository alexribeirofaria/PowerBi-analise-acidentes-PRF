from  threading import Thread, Lock
import requests
import zipfile
import pandas as pd
from io import BytesIO
from .arquivos import ARQUIVOS

# =======================  
# GLOBALS PARA CONCATENAR  
# =======================  

DATA_FRAMES = []
COLUNAS_PADRAO = set()
data_frames_lock = Lock() 

# -------------------------------------------------------
# Baixa arquivo ZIP de uma URL e retorna em memória
# 
# Parâmetros:
# - url (str): URL do arquivo ZIP a ser baixado.
# 
# Retorno:
# - BytesIO: objeto em memória com o arquivo ZIP.
# - None: em caso de erro no download.
# -------------------------------------------------------
f_baixar_arquivo_memoria = lambda url: (
    lambda: (
        print(f"Baixando {url} ..."),
        (r := requests.get(url)),
        r.raise_for_status(),
        BytesIO(r.content)
    )[-1]
)() if (lambda: True)() else None


# -------------------------------------------------------
# Função para tratar colunas de um DataFrame, verificando se existem
# e convertendo seus tipos conforme especificado.
#
# Parâmetros:
# - df (pd.DataFrame): DataFrame a ser tratado.
# - colunas_e_tipos (dict): Dicionário com nomes das colunas como chave
#   e tipos desejados como valor (ex: {"id": "Int64", "nome": "str"}).
# - coluna_indice (str, opcional): Nome da coluna para ser usada como índice,
#   caso exista no DataFrame.
#
# Retorno:
# - pd.DataFrame: DataFrame com as colunas convertidas e índice ajustado.
#
# Exemplo de uso:
# >>> df = pd.DataFrame({
# ...     "id": ["1", "2", "3"],
# ...     "idade": ["25", "30", "40"],
# ...     "nome": ["Ana", "Beto", "Carla"],
# ...     "valor": ["10.5", "20.7", "15.0"]
# ... })
# >>> colunas_desejadas = {"id": "Int64", "idade": "Int64", "nome": "str", "valor": "float64"}
# >>> df_tratado = tratar_colunas(df, colunas_desejadas, coluna_indice="id")
# >>> print(df_tratado.index)
# Int64Index([1, 2, 3], dtype='int64', name='id')
# >>> print(df_tratado.dtypes)
# idade       Int64
# nome       object
# valor     float64
# dtype: object
# -------------------------------------------------------

f_tratar_colunas = lambda df, col_tipos, col_indice=None: (
    [
        (
            (lambda conv: 
                df.__setitem__(col, conv(df[col].fillna(0)))
                or (df.__setitem__(col, df[col].replace(0, "")) if col in ["longitude", "latitude"] else None)
            )
            (
                (lambda x: pd.to_numeric(x, errors="coerce").astype("Int64")) if tipo == "Int64" else
                (lambda x: pd.to_numeric(x, errors="coerce").astype("float64")) if tipo == "float64" else
                (lambda x: pd.to_datetime(x, errors="coerce")) if tipo == "datetime64[ns]" else
                (lambda x: x.astype(str)) if tipo == "str" else
                (lambda x: x.astype(tipo))
            )
        ) if col in df.columns else print(f"Coluna '{col}' não encontrada no DataFrame.")
        [df.drop(columns=["ano"], inplace=True)]
        for col, tipo in col_tipos.items()
    ],

    (df.set_index(col_indice, inplace=True), print(f"Coluna '{col_indice}' definida como índice.")) if col_indice and col_indice in df.columns else
    (print(f"Coluna índice '{col_indice}' não encontrada para setar como índice.") if col_indice else None),

    df
)[-1]

def remover_coluna_ano(df):
    if "ano" in df.columns:
        df.drop(columns=["ano"], inplace=True)
        print("Coluna 'ano' removida do DataFrame.")
        
# -------------------------------------------------------
# Extrai o primeiro arquivo CSV encontrado em ZIP em memória
#
# Parâmetros:
# - zip_bytes (BytesIO): objeto com arquivo ZIP em memória.
#
# Retorno:
# - BytesIO: objeto em memória com o arquivo CSV extraído.
# - None: se não encontrar CSV ou erro.
# -------------------------------------------------------
def baixar_arquivo_memoria(url: str) -> BytesIO:
    try:
        print(f"Baixando {url} ...")
        response = requests.get(url)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return None

# -------------------------------------------------------
# Extrai o primeiro arquivo CSV encontrado em ZIP em memória
#
# Parâmetros:
# - zip_bytes (BytesIO): objeto com arquivo ZIP em memória.
#
# Retorno:
# - BytesIO: objeto em memória com o arquivo CSV extraído.
# - None: se não encontrar CSV ou erro.
# -------------------------------------------------------
def extrair_csv_memoria(zip_bytes: BytesIO) -> BytesIO:
    try:
        with zipfile.ZipFile(zip_bytes) as zip_ref:
            for nome in zip_ref.namelist():
                if nome.lower().endswith(".csv"):
                    return BytesIO(zip_ref.read(nome))
    except Exception as e:
        print(f"Erro ao extrair ZIP: {e}")
    return None

# -------------------------------------------------------
# Lê CSV de um BytesIO e retorna DataFrame pandas
#
# Parâmetros:
# - csv_bytes (BytesIO): arquivo CSV em memória.
# - sep (str): separador (default ';').
# - encoding (str): codificação do CSV (default 'iso-8859-1').
#
# Retorno:
# - pd.DataFrame: DataFrame com dados CSV.
# - DataFrame vazio se erro.
# -------------------------------------------------------

# -------------------------------------------------------
# Lê CSV de um BytesIO e retorna DataFrame pandas
#
# Parâmetros:
# - csv_bytes (BytesIO): arquivo CSV em memória.
# - sep (str): separador (default ';').
# - encoding (str): codificação do CSV (default 'iso-8859-1').
#
# Retorno:
# - pd.DataFrame: DataFrame com dados CSV.
# - DataFrame vazio se erro.
# -------------------------------------------------------
def ler_csv_memoria(csv_bytes: BytesIO, sep=";", encoding="iso-8859-1") -> pd.DataFrame:
    try:
        return pd.read_csv(csv_bytes, sep=sep, encoding=encoding, low_memory=False)
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return pd.DataFrame()


# -------------------------------------------------------
# Define as colunas padrão baseando-se no maior ano disponível
#
# Parâmetros:
# - nenhum
#
# Retorno:
# - bool: True se conseguiu definir as colunas, False caso contrário
# -------------------------------------------------------
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

# -------------------------------------------------------
# Carrega dados de acidentes para um ano dado, adiciona ao global
#
# Parâmetros:
# - ano (int): ano dos dados.
# - url (str): URL para download do ZIP.
#
# Retorno:
# - None (os dados são salvos em variáveis globais e na lista dataframes)
# -------------------------------------------------------
def carregar_acidentes(ano, url):
    try:
        zip_mem = f_baixar_arquivo_memoria(url)
        if not zip_mem:
            print(f"❌ Falha ao baixar ZIP do ano {ano}")
            return
        csv_mem = extrair_csv_memoria(zip_mem)
        if not csv_mem:
            print(f"❌ Falha ao extrair CSV do ano {ano}")
            return
        df = ler_csv_memoria(csv_mem)
        if df.empty:
            print(f"⚠️ CSV do ano {ano} está vazio ou inválido")
            return
        nome_var = f"acidentes_{ano}"
        globals()[nome_var] = df
        with data_frames_lock:
            DATA_FRAMES.append(df)
        print(f" {nome_var} carregado com {df.shape[0]} linhas")
    except Exception as e:
        print(f"❌ Erro ao carregar dados do ano {ano}: {e}")


# -------------------------------------------------------
# Função principal que executa o carregamento, concatenação e salvamento
#
# Parâmetros:
# - nenhum
#
# Retorno:
# - None (resultados impressos e arquivo salvo)
# -------------------------------------------------------
def main():
    sucesso = definir_colunas_padrao()
    if not sucesso:
        print("Falha ao determinar colunas padrao. Nenhum arquivo processado.")
        return

    threads = []
    for ano, url in ARQUIVOS.items():
        t = Thread(target=carregar_acidentes, args=(ano, url))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if not DATA_FRAMES:
        print("Nenhum dado carregado. Encerrando.")
        return

    df = pd.concat(DATA_FRAMES, ignore_index=False)
    df.to_csv("acidentes.csv", sep=";", encoding="UTF-8-sig")
    print("Arquivo 'acidentes.csv' salvo com sucesso.")
    print(df.head())
    colunas_desejadas = {
        "id": "Int64",
        "data_inversa": "datetime64[ns]",
        "br": "Int64",
        "km": "float64",
        "pessoas": "Int64",
        "mortos": "Int64",
        "feridos_leves": "Int64",
        "feridos_graves": "Int64",
        "ilesos": "Int64",
        "ignorados": "Int64",
        "longitude": "float64",
        "latitude": "float64"
    }

    acidentes = f_tratar_colunas(df, colunas_desejadas)
    return acidentes

# ==============================================================  
# EXECUTA
# ==============================================================  
if __name__ == "__main__":
    main()
