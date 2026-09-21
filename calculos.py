from typing import Optional


def validar_nao_negativo(valor, nome):
    """
    Verifica se um valor numérico não é negativo.
    """
    try:
        valor = float(str(valor).replace(",", "."))
    except (ValueError, TypeError):
        raise ValueError(
            f"O campo '{nome}' deve conter um número válido."
        )

    if valor < 0:
        raise ValueError(
            f"O campo '{nome}' não pode ser negativo."
        )

    return valor


def validar_maior_que_zero(valor, nome):
    """
    Verifica se um valor numérico é maior que zero.
    """
    valor = validar_nao_negativo(valor, nome)

    if valor <= 0:
        raise ValueError(
            f"O campo '{nome}' deve ser maior que zero."
        )

    return valor


def calcular_total_aranhas(
    vivas_extraidas,
    vivas_nao_extraidas,
    mortas,
):
    """
    Calcula o total de aranhas registradas.
    """
    vivas_extraidas = validar_nao_negativo(
        vivas_extraidas,
        "aranhas vivas extraídas",
    )

    vivas_nao_extraidas = validar_nao_negativo(
        vivas_nao_extraidas,
        "aranhas vivas não extraídas",
    )

    mortas = validar_nao_negativo(
        mortas,
        "aranhas mortas",
    )

    return (
        vivas_extraidas +
        vivas_nao_extraidas +
        mortas
    )


def calcular_percentual_extraidas(
    vivas_extraidas,
    vivas_nao_extraidas,
):
    """
    Calcula o percentual de aranhas vivas extraídas.

    Fórmula:

    vivas extraídas /
    total de vivas × 100
    """
    vivas_extraidas = validar_nao_negativo(
        vivas_extraidas,
        "aranhas vivas extraídas",
    )

    vivas_nao_extraidas = validar_nao_negativo(
        vivas_nao_extraidas,
        "aranhas vivas não extraídas",
    )

    total_vivas = (
        vivas_extraidas +
        vivas_nao_extraidas
    )

    if total_vivas <= 0:
        raise ValueError(
            "O total de aranhas vivas deve ser maior que zero."
        )

    return (
        vivas_extraidas /
        total_vivas
    ) * 100


def calcular_taxa_mortalidade(
    vivas_extraidas,
    vivas_nao_extraidas,
    mortas,
):
    """
    Calcula a taxa de mortalidade considerando
    toda a população registrada.
    """
    total = calcular_total_aranhas(
        vivas_extraidas,
        vivas_nao_extraidas,
        mortas,
    )

    if total <= 0:
        raise ValueError(
            "O total de aranhas deve ser maior que zero."
        )

    return (
        mortas /
        total
    ) * 100


def calcular_veneno_manha(
    peso_frasco_vazio_g,
    peso_frasco_manha_g,
):
    """
    Calcula o veneno produzido pela manhã.

    Fórmula:

    peso do frasco pela manhã -
    peso do frasco vazio
    """
    peso_frasco_vazio_g = validar_nao_negativo(
        peso_frasco_vazio_g,
        "peso do frasco vazio",
    )

    peso_frasco_manha_g = validar_nao_negativo(
        peso_frasco_manha_g,
        "peso do frasco pela manhã",
    )

    veneno_manha = (
        peso_frasco_manha_g -
        peso_frasco_vazio_g
    )

    if veneno_manha < 0:
        raise ValueError(
            "O peso do frasco pela manhã não pode "
            "ser menor que o peso do frasco vazio."
        )

    return veneno_manha


def calcular_veneno_tarde(
    peso_frasco_manha_g,
    peso_frasco_tarde_g,
):
    """
    Calcula o veneno produzido à tarde.

    O mesmo frasco é utilizado nos dois períodos.

    Fórmula:

    peso do frasco à tarde -
    peso do frasco pela manhã
    """
    peso_frasco_manha_g = validar_nao_negativo(
        peso_frasco_manha_g,
        "peso do frasco pela manhã",
    )

    peso_frasco_tarde_g = validar_nao_negativo(
        peso_frasco_tarde_g,
        "peso do frasco à tarde",
    )

    veneno_tarde = (
        peso_frasco_tarde_g -
        peso_frasco_manha_g
    )

    if veneno_tarde < 0:
        raise ValueError(
            "O peso do frasco à tarde não pode "
            "ser menor que o peso do frasco pela manhã."
        )

    return veneno_tarde


def calcular_veneno_total(
    veneno_manha_g,
    veneno_tarde_g,
):
    """
    Calcula o total de veneno bruto produzido.
    """
    veneno_manha_g = validar_nao_negativo(
        veneno_manha_g,
        "veneno da manhã",
    )

    veneno_tarde_g = validar_nao_negativo(
        veneno_tarde_g,
        "veneno da tarde",
    )

    return veneno_manha_g + veneno_tarde_g


def calcular_media_voltagem(
    voltagem_inicio,
    voltagem_meio,
    voltagem_fim,
):
    """
    Calcula a média das três medições de voltagem.
    """
    valores = [
        validar_nao_negativo(
            voltagem_inicio,
            "voltagem inicial",
        ),
        validar_nao_negativo(
            voltagem_meio,
            "voltagem do meio",
        ),
        validar_nao_negativo(
            voltagem_fim,
            "voltagem final",
        ),
    ]

    return sum(valores) / len(valores)


def calcular_media_por_aranha(
    veneno_g,
    quantidade_extraida,
):
    """
    Calcula a média de veneno por aranha.

    O resultado é retornado em gramas por aranha.
    """
    veneno_g = validar_nao_negativo(
        veneno_g,
        "veneno produzido",
    )

    quantidade_extraida = validar_maior_que_zero(
        quantidade_extraida,
        "quantidade extraída",
    )

    return veneno_g / quantidade_extraida


def calcular_razao_mortas_extraidas(
    mortas,
    extraidas_turno_anterior,
):
    """
    Calcula a razão entre aranhas mortas e aranhas
    extraídas no turno correspondente do dia anterior.
    """
    mortas = validar_nao_negativo(
        mortas,
        "aranhas mortas",
    )

    extraidas_turno_anterior = validar_maior_que_zero(
        extraidas_turno_anterior,
        "aranhas extraídas do turno anterior",
    )

    return mortas / extraidas_turno_anterior


def calcular_rendimento_liofilizacao(
    veneno_bruto_g,
    veneno_liofilizado_ug,
):
    """
    Calcula o percentual de recuperação após a liofilização.

    O veneno bruto é convertido de gramas para microgramas:

    1 g = 1.000.000 µg
    """
    veneno_bruto_g = validar_maior_que_zero(
        veneno_bruto_g,
        "veneno bruto",
    )

    veneno_liofilizado_ug = validar_nao_negativo(
        veneno_liofilizado_ug,
        "veneno liofilizado",
    )

    veneno_bruto_ug = (
        veneno_bruto_g * 1_000_000
    )

    return (
        veneno_liofilizado_ug /
        veneno_bruto_ug
    ) * 100
