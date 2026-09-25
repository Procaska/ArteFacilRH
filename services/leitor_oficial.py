from pathlib import Path
import pandas as pd

NOME_ABA = "QUADRO DE LOTAÇÃO"

# Colunas que realmente usamos:
# B = Nome
# G = Data de Nascimento
# O = Data de Admissão

COLUNA_NOME = 1              # B
COLUNA_NASCIMENTO = 6        # G
COLUNA_ADMISSAO = 14         # O

LINHA_INICIAL = 2            # linha 3 do Excel


def carregar_planilha_oficial(caminho):
    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Planilha não encontrada: {caminho}"
        )

    try:
        df = pd.read_excel(
            caminho,
            sheet_name=NOME_ABA,
            header=None,
        )
    except ValueError as erro:
        raise ValueError(
            f'A aba "{NOME_ABA}" não foi encontrada.'
        ) from erro

    registros = []

    for linha in range(LINHA_INICIAL, len(df)):

        nome = df.iat[linha, COLUNA_NOME]
        nascimento = df.iat[linha, COLUNA_NASCIMENTO]
        admissao = df.iat[linha, COLUNA_ADMISSAO]

        # Ignora linhas sem funcionário
        if pd.isna(nome):
            continue

        nome = str(nome).strip()

        if not nome:
            continue

        registros.append({
            "Nome": nome,
            "Data de Nascimento": nascimento,
            "Data de Admissão": admissao,
        })

    if not registros:
        raise ValueError(
            f'Nenhum funcionário encontrado na aba "{NOME_ABA}".'
        )

    funcionarios = pd.DataFrame(registros)

    funcionarios["Data de Nascimento"] = pd.to_datetime(
        funcionarios["Data de Nascimento"],
        errors="coerce",
    )

    funcionarios["Data de Admissão"] = pd.to_datetime(
        funcionarios["Data de Admissão"],
        errors="coerce",
    )

    # Remove funcionários repetidos
    funcionarios = funcionarios.drop_duplicates(
        subset=[
            "Nome",
            "Data de Nascimento",
            "Data de Admissão",
        ]
    ).reset_index(drop=True)

    # Validação
    if funcionarios["Data de Nascimento"].isna().any():
        raise ValueError(
            "Existem datas de nascimento inválidas na planilha."
        )

    if funcionarios["Data de Admissão"].isna().any():
        raise ValueError(
            "Existem datas de admissão inválidas na planilha."
        )

    return funcionarios