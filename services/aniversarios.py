import math
from pathlib import Path

import pandas as pd


QUANTIDADE_POR_ARTE = 12

MESES = {
    1: "JANEIRO",
    2: "FEVEREIRO",
    3: "MARÇO",
    4: "ABRIL",
    5: "MAIO",
    6: "JUNHO",
    7: "JULHO",
    8: "AGOSTO",
    9: "SETEMBRO",
    10: "OUTUBRO",
    11: "NOVEMBRO",
    12: "DEZEMBRO",
}

def formatar_nome(nome):
    partes = str(nome).strip().split()

    if len(partes) == 1:
        return partes[0].lower()

    return f"{partes[0]} {partes[-1]}".lower()

def carregar_planilha(caminho):
    """Carrega a planilha do RH e valida as colunas necessárias."""

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Planilha não encontrada: {caminho}"
        )

    df = pd.read_excel(caminho)

    colunas_obrigatorias = [
        "Nome",
        "Data de Nascimento",
    ]

    colunas_faltando = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if colunas_faltando:
        raise ValueError(
            "A planilha não possui as colunas obrigatórias: "
            + ", ".join(colunas_faltando)
        )

    df["Data de Nascimento"] = pd.to_datetime(
        df["Data de Nascimento"],
        dayfirst=True,
        errors="coerce",
    )

    if df["Data de Nascimento"].isna().any():
        raise ValueError(
            "Existem datas de nascimento inválidas na planilha."
        )

    return df


def buscar_aniversariantes(df, mes):
    """Filtra e ordena os aniversariantes do mês escolhido."""

    aniversariantes = df[
        df["Data de Nascimento"].dt.month == mes
    ].copy()

    aniversariantes["Dia"] = (
        aniversariantes["Data de Nascimento"].dt.day
    )

    aniversariantes = aniversariantes.sort_values(
        by="Dia"
    ).reset_index(drop=True)

    return aniversariantes


def dividir_em_artes(aniversariantes):
    """Divide os funcionários em grupos de até 12."""

    quantidade = len(aniversariantes)

    quantidade_de_artes = math.ceil(
        quantidade / QUANTIDADE_POR_ARTE
    )

    artes = []

    for numero_arte in range(quantidade_de_artes):
        inicio = numero_arte * QUANTIDADE_POR_ARTE
        fim = inicio + QUANTIDADE_POR_ARTE

        grupo = aniversariantes.iloc[inicio:fim]

        artes.append(grupo)

    return artes


def preparar_dados_canva(artes, mes):
    """Transforma os grupos no formato esperado pelo Canva."""

    nome_mes = MESES[mes].lower()

    dados_canva = []

    for numero_arte, grupo in enumerate(artes, start=1):

        linha = {
            "MES": nome_mes,
        }

        for posicao in range(1, QUANTIDADE_POR_ARTE + 1):

            coluna_nome = f"NOME_{posicao}"
            coluna_data = f"DATA_{posicao}"

            if posicao <= len(grupo):

                funcionario = grupo.iloc[posicao - 1]

                linha[coluna_nome] = formatar_nome(funcionario["Nome"])

                linha[coluna_data] = (
                    funcionario["Data de Nascimento"]
                    .strftime("%d/%m")
                )

            else:

                linha[coluna_nome] = ""
                linha[coluna_data] = ""

        linha["ARTE"] = numero_arte

        dados_canva.append(linha)

    return pd.DataFrame(dados_canva)


def gerar_csv(df_canva, caminho_saida):
    """Salva o arquivo final para importação no Canva."""

    caminho_saida = Path(caminho_saida)

    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df_canva.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8-sig",
    )

    return caminho_saida


def processar_aniversarios(
    caminho_planilha,
    mes,
    caminho_saida,
):
    """
    Executa todo o processamento de aniversários.

    Retorna:
        aniversariantes
        artes
        dataframe do Canva
        caminho do CSV
    """

    df = carregar_planilha(caminho_planilha)
    aniversariantes = buscar_aniversariantes( df, mes,)

    artes = dividir_em_artes( aniversariantes)

    df_canva = preparar_dados_canva(
        artes,
        mes,
    )

    arquivo = gerar_csv(
        df_canva,
        caminho_saida,
    )

    return (
        aniversariantes,
        artes,
        df_canva,
        arquivo,
    )