from pathlib import Path
from datetime import datetime
from ui.preview_window import PreviewWindow
from ui.preview_tempo_window import PreviewTempoCasaWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from services.tempo_de_casa import buscar_marcos

from services.aniversarios import (
    buscar_aniversariantes,
    carregar_planilha,
    dividir_em_artes,
    preparar_dados_canva,
    gerar_csv,
)
from services.leitor_oficial import carregar_planilha_oficial


MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


class CardTipo(QFrame):
    
    def __init__(self, tipo, callback, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.callback = callback
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback(self.tipo)
        super().mousePressEvent(event)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.caminho_planilha = None
        self.df = None
        self.tipo_arte = "aniversarios"

        self.setWindowTitle("ArteFácil RH")
        self.setMinimumSize(920, 700)
        self.resize(1000, 760)

        self.criar_interface()
        self.aplicar_estilo()

    # =========================================================
    # INTERFACE
    # =========================================================

    def criar_interface(self):

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(36, 30, 36, 30)
        layout.setSpacing(14)

        # =====================================================
        # CABEÇALHO
        # =====================================================

        header = QHBoxLayout()
        header.setSpacing(14)

        logo = QLabel("🔴")
        logo.setObjectName("logo")

        bloco_titulo = QVBoxLayout()
        bloco_titulo.setSpacing(2)

        titulo = QLabel("ArteFácil RH")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Transforme sua planilha em dados prontos para o Canva.")
        subtitulo.setObjectName("subtitulo")

        bloco_titulo.addWidget(titulo)
        bloco_titulo.addWidget(subtitulo)

        header.addWidget(logo)
        header.addLayout(bloco_titulo)
        header.addStretch()

        status_header = QLabel("●  ONLINE")
        status_header.setObjectName("statusHeader")

        header.addWidget(status_header)

        layout.addLayout(header)

        # =====================================================
        # TÍTULO DA SEÇÃO
        # =====================================================

    

        descricao = QLabel()
        descricao.setObjectName("descricao")

        layout.addWidget(descricao)

        # =====================================================
        # CARD PLANILHA
        # =====================================================

        card_planilha = self.criar_card()

        layout_planilha = QVBoxLayout(card_planilha)
        layout_planilha.setContentsMargins(22, 20, 22, 20)
        layout_planilha.setSpacing(14)

        titulo_planilha = QLabel("PLANILHA")
        titulo_planilha.setObjectName("tituloCard")

        layout_planilha.addWidget(titulo_planilha)

        linha_planilha = QHBoxLayout()
        linha_planilha.setSpacing(15)

        self.icone_arquivo = QLabel("📄")
        self.icone_arquivo.setObjectName("iconeArquivo")

        bloco_arquivo = QVBoxLayout()
        bloco_arquivo.setSpacing(3)

        self.label_arquivo = QLabel(
            "Nenhum arquivo anexado"
        )
        self.label_arquivo.setObjectName("nomeArquivo")

        self.label_detalhe = QLabel(
            "Selecione a cópia da planilha fornecida pelo RH"
        )
        self.label_detalhe.setObjectName("detalheArquivo")

        bloco_arquivo.addWidget(self.label_arquivo)
        bloco_arquivo.addWidget(self.label_detalhe)

        botao_arquivo = QPushButton("Importar")
        botao_arquivo.setObjectName("botaoSecundario")
        botao_arquivo.setCursor(Qt.CursorShape.PointingHandCursor)

        botao_arquivo.clicked.connect(
            self.selecionar_planilha
        )

        linha_planilha.addWidget(self.icone_arquivo)
        linha_planilha.addLayout(bloco_arquivo)
        linha_planilha.addStretch()
        linha_planilha.addWidget(botao_arquivo)

        layout_planilha.addLayout(linha_planilha)

        layout.addWidget(card_planilha)

        # =====================================================
        # TIPO DE ARTE
        # =====================================================

        titulo_tipo = QLabel("TIPO DE ARTE")
        titulo_tipo.setObjectName("tituloGrupo")

        layout.addWidget(titulo_tipo)

        linha_tipos = QHBoxLayout()
        linha_tipos.setSpacing(15)

        # ANIVERSÁRIOS
        self.card_aniversarios = CardTipo("aniversarios", self.selecionar_tipo_arte)
        self.card_aniversarios.setObjectName(
            "cardTipoSelecionado"
        )
        self.card_aniversarios.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        layout_aniversarios = QVBoxLayout(
            self.card_aniversarios
        )
        layout_aniversarios.setContentsMargins(
            22, 20, 22, 20
        )
        layout_aniversarios.setSpacing(6)

        icone_aniversario = QLabel("🎂")
        icone_aniversario.setObjectName("iconeTipo")

        nome_aniversario = QLabel("Aniversários")
        nome_aniversario.setObjectName("nomeTipo")

        detalhe_aniversario = QLabel(
            "Artes de aniversário"
        )
        detalhe_aniversario.setObjectName(
            "detalheTipo"
        )

        selecionado = QLabel()
        selecionado.setObjectName("selecionado")

        layout_aniversarios.addWidget(
            icone_aniversario
        )
        layout_aniversarios.addWidget(
            nome_aniversario
        )
        layout_aniversarios.addWidget(
            detalhe_aniversario
        )
        layout_aniversarios.addSpacing(5)

        # TEMPO DE CASA
        self.card_tempo = CardTipo("tempo", self.selecionar_tipo_arte)
        self.card_tempo.setObjectName("cardTipo")
        self.card_tempo.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        layout_tempo = QVBoxLayout(
            self.card_tempo
        )
        layout_tempo.setContentsMargins(
            22, 20, 22, 20
        )
        layout_tempo.setSpacing(6)

        icone_tempo = QLabel("🏆")
        icone_tempo.setObjectName("iconeTipo")

        nome_tempo = QLabel("Tempo de casa")
        nome_tempo.setObjectName("nomeTipo")

        detalhe_tempo = QLabel(
            "Artes de tempo de casa"
        )
        detalhe_tempo.setObjectName("detalheTipo")

        layout_tempo.addWidget(icone_tempo)
        layout_tempo.addWidget(nome_tempo)
        layout_tempo.addWidget(detalhe_tempo)

        linha_tipos.addWidget(
            self.card_aniversarios,
            1,
        )

        linha_tipos.addWidget(
            self.card_tempo,
            1,
        )

        layout.addLayout(linha_tipos)

        # =====================================================
        # PERÍODO
        # =====================================================

        titulo_periodo = QLabel("PERÍODO")
        titulo_periodo.setObjectName("tituloGrupo")

        layout.addWidget(titulo_periodo)

        self.combo_mes = QComboBox()
        self.combo_mes.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        for numero, nome in MESES.items():
            self.combo_mes.addItem(
                nome,
                numero,
            )

        # Setembro como padrão
        self.combo_mes.setCurrentIndex(8)

        layout.addWidget(self.combo_mes)

        # =====================================================
        # BOTÃO PRINCIPAL
        # =====================================================

        self.botao_preparar = QPushButton(
            "PREPARAR PARA O CANVA"
        )

        self.botao_preparar.setObjectName(
            "botaoPrincipal"
        )

        self.botao_preparar.setMinimumHeight(58)
        self.botao_preparar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.botao_preparar.clicked.connect(
        self.preparar_canva     
        )

        layout.addWidget(
            self.botao_preparar
        )

        # =====================================================
        # STATUS
        # =====================================================

        card_status = self.criar_card()
        card_status.setObjectName("cardStatus")

        layout_status = QHBoxLayout(card_status)
        layout_status.setContentsMargins(
            18, 14, 18, 14
        )

        indicador = QLabel("●")
        indicador.setObjectName("indicadorStatus")

        bloco_status = QVBoxLayout()
        bloco_status.setSpacing(2)

        status_titulo = QLabel("PREPARANDO..")
        status_titulo.setObjectName(
            "statusTitulo"
        )

        self.status = QLabel(
            "Selecione uma planilha para começar."
        )
        self.status.setObjectName(
            "statusTexto"
        )

        bloco_status.addWidget(status_titulo)
        bloco_status.addWidget(self.status)

        layout_status.addWidget(indicador)
        layout_status.addLayout(bloco_status)
        layout_status.addStretch()

        layout.addWidget(card_status)

        layout.addStretch()

        # =====================================================
        # RODAPÉ
        # =====================================================

        rodape = QLabel(
            "Developed by Arthur Procaska"
        )

        rodape.setObjectName("rodape")
        rodape.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(rodape)

    # =========================================================
    # CARD
    # =========================================================

    def criar_card(self):

        card = QFrame()
        card.setObjectName("card")

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        return card

    # =========================================================
    # SELECIONAR TIPO DE ARTE
    # =========================================================

    def selecionar_tipo_arte(self, tipo):
        self.tipo_arte = tipo

        if tipo == "aniversarios":
            self.card_aniversarios.setObjectName("cardTipoSelecionado")
            self.card_tempo.setObjectName("cardTipo")
        else:
            self.card_aniversarios.setObjectName("cardTipo")
            self.card_tempo.setObjectName("cardTipoSelecionado")

        for card in (self.card_aniversarios, self.card_tempo):
            card.style().unpolish(card)
            card.style().polish(card)
            card.update()
        # Tempo de casa usa sempre o mês atual; o seletor de mês fica
        # disponível apenas para Aniversários.
        self.combo_mes.setEnabled(tipo == "aniversarios")

    # =========================================================
    # SELECIONAR PLANILHA
    # =========================================================

    def selecionar_planilha(self):

        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar planilha",
            "",
            "Planilhas Excel (*.xlsx *.xls)",
        )

        if not caminho:
            return

        try:

            df = carregar_planilha_oficial(caminho)

            self.caminho_planilha = caminho
            self.df = df

            nome = Path(caminho).name

            self.label_arquivo.setText(
                nome
            )

            self.label_detalhe.setText(
                "Planilha Excel carregada com sucesso"
            )

            self.status.setText(
                "Planilha carregada. "
                "Selecione o período para continuar."
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro ao carregar planilha",
                str(erro),
            )

    # =========================================================
    # PREPARAR CANVA
    # =========================================================

    def preparar_canva(self):

        if self.df is None:
            QMessageBox.warning(
                self,
                "Planilha não selecionada",
                "Selecione a planilha antes de continuar.",
            )
            return

        try:
            if self.tipo_arte == "tempo":
                mes_atual = datetime.now().month
                ano_atual = datetime.now().year

                marcos = buscar_marcos(
                    self.df,
                    mes_atual,
                    ano_atual,
                )

                if marcos.empty:
                    QMessageBox.information(
                        self,
                        "Nenhum marco encontrado",
                        f"Nenhum funcionário com marco de tempo de casa em {MESES[mes_atual]}.",
                    )
                    return

                preview = PreviewTempoCasaWindow(
                    self,
                    MESES[mes_atual],
                    mes_atual,
                    marcos,
                )
                preview.exec()
                return

            mes = self.combo_mes.currentData()

            aniversariantes = buscar_aniversariantes(
                self.df,
                mes,
            )

            if aniversariantes.empty:
                QMessageBox.information(
                    self,
                    "Nenhum aniversariante",
                    f"Nenhum aniversariante encontrado em {MESES[mes]}.",
                )
                return

            artes = dividir_em_artes(aniversariantes)

            preview = PreviewWindow(
                self,
                MESES[mes],
                mes,
                aniversariantes,
                artes,
            )

            preview.exec()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao preparar dados",
                str(erro),
            )


    # =========================================================
    # ESTILO
    # =========================================================

    def aplicar_estilo(self):

        self.setStyleSheet(
"""
/* =============================================
   BASE
============================================= */

QMainWindow {
    background: #0F1012;
}

QWidget#central {
    background: #0F1012;
}

QLabel {
    color: #D6A354;
}


/* =============================================
   CABEÇALHO
============================================= */

QLabel#logo {
    font-size: 34px;
}

QLabel#titulo {
    color: #F5F5F5;
    font-size: 25px;
    font-weight: 700;
}

QLabel#subtitulo {
    color: #92969F;
    font-size: 13px;
}

QLabel#statusHeader {
    color: #43D17D;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}


/* =============================================
   TÍTULOS
============================================= */

QLabel#tituloSecao {
    color: #F5F5F5;
    font-size: 27px;
    font-weight: 700;
    margin-top: 8px;
}

QLabel#descricao {
    color: #898E98;
    font-size: 14px;
}

QLabel#tituloGrupo {
    color: #737881;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 5px;
}


/* =============================================
   CARDS
============================================= */

QFrame#card {
    background: #18191D;
    border: 1px solid #2B2D33;
    border-radius: 14px;
}

QFrame#cardStatus {
    background: #151619;
    border: 1px solid #282A2F;
    border-radius: 10px;
}

QLabel#tituloCard {
    color: #B3B6BE;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}


/* =============================================
   ARQUIVO
============================================= */

QLabel#iconeArquivo {
    background: #23252A;
    border-radius: 10px;
    padding: 12px;
    font-size: 22px;
}

QLabel#nomeArquivo {
    color: #F5F5F5;
    font-size: 15px;
    font-weight: 600;
}

QLabel#detalheArquivo {
    color: #747982;
    font-size: 12px;
}


/* =============================================
   BOTÕES
============================================= */

QPushButton#botaoSecundario {
    background: #222428;
    color: #C8CBD1;
    border: 1px solid #34363C;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#botaoSecundario:hover {
    background: #2C2E34;
    border-color: #484A51;
}


/* =============================================
   TIPOS DE ARTE
============================================= */

QFrame#cardTipoSelecionado {
    background: #241719;
    border: 1px solid #C73535;
    border-radius: 14px;
}

QFrame#cardTipoSelecionado:hover {
    background: #301A1C;
    border-color: #E04A4A;
}

QFrame#cardTipo {
    background: #16171A;
    border: 1px solid #292B30;
    border-radius: 14px;
}

QLabel#iconeTipo {
    font-size: 25px;
}

QLabel#nomeTipo {
    color: #F5F5F5;
    font-size: 16px;
    font-weight: 700;
}

QLabel#detalheTipo {
    color: #7C818A;
    font-size: 12px;
}

QLabel#selecionado {
    color: #E04A4A;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}


/* =============================================
   COMBOBOX
============================================= */

QComboBox {
    background: #18191D;
    color: #E8E9EC;
    border: 1px solid #2C2E34;
    border-radius: 9px;
    padding: 12px 15px;
    font-size: 14px;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #484A51;
}

QComboBox:focus {
    border-color: #C73535;
}

QComboBox::drop-down {
    border: none;
    width: 35px;
}

QComboBox QAbstractItemView {
    background: #1C1D21;
    color: #F5F5F5;
    border: 1px solid #35373D;
    selection-background-color: #A92525;
    selection-color: white;
    padding: 5px;
}


/* =============================================
   BOTÃO PRINCIPAL
============================================= */

QPushButton#botaoPrincipal {
    background: #A92525;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

QPushButton#botaoPrincipal:hover {
    background: #D13A3A;
}

QPushButton#botaoPrincipal:pressed {
    background: #871D1D;
}


/* =============================================
   STATUS
============================================= */

QLabel#indicadorStatus {
    color: #43D17D;
    font-size: 13px;
}

QLabel#statusTitulo {
    color: #43D17D;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#statusTexto {
    color: #898E98;
    font-size: 12px;
}


/* =============================================
   RODAPÉ
============================================= */

QLabel#rodape {
    color: #565A63;
    font-size: 10px;
}

"""
  ) #teste