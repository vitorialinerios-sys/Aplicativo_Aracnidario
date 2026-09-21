#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

ETAPA="$1"

case "$ETAPA" in

    pre-extracao)
        python3 "$BASE_DIR/calcular_pre_extracao.py"
        ;;

    pos-extracao)
        python3 "$BASE_DIR/calcular_pos_extracao.py"
        ;;

    manutencao)
        python3 "$BASE_DIR/calcular_manutencao.py"
        ;;

    liofilizacao)
        python3 "$BASE_DIR/calcular_liofilizacao.py"
        ;;

    *)
        echo "Etapa inválida."
        echo ""
        echo "Use:"
        echo "./executar_calculos.sh pre-extracao"
        echo "./executar_calculos.sh pos-extracao"
        echo "./executar_calculos.sh manutencao"
        echo "./executar_calculos.sh liofilizacao"
        exit 1
        ;;

esac
