# Projeto: Carga e Análise de Dados de Acidentes por Ocorrência

Este projeto automatiza a importação, extração e análise de dados de acidentes de trânsito da Polícia Rodoviária Federal (PRF), disponíveis em arquivos CSV compactados em ZIP. Os dados são carregados em pandas DataFrames para posterior análise e utilização no Power BI.

---

## 1. Visão Geral

O script Python realiza:

- Download dos arquivos ZIP diretamente do Google Drive.
- Extração dos arquivos CSV para diretório local ou memória.
- Leitura dos arquivos CSV em pandas DataFrames, garantindo a codificação correta e tratamento de caracteres especiais.
- Cache local dos dados para acelerar o carregamento em execuções futuras.
- Atualização inteligente para baixar e processar apenas os anos que precisam ser atualizados.
- Preparação dos dados para uso em ferramentas como Power BI.

---

## 2. Como o Power BI consome os dados?

Antes de integrar com Power BI, precisamos entender:

- **Fonte dos dados no Power BI:** CSV, Excel, banco de dados, API, etc.?
- **Localização do arquivo fonte:** local, rede, nuvem?
- **Método de atualização manual atual:** como você faz hoje para atualizar os dados?

---

## 3. Estratégia de atualização eficiente

O script Python:

- Detecta quais anos precisam ser atualizados (ex: ano corrente ou anos específicos).
- Baixa e processa somente esses anos.
- Atualiza o arquivo fonte (substituindo ou concatenando dados).
- Power BI simplesmente faz refresh para acessar os dados atualizados.

---

## 4. Exemplo prático: Atualizar CSV com dados novos

Se o arquivo `acidentes.csv` contém dados já baixados:

- Carrega o CSV existente.
- Identifica quais anos já estão presentes.
- Compara com os anos disponíveis no dicionário de URLs.
- Baixa e processa apenas os anos faltantes ou que precisam de atualização.
- Concatena os dados novos com os existentes, evitando duplicatas.
- Salva o CSV atualizado.

---

## 5. Ferramentas utilizadas

- **pandas**: Manipulação de dados tabulares.  
  Instalação: `pip install pandas`

- **matplotlib**: Geração de gráficos (opcional).  
  Instalação: `pip install matplotlib`

- **gdown**: Download de arquivos do Google Drive.  
  Instalação: `pip install gdown`

- **requests**: Download de arquivos via HTTP.  
  Instalação: `pip install requests`

---

## 6. Fonte dos dados

Os dados são provenientes da PRF, disponibilizados em:

[Dados Abertos da PRF](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf)

---

## 7. Estrutura do código

### Configurações principais

```python
ARQUIVOS = {
    2025: "https://drive.google.com/uc?id=1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR",
    2024: "https://drive.google.com/uc?id=14lB0vqMFkaZj8HZ44b0njYgxs9nAN8KO",
    # demais anos...
}
´´´

