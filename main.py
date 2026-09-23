import pandas as pd
import math

# ==============================
# CONFIGURAÇÕES

ARQUIVO = "funcionarios.xlsx"
MES_SELECIONADO = 9
QUANTIDADE_POR_ARTE = 12
ARQUIVO_SAIDA = "aniversariantes_canva.csv"

# ==============================
# LER PLANILHA

df = pd.read_excel(ARQUIVO)

df["Data de Nascimento"] = pd.to_datetime(
    df["Data de Nascimento"],
    dayfirst=True
)

# ==============================
# FILTRAR ANIVERSARIANTES

aniversariantes = df[
    df["Data de Nascimento"].dt.month == MES_SELECIONADO
].copy()


# ==============================
# ORDENAR POR DIA

aniversariantes["Dia"] = (
    aniversariantes["Data de Nascimento"].dt.day
)

aniversariantes = aniversariantes.sort_values(
  by="Dia"
)

# ==============================
# CALCULAR QUANTIDADE DE ARTES

quantidade = len(aniversariantes)

quantidade_de_artes = math.ceil(
    quantidade / QUANTIDADE_POR_ARTE
)

print()
print("=" * 60)
print("GERADOR DE ANIVERSARIANTES")
print("=" * 60)

print(f"Aniversariantes encontrados: {quantidade}")
print(f"Artes necessárias: {quantidade_de_artes}")

# ==============================
# CRIAR ESTRUTURA DO CSV

dados_canva = []

# ==============================
# DIVIDIR FUNCIONÁRIOS EM ARTES

for numero_arte in range(quantidade_de_artes):

    inicio = numero_arte * QUANTIDADE_POR_ARTE
    fim = inicio + QUANTIDADE_POR_ARTE

    grupo = aniversariantes.iloc[inicio:fim]


    # CRIAR UMA LINHA PARA A ARTE

    linha = {}
    linha["MES"] = "SETEMBRO" # Mês da arte


    # PREENCHER OS 12 ESPAÇOS
    for posicao in range(1, QUANTIDADE_POR_ARTE + 1):

        coluna_nome = f"NOME_{posicao}"
        coluna_data = f"DATA_{posicao}"

        if posicao <= len(grupo): # Verifica se existe funcionário

            funcionario = grupo.iloc[posicao - 1]
            nome = funcionario["Nome"]
            data = funcionario["Data de Nascimento"]
            data_formatada = data.strftime("%d/%m")

            linha[coluna_nome] = nome
            linha[coluna_data] = data_formatada

        else:      # Espaços vazios
            linha[coluna_nome] = ""
            linha[coluna_data] = ""


    # Adiciona a arte à lista
    dados_canva.append(linha)


# ==============================
# CRIAR DATAFRAME DO CANVA
df_canva = pd.DataFrame(dados_canva)


# ==============================
# EXPORTAR CSV

df_canva.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")

# ==============================
# MOSTRAR RESULTADO

print()
print("CSV criado com sucesso!")
print(f"Arquivo: {ARQUIVO_SAIDA}")

print()
print("=" * 60)
print("PRÉVIA DOS DADOS")
print("=" * 60)

for indice, linha in df_canva.iterrows():

    print()
    print(f"ARTE {indice + 1}")

    for posicao in range(1, 13):
        nome = linha[f"NOME_{posicao}"]
        data = linha[f"DATA_{posicao}"]

        if nome:
            print(f"{posicao:02d} - {nome} - {data}" )