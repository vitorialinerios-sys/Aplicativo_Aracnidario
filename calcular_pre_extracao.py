import sys
from calculos import (
    calcular_percentual_extraidas,
    calcular_taxa_mortalidade,
    calcular_veneno_manha,
    calcular_veneno_tarde,
    calcular_veneno_total,
    calcular_media_voltagem,
)


def calcular_pre_extracao(dados):
    """
    Executa todos os cálculos da etapa de pré-extração.
    """
    veneno_manha = calcular_veneno_manha(
        dados["peso_frasco_vazio_g"],
        dados["peso_frasco_manha_g"],
    )

    veneno_tarde = calcular_veneno_tarde(
        dados["peso_frasco_manha_g"],
        dados["peso_frasco_tarde_g"],
    )

    veneno_total = calcular_veneno_total(
        veneno_manha,
        veneno_tarde,
    )

    percentual_extraidas = calcular_percentual_extraidas(
        dados["vivas_extraidas"],
        dados["vivas_nao_extraidas"],
    )

    taxa_mortalidade = calcular_taxa_mortalidade(
        dados["vivas_extraidas"],
        dados["vivas_nao_extraidas"],
        dados["mortas"],
    )

    media_voltagem = calcular_media_voltagem(
        dados["voltagem_inicio"],
        dados["voltagem_meio"],
        dados["voltagem_fim"],
    )

    dados_calculados = dict(dados)

    dados_calculados.update({
        "veneno_manha_g": round(
            veneno_manha,
            4,
        ),
        "veneno_tarde_g": round(
            veneno_tarde,
            4,
        ),
        "veneno_total_g": round(
            veneno_total,
            4,
        ),
        "percentual_extraidas": round(
            percentual_extraidas,
            2,
        ),
        "taxa_mortalidade": round(
            taxa_mortalidade,
            2,
        ),
        "voltagem_media": round(
            media_voltagem,
            2,
        ),
    })

    return dados_calculados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Este arquivo deve ser chamado pelo aplicativo "
            "ou receber um registro para cálculo."
        )
    else:
        # Placeholder for actual data processing if run as a script.
        # For now, it just prints a message.
        print(
            "O registro de pré-extração deve ser "
            "carregado pelo aplicativo."
        )
