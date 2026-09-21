from datetime import datetime

from calculos import (
    validar_nao_negativo,
    validar_maior_que_zero,
    calcular_razao_mortas_extraidas,
)


# ============================================================
# VALIDAÇÃO DO TURNO
# ============================================================

def validar_turno(turno):
    """
    Garante que o turno informado seja válido.
    """
    turnos_validos = [
        "Manhã",
        "Tarde",
    ]

    if turno not in turnos_validos:
        raise ValueError(
            "O turno deve ser 'Manhã' ou 'Tarde'."
        )

    return turno


# ============================================================
# CÁLCULO DA PÓS-EXTRAÇÃO
# ============================================================

def calcular_pos_extracao(dados):
    """
    Calcula os indicadores da etapa de pós-extração.

    A comparação entre aranhas mortas e aranhas extraídas
    deve respeitar o mesmo turno.

    Exemplo:

    mortas da manhã /
    extraídas da manhã no registro anterior

    mortas da tarde /
    extraídas da tarde no registro anterior
    """

    turno = validar_turno(
        dados["turno"]
    )

    mortas = validar_nao_negativo(
        dados["mortas"],
        "aranhas mortas",
    )

    extraidas_turno_anterior = validar_maior_que_zero(
        dados["extraidas_turno_anterior"],
        (
            "aranhas extraídas do turno "
            "correspondente no registro anterior"
        ),
    )

    temperatura = validar_nao_negativo(
        dados["temperatura"],
        "temperatura",
    )

    umidade = validar_nao_negativo(
        dados["umidade"],
        "umidade",
    )

    razao = calcular_razao_mortas_extraidas(
        mortas,
        extraidas_turno_anterior,
    )

    percentual = razao * 100

    resultado = dict(dados)

    resultado.update({
        "id_registro": dados.get(
            "id_registro",
            datetime.now().strftime(
                "POS-%Y%m%d%H%M%S%f"
            ),
        ),
        "turno": turno,
        "mortas": mortas,
        "extraidas_turno_anterior": (
            extraidas_turno_anterior
        ),
        "temperatura": temperatura,
        "umidade": umidade,
        "razao_mortas_extraidas": round(
            razao,
            6,
        ),
        "percentual_mortas_extraidas": round(
            percentual,
            2,
        ),
    })

    return resultado


# ============================================================
# EXECUÇÃO INTERATIVA DO SCRIPT
# ============================================================

def solicitar_numero(prompt):
    """
    Solicita um número ao usuário.
    Aceita ponto ou vírgula como separador decimal.
    """
    while True:
        try:
            valor = input(prompt)
            return float(
                valor.replace(",", ".")
            )

        except ValueError:
            print(
                "Digite um número válido. "
                "Exemplo: 10 ou 10,5."
            )


def solicitar_inteiro(prompt):
    """
    Solicita um número inteiro ao usuário.
    """
    while True:
        try:
            return int(input(prompt))

        except ValueError:
            print(
                "Digite um número inteiro válido."
            )


def executar_teste_interativo():
    """
    Permite testar a etapa de pós-extração
    diretamente pelo terminal.
    """
    print("==============================================")
    print("CÁLCULO DA PÓS-EXTRAÇÃO")
    print("==============================================")

    id_lote = input(
        "Informe o ID do lote: "
    ).strip()

    data = input(
        "Informe a data do procedimento: "
    ).strip()

    ciclo = input(
        "Informe o ciclo de extração: "
    ).strip()

    while True:
        turno = input(
            "Informe o turno (Manhã/Tarde): "
        ).strip()

        try:
            validar_turno(turno)
            break

        except ValueError as erro:
            print(erro)

    responsavel = input(
        "Informe o responsável técnico: "
    ).strip()

    mortas = solicitar_inteiro(
        "Aranhas mortas no turno: "
    )

    extraidas_turno_anterior = solicitar_inteiro(
        "Aranhas extraídas no mesmo turno "
        "do registro anterior: "
    )

    temperatura = solicitar_numero(
        "Temperatura (°C): "
    )

    umidade = solicitar_numero(
        "Umidade (%): "
    )

    dados = {
        "id_lote": id_lote,
        "data": data,
        "ciclo": ciclo,
        "turno": turno,
        "responsavel": responsavel,
        "mortas": mortas,
        "extraidas_turno_anterior": (
            extraidas_turno_anterior
        ),
        "temperatura": temperatura,
        "umidade": umidade,
    }

    try:
        resultado = calcular_pos_extracao(
            dados
        )

        print()
        print("Pós-extração calculada com sucesso!")
        print()
        print(
            f"Turno: {resultado['turno']}"
        )
        print(
            "Razão entre mortas e extraídas: "
            f"{resultado['razao_mortas_extraidas']:.6f}"
        )
        print(
            "Percentual de mortas em relação "
            "às extraídas: "
            f"{resultado['percentual_mortas_extraidas']:.2f}%"
        )
        print(
            f"Temperatura: "
            f"{resultado['temperatura']:.2f} °C"
        )
        print(
            f"Umidade: "
            f"{resultado['umidade']:.2f}%"
        )

        return resultado

    except ValueError as erro:
        print()
        print(
            "Não foi possível calcular a pós-extração."
        )
        print(f"Corrija o campo: {erro}")


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    executar_teste_interativo()
