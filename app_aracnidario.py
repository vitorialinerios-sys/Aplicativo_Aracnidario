from pathlib import Path
from datetime import date, datetime
import csv

import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output


# ============================================================
# CONFIGURAÇÃO DOS ARQUIVOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"
LOTES_FILE = DADOS_DIR / "lotes.csv"

DADOS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURAÇÃO DAS ESPÉCIES
# ============================================================

ESPECIES = [
    "L. gaucho",
    "L. intermedia",
    "L. laeta",
]


# ============================================================
# FUNÇÕES DE PERSISTÊNCIA
# ============================================================

def criar_arquivo_lotes():
    """
    Cria o arquivo de lotes caso ele ainda não exista.
    """
    if not LOTES_FILE.exists():
        with open(
            LOTES_FILE,
            "w",
            newline="",
            encoding="utf-8",
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=[
                    "id_lote",
                    "lote",
                    "especie",
                    "total_aranhas",
                    "data_chegada",
                    "responsavel",
                ],
            )
            escritor.writeheader()


def gerar_id_lote():
    """
    Gera um identificador único para o lote.
    """
    return datetime.now().strftime(
        "LOTE-%Y%m%d%H%M%S%f"
    )


def salvar_lote(dados):
    """
    Salva um lote no arquivo lotes.csv.
    """
    criar_arquivo_lotes()

    with open(
        LOTES_FILE,
        "a",
        newline="",
        encoding="utf-8",
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=[
                "id_lote",
                "lote",
                "especie",
                "total_aranhas",
                "data_chegada",
                "responsavel",
            ],
        )
        escritor.writerow(dados)


def carregar_lotes():
    """
    Carrega os lotes cadastrados.
    """
    criar_arquivo_lotes()

    try:
        return pd.read_csv(LOTES_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


# ============================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================

def validar_texto(valor, nome):
    """
    Verifica se um campo de texto foi preenchido.
    """
    if valor is None or not str(valor).strip():
        raise ValueError(
            f"O campo '{nome}' deve ser preenchido."
        )

    return str(valor).strip()


def validar_inteiro(valor, nome):
    """
    Verifica se um valor é um inteiro não negativo.
    """
    try:
        valor = int(valor)
    except (ValueError, TypeError):
        raise ValueError(
            f"O campo '{nome}' deve ser um número inteiro."
        )

    if valor < 0:
        raise ValueError(
            f"O campo '{nome}' não pode ser negativo."
        )

    return valor


# ============================================================
# EVENTO DE SALVAMENTO DO LOTE
# ============================================================

def salvar_lote_clicado(botao):
    """
    Executado quando o usuário clica em Salvar lote.
    """
    with cadastro_saida:
        clear_output()

        try:
            especie = validar_texto(
                especie_widget.value,
                "espécie",
            )

            lote = validar_texto(
                lote_widget.value,
                "lote",
            )

            responsavel = validar_texto(
                responsavel_widget.value,
                "responsável",
            )

            if data_widget.value is None:
                raise ValueError(
                    "Selecione a data de chegada."
                )

            vivas = validar_inteiro(
                vivas_widget.value,
                "aranhas vivas",
            )

            mortas = validar_inteiro(
                mortas_widget.value,
                "aranhas mortas",
            )

            total = vivas + mortas

            if total <= 0:
                raise ValueError(
                    "O total de aranhas deve ser maior que zero."
                )

            dados = {
                "id_lote": gerar_id_lote(),
                "lote": lote,
                "especie": especie,
                "total_aranhas": total,
                "data_chegada": str(
                    data_widget.value
                ),
                "responsavel": responsavel,
            }

            salvar_lote(dados)

            print("Lote salvo com sucesso!")
            print(f"Identificador: {dados['id_lote']}")
            print(f"Lote: {lote}")
            print(f"Espécie: {especie}")
            print(f"Total de aranhas: {total}")

            atualizar_tabela_lotes()

        except ValueError as erro:
            print("Não foi possível salvar o lote.")
            print(f"Corrija o campo: {erro}")

        except Exception as erro:
            print("Ocorreu um erro inesperado.")
            print(f"Detalhes: {erro}")


# ============================================================
# TELA DE LOTES CADASTRADOS
# ============================================================

def atualizar_tabela_lotes():
    """
    Atualiza a tabela de lotes cadastrados.
    """
    with lotes_saida:
        clear_output()

        tabela = carregar_lotes()

        if tabela.empty:
            print("Nenhum lote cadastrado.")
            return

        colunas = [
            "id_lote",
            "lote",
            "especie",
            "total_aranhas",
        ]

        display(tabela[colunas])


def atualizar_calendario():
    """
    Exibe a aba de calendário.
    As datas de extração e alimentação serão preenchidas
    quando as respectivas etapas forem registradas.
    """
    with calendario_saida:
        clear_output()

        tabela = carregar_lotes()

        if tabela.empty:
            print("Nenhum lote cadastrado.")
            return

        tabela["ultima_extracao"] = ""
        tabela["proxima_extracao"] = ""
        tabela["ultima_alimentacao"] = ""
        tabela["proxima_alimentacao"] = ""

        colunas = [
            "lote",
            "especie",
            "data_chegada",
            "ultima_extracao",
            "proxima_extracao",
            "ultima_alimentacao",
            "proxima_alimentacao",
        ]

        display(tabela[colunas])


# ============================================================
# WIDGETS DA TELA DE CADASTRO
# ============================================================

titulo = widgets.HTML(
    "<h1>Centro de Produção e Pesquisa de Imunobiológicos</h1>"
)

subtitulo = widgets.HTML(
    "<h2>Aplicativo de Coleta de Dados do Aracnidário</h2>"
)

cadastro_titulo = widgets.HTML(
    "<h3>Cadastro de lote</h3>"
)

especie_widget = widgets.ToggleButtons(
    options=ESPECIES,
    description="Espécie:",
)

lote_widget = widgets.Text(
    description="Lote:",
    placeholder="Informe o código do lote",
)

data_widget = widgets.DatePicker(
    description="Chegada:",
    value=date.today(),
)

responsavel_widget = widgets.Text(
    description="Responsável:",
    placeholder="Nome do responsável",
)

vivas_widget = widgets.IntText(
    description="Vivas:",
    value=0,
    min=0,
)

mortas_widget = widgets.IntText(
    description="Mortas:",
    value=0,
    min=0,
)

salvar_button = widgets.Button(
    description="Salvar lote",
    button_style="success",
    icon="save",
)

cadastro_saida = widgets.Output()
lotes_saida = widgets.Output()
calendario_saida = widgets.Output()

salvar_button.on_click(
    salvar_lote_clicado
)


# ============================================================
# ABAS DO APLICATIVO
# ============================================================

aba_cadastro = widgets.VBox([
    cadastro_titulo,
    especie_widget,
    lote_widget,
    data_widget,
    responsavel_widget,
    vivas_widget,
    mortas_widget,
    salvar_button,
    cadastro_saida,
])

aba_lotes = widgets.VBox([
    widgets.HTML("<h3>Lotes cadastrados</h3>"),
    lotes_saida,
])

aba_calendario = widgets.VBox([
    widgets.HTML("<h3>Calendário</h3>"),
    widgets.HTML(
        """
        <p>
        Esta tela apresentará as datas de chegada,
        última e próxima extração e última e próxima
        alimentação.
        </p>
        """
    ),
    calendario_saida,
])

aba_pre_extracao = widgets.VBox([
    widgets.HTML("<h3>Pré-extração</h3>"),
    widgets.HTML(
        """
        <p>
        Nesta etapa serão incluídos os cálculos de
        percentual de extraídas, taxa de mortalidade,
        peso do veneno, temperatura, umidade e voltagem.
        </p>
        """
    ),
])

aba_pos_extracao = widgets.VBox([
    widgets.HTML("<h3>Pós-extração</h3>"),
    widgets.HTML(
        """
        <p>
        Nesta etapa será registrada a razão entre
        aranhas mortas e aranhas extraídas no turno
        correspondente do dia anterior.
        </p>
        """
    ),
])

aba_manutencao = widgets.VBox([
    widgets.HTML("<h3>Manutenção</h3>"),
    widgets.HTML(
        """
        <p>
        Nesta etapa serão registrados os dados de
        manutenção e calculada a taxa de mortalidade.
        </p>
        """
    ),
])

aba_liofilizacao = widgets.VBox([
    widgets.HTML("<h3>Liofilização</h3>"),
    widgets.HTML(
        """
        <p>
        Nesta etapa será selecionado o lote e registrado
        o peso do veneno liofilizado.
        </p>
        """
    ),
])

aba_relatorios = widgets.VBox([
    widgets.HTML("<h3>Relatórios</h3>"),
    widgets.HTML(
        """
        <p>
        Os relatórios serão gerados a partir dos dados
        registrados nas etapas do processo.
        </p>
        """
    ),
])

abas = widgets.Tab(
    children=[
        aba_cadastro,
        aba_lotes,
        aba_calendario,
        aba_pre_extracao,
        aba_pos_extracao,
        aba_manutencao,
        aba_liofilizacao,
        aba_relatorios,
    ]
)

abas.set_title(0, "Cadastro")
abas.set_title(1, "Lotes")
abas.set_title(2, "Calendário")
abas.set_title(3, "Pré-extração")
abas.set_title(4, "Pós-extração")
abas.set_title(5, "Manutenção")
abas.set_title(6, "Liofilização")
abas.set_title(7, "Relatórios")


# ============================================================
# EXIBIÇÃO INICIAL DO APLICATIVO
# ============================================================

criar_arquivo_lotes()

display(titulo)
display(subtitulo)
display(abas)

atualizar_tabela_lotes()
atualizar_calendario()
