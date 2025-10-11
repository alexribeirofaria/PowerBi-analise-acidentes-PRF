# Carga de arquivos a partir de script Python

### Antes de propor melhorias concretas para a educação, os pesquisadores precisaram estudar os dadosNessa etapa, perceberam que analisar o processo educacional como um todo era muito complexo e e reduziram o escopo do problema. Essa decisão foi correta? Como você continuaria esse projeto?

  > Sim, os pesquisadores tomaram uma boa decisão ao reduzir o escopo do projeto para focar apenas na educação primária. Mesmo assim, eles ainda se depararam com muitos desafios, pois esses dados não estão centralizados nem são armazenados seguindo um padrão específico. Para continuar esse projeto, é necessário aumentar o escopo lentamente, pois é provável que as próximas etapas compartilhem muitos pontos em comum com o que já foi produzido, mas cada novo passo exige muito cuidado para que a consistência seja garantida.

  

### Para acessar os dados abertos da PRF, veja o link oficial:  
 > [Dados Abertos da PRF](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf?utm_source=chatgpt.com)


### Pandas 
  É uma biblioteca largamente utilizada para manipulação e análise de dados. Oferece estruturas de dados e
operações para manipular tabelas numéricas e séries temporais. Os dados importados devem estar em uma estrutura de        dados  do Pandas, caracterizada pela bidimensionalidade, ou seja, são organizados em linhas e colunas. 
  São conhecidos como Pandas DataFrames.
   > pip install pandas
 
 ### Matplotlib
   É uma biblioteca utilizada para geração de gráficos a partir de dados oriundos de Pandas DataFrames ou, então, de  dados vetorizados. Uma das dependências instaladas juntamente com o Matplotlib é a biblioteca Numpy, largamente utilizada para trabalhar com vetores, matrizes e operações matemáticas entre essas estruturas.
 >  pip install matplotlib
 
 ### Arquivos importados no formato correto que vieram CRLF do windows mantendo caracteres epeciais nos dados com ã á etc.

```python
import gdown
import zipfile
import pandas as pd
import os

# URLs dos arquivos ZIP no Google Drive (direto para download)
url_2020 = 'https://drive.google.com/uc?id=1esu6IiH5TVTxFoedv6DBGDd01Gvi8785'
url_2019 = 'https://drive.google.com/uc?id=1pN3fn2wY34GH6cY-gKfbxRJJBFE0lb_l'

# Nomes temporários dos arquivos ZIP
zip_2020 = 'datatran2020.zip'
zip_2019 = 'datatran2019.zip'

# Baixa os arquivos ZIP
gdown.download(url_2020, zip_2020, quiet=False)
gdown.download(url_2019, zip_2019, quiet=False)

# Função para extrair CSV de um ZIP e retornar o caminho do CSV extraído
def extrair_csv(zip_file, pasta_destino="."):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(pasta_destino)
        # Assume que o ZIP contém apenas um CSV
        for nome_arquivo in zip_ref.namelist():
            if nome_arquivo.endswith('.csv'):
                return os.path.join(pasta_destino, nome_arquivo)

# Extrai os CSVs
caminho_2020 = extrair_csv(zip_2020)
caminho_2019 = extrair_csv(zip_2019)

# Lê os CSVs com pandas
acidentes_2020 = pd.read_csv(caminho_2020, sep=';', encoding='iso-8859-1', header=0)
acidentes_2019 = pd.read_csv(caminho_2019, sep=';', encoding='iso-8859-1', header=0)

# Exibe as primeiras linhas
print(acidentes_2020.head())
print(acidentes_2019.head())

```


```python
# Documento CSV de Acidentes 2025 (Agrupados por pessoa - Todas as causas e tipos de acidentes)	
# https://drive.google.com/file/d/1-PJGRbfSe7PVjU37A3wTCls_NRXyVGRD/view
import gdown
import zipfile
import pandas as pd
import os

# URL do arquivo ZIP no Google Drive (ID direto)
url_2020 = 'https://drive.google.com/uc?id=1-Gp9S-ALO0D1nT8S_OKoC8xlW7BY8F82'

# Nome do arquivo ZIP e diretório de extração
arquivo_zip_2020 = 'acidentes2025.zip'
pasta_destino_2020 = 'acidentes2025'

# Baixa o arquivo ZIP, se ainda não existir
if not os.path.exists(arquivo_zip_2020):
    print(f"Baixando {arquivo_zip_2020}...")
    gdown.download(url_2020, arquivo_zip_2020, quiet=False)
else:
    print(f"{arquivo_zip_2020} já existe, pulando download.")

# Função para extrair CSV de um ZIP e retornar o caminho do CSV extraído
def extrair_csv(zip_file, pasta_destino="."):
    os.makedirs(pasta_destino, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(pasta_destino)
        for nome_arquivo in zip_ref.namelist():
            if nome_arquivo.lower().endswith('.csv'):
                caminho_csv = os.path.join(pasta_destino, nome_arquivo)
                print(f"Arquivo CSV encontrado: {caminho_csv}")
                return caminho_csv
    raise FileNotFoundError("Nenhum arquivo CSV encontrado dentro do ZIP.")

# Extrai o CSV e lê com pandas
caminho_csv_2020 = extrair_csv(arquivo_zip_2020, pasta_destino_2020)

# Lê o CSV (com encoding e separador apropriados)
acidentes2025 = pd.read_csv(caminho_csv_2020, sep=';', encoding='latin1', low_memory=False)

# Exibe as primeiras linhas e informações básicas
print("\nPré-visualização dos dados:")
print(acidentes2025.head())

print("\nInformações do DataFrame:")
print(acidentes2025.info())
```

```python 
import gdown
import zipfile
import pandas as pd
import os
url = 'https://drive.google.com/uc?id=1esu6IiH5TVTxFoedv6DBGDd01Gvi8785'

# Nome temporário do arquivo ZIP
arquivo_zip = 'datatran2020.zip'

# Baixa o arquivo ZIP
gdown.download(url, arquivo_zip, quiet=False)

# Função para extrair CSV de um ZIP e retornar o caminho do CSV extraído
def extrair_csv(zip_file, pasta_destino="."):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(pasta_destino)
        # Assume que o ZIP contém apenas um CSV
        for nome_arquivo in zip_ref.namelist():
            if nome_arquivo.endswith('.csv'):
                return os.path.join(pasta_destino, nome_arquivo)

# Extrai o CSV
caminho = extrair_csv(arquivo_zip)

# Lê o CSV com pandas
acidentes = pd.read_csv(caminho, sep=';', encoding='iso-8859-1', header=0)


url_acidentes_por_pessoas = 'https://drive.google.com/uc?id=1iQvs2D9a2XO9vIukrjEIIhtjzkNkgD7Z'

# Nome temporário do arquivo ZIP
arquivo_zip_acidentes_por_pessoas = 'acidentes2020.zip'

# Baixa o arquivo ZIP
gdown.download(url_acidentes_por_pessoas, arquivo_zip_acidentes_por_pessoas, quiet=False)

# Função para extrair CSV de um ZIP e retornar o caminho do CSV extraído
def extrair_csv(zip_file, pasta_destino="."):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(pasta_destino)
        # Assume que o ZIP contém apenas um CSV
        for nome_arquivo in zip_ref.namelist():
            if nome_arquivo.endswith('.csv'):
                return os.path.join(pasta_destino, nome_arquivo)

# Extrai o CSV
caminho_acidentes_por_pessoas = extrair_csv(arquivo_zip_acidentes_por_pessoas)

# Lê o CSV com pandas
acidentes2020_por_pessoas = pd.read_csv(caminho_acidentes_por_pessoas, sep=';', encoding='iso-8859-1', header=0)


print(acidentes.head())
print(acidentes2020_por_pessoas.head())

```

### Os dirigentes da Aço para o Progresso S.A. perceberam a necessidade de modelar seus processos como um todo. Curiosamente, cada etapa desses processos já estava modelada. O que pode explicar essa falta de integração dos sistemas que modelavam os processos da Aço para o Progresso S.A.?

  >  B)Os sistemas da Aço para o Progresso S.A. foram desenvolvidos para tratar processos específicos.
  Em empresas de grande porte, é comum a existência de diferentes setores. As soluções são dadas, normalmente, com o objetivo de resolver problemas desses setores. Como, raramente, esse processo ocorre de forma ordenada, integrar os sistemas posteriormente é um grande desafio.

### O fato de os gestores da Aço para o Progresso S.A. perceberem a importância da modelagem dos processos chama a atenção para as muitas etapas que são necessárias para tornar isso concreto. A respeito dessas etapas, qual a importância de usar uma ferramenta especializada na modelagem de dados?

 >  E) Possui recursos que otimizam o trabalho de realizar a modelagem.

 Usar ferramentas especializadas na modelagem de dados facilita muito esse trabalho, pois elas já possuem muitas funcionalidades que poupam tempo e garantem consistência dos resultados. No final, é esperado que o processo seja automatizado, mas a construção da modelagem depende de profissionais que entendam bem de detalhes do negócio.

### Considere o seguinte cenário: você foi contratado para treinar alguns dos analistas da Aço para o Progresso S.A. na modelagem de dados. Seu trabalho é muito importante e, se for bem-sucedido, você dará outros treinamentos na empresa. Nesse cenário, qual seria a estratégia que você adotaria?
  
   > Ensinar pessoas sempre é um grande privilégio e uma oportunidade de aprender também através da natural troca de experiências. No cenário descrito, é importante entender que um treinamento deve resultar em profissionais qualificados. Portanto, a melhor forma de aprender modelagem é trabalhar em um exemplo real, porém pequeno, em que seja possível verificar a aplicação dos conceitos na prática com a utilização de uma ferramenta específica para modelagem.


### Ao importar a tabela Clientes no formato CSV e a tabela Endereços no formato Excel, utilizando o Power Query, temos o esquema a seguir, em que as colunas ID_Cliente e ID_Endereço representam chaves primárias:

Clientes	Endereços
ID_Cliente	ID_Endereço
Nome Cliente	Endereço 1
Telefone	Cidade
E-mail	Estado
ID_Endereço	País
CEP
Elaborada por Humberto Cesar Souza Lomeu.

Precisamos criar uma consulta com um cliente por linha, e cada linha deve conter Cidade, Estado e País de cada cliente. Que recurso do Power BI devemos aplicar?

    > A) Combinar as tabelas Clientes e Endereços.



###  Que recurso podemos usar no Power BI para eliminar registros de dados não preenchidos ou em duplicata?

 > B) Remover linhas.
Comentário
Parabéns! A alternativa "B" está correta.


A interface do Power BI possui o recurso “Reduzir linhas”, que tem a opção “Remover linhas”, cujos principais recursos são: Remover Duplicadas, Remover Linhas em Branco e Remover Erros. Essa limpeza de dados deve ser feita caso a caso, pois o Power BI não possui funcionalidade para correção automática desses problemas.


###  A Invista Bem S.A. trabalha com grandes volumes de dados de diferentes formatos que alimentam um sistema de suporte à tomada de decisão. Qual foi o principal risco da Invista Bem S.A. ao trabalhar com esses dados?

 > C) Utilizar dados inconsistentes que prejudicaram as respostas do sistema de suporte à tomada de decisão.

Comentário
Um sistema de suporte à tomada de decisão possui regras ou é treinado para produzir respostas que dependem dos dados de entrada. No caso da Invista Bem S.A., foram detectadas inconsistências nos dados que levaram à produção de respostas também inconsistentes do sistema de suporte à tomada de decisão.

### Como você leu no texto, uma das fontes de dados que a Invista Bem S.A. utiliza é a de grupos de redes sociais. Dentro da empresa, é conhecido que esses dados não são confiáveis. Como esses dados podem ser modelados sem prejudicar a consistência da informação?
 >  A) Devem receber alguma marcação sobre o nível de confiança.

Comentário
Utilizar dados de fontes não confiáveis é um risco. No caso da Invista Bem S.A., utilizar esse tipo de dado é uma decisão que faz parte do processo de tomada de decisão. Portanto, é importante que esses dados recebam uma marcação que permita entender o quanto são confiáveis, pois eles podem ser usados como fontes ponderadoras para dar suporte para a tomada de decisão.

### Considere o seguinte cenário: você foi contratado pela Invista Bem S.A. para melhorar o modelo de dados. Existem muitas expectativas sobre o resultado do seu trabalho. Com base em sua experiência, como você cumpriria essa missão? De que maneira iria demonstrar que seu trabalho foi bem-sucedido?

> A Invista Bem S.A. é uma empresa de investimentos que utiliza grandes volumes de dados de diversas fontes. Portanto, a primeira ação a ser tomada é mapear todas essas fontes e medir a dimensão do volume de dados. Cumprida essa etapa, vem a análise do processo de limpeza e transformação de cada um dos dados. Aqui, é fundamental fazer o registro de todas as ocorrências de inconsistências, pois isso será muito importante para demonstrar, posteriormente, como sua intervenção gerou resultados.


### A sintaxe da linguagem M é dividida em dois blocos:
    > let - Em que são definidas as variáveis.
    > in - Saída do que foi definido no primeiro bloco.



### Após algumas transformações, o usuário obteve o seguinte código:
#"Colunas Removidas" = Table.RemoveColumns(#"Tipo Alterado",{"CPF"}), #"Duplicatas Removidas" = Table.Distinct(#"Colunas Removidas", {"TITULO"}), #"Texto Substituído inserido" = Table.AddColumn(#"Duplicatas Removidas", "Texto Substituído", each Text.Replace(Text.Lower([TITULO]), "s", "Senho"), type text)
Caso ele deseje retirar a etapa em destaque, o que deve ser feito para concluir seu objetivo?

    > E) Deletar a linha da etapa em destaque e trocar o nome da etapa anterior na etapa #"Texto Substituído inserido".

Comentário
Parabéns! A alternativa "E" está correta.
Por possuir uma estrutura de etapas, uma função na linguagem M sempre faz referência à função anterior. Então, ao simplesmente deletar a linha que não será utilizada, a função seguinte buscará por uma função que não existe mais, e o código não funcionará.

### Um usuário utilizou a função SWITCH na barra de fórmulas e a copiou para o Editor Avançado, porém, ao clicar em concluir, nada acontece. O que o usuário fez de errado?

    >  B) O usuário utilizou uma função de DAX em um código em linguagem M.

Comentário
Parabéns! A alternativa "B" está correta.
SWITCH é uma função da linguagem DAX, e o Editor Avançado é uma interface da linguagem M, que não permite a utilização de funções de DAX. Embora muitas funcionalidades das duas linguagens sejam comuns, suas sintaxes não suportam comandos de uma linguagem em scripts da outra.