from calculos import (
    calcular_rendimento_liofilizacao,
)

def calcular_liofilizacao(dados):
    """
    Calcula a relação entre o veneno bruto e
    o veneno liofilizado.
    """
    rendimento = calcular_rendimento_liofilizacao(
        dados["veneno_bruto_g"],
        dados["veneno_liofilizado_ug"],
    )

    dados_calculados = dict(dados)

    dados_calculados[
        "rendimento_liofilizacao_percentual"
    ] = round(
        rendimento,
        2,
    )

    return dados_calculados
