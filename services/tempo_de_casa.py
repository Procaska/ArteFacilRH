from pathlib import Path
from datetime import datetime

import pandas as pd

from services.aniversarios import formatar_nome


MARCOS_TEMPO_DE_CASA = [5, 10, 15, 20, 25]


def carregar_planilha(caminho):
    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(f"Planilha não encontrada: {caminho}")

    df = pd.read_excel(caminho)

    colunas_obrigatorias = ["Nome", "Data de Admissão"]
    colunas_faltando = [
        coluna for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if colunas_faltando:
        raise ValueError(
            "A planilha não possui as colunas obrigatórias: "
            + ", ".join(colunas_faltando)
        )

    df["Data de Admissão"] = pd.to_datetime(
        df["Data de Admissão"],
        dayfirst=True,
        errors="coerce",
    )

    if df["Data de Admissão"].isna().any():
        raise ValueError("Existem datas de admissão inválidas na planilha.")

    return df


def buscar_marcos(df, mes, ano=None):
    if ano is None:
        ano = datetime.now().year

    funcionarios = df[
        df["Data de Admissão"].dt.month == mes
    ].copy()

    resultados = []

    for _, funcionario in funcionarios.iterrows():
        data_admissao = funcionario["Data de Admissão"]
        anos_de_casa = ano - data_admissao.year

        if anos_de_casa not in MARCOS_TEMPO_DE_CASA:
            continue

        resultados.append({
            "Nome": funcionario["Nome"],
            "Data de Admissão": data_admissao,
            "Tempo de Casa": anos_de_casa,
            "Data do Marco": data_admissao.strftime("%d/%m"),
        })

    return pd.DataFrame(resultados)


def preparar_dados_canva(marcos, mes, meses):
    nome_mes = meses[mes].lower()
    dados_canva = []

    for _, funcionario in marcos.iterrows():
        dados_canva.append({
            "MES": nome_mes,
            "NOME": formatar_nome(funcionario["Nome"]),
            "TEMPO_DE_CASA": f"{funcionario['Tempo de Casa']} anos",
            "DATA": funcionario["Data do Marco"],
        })

    return pd.DataFrame(
        dados_canva,
        columns=["MES", "NOME", "TEMPO_DE_CASA", "DATA"],
    )


def gerar_csv(df_canva, caminho_saida):
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    df_canva.to_csv(caminho_saida, index=False, encoding="utf-8-sig")
    return caminho_saida


def processar_tempo_de_casa(
    caminho_planilha,
    mes,
    caminho_saida,
    ano=None,
    meses=None,
):
    if meses is None:
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
        }

    df = carregar_planilha(caminho_planilha)
    marcos = buscar_marcos(df, mes, ano)
    df_canva = preparar_dados_canva(marcos, mes, meses)
    arquivo = gerar_csv(df_canva, caminho_saida)

    return marcos, df_canva, arquivo
