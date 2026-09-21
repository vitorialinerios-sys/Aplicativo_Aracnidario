from calculos import (
    calcular_taxa_mortalidade,
)


def calcular_manutencao(dados):
    """
    Calcula a taxa de mortalidade da manutenção.
    """
    taxa = calcular_taxa_mortalidade(
        dados["vivas"],
        0,
        dados["mortas"],
    )

    dados_calculados = dict(dados)

    dados_calculados[
        "taxa_mortalidade"
    ] = round(
        taxa,
        2,
    )

    return dados_calculados
