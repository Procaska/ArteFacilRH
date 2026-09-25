from pathlib import Path

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

from services.aniversarios import (
    buscar_aniversariantes,
    carregar_planilha,
    dividir_em_artes,
    preparar_dados_canva,
    gerar_csv,
)



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

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.caminho_planilha = None
        self.df = None

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

        logo = QLabel("🎨")
        logo.setObjectName("logo")

        bloco_titulo = QVBoxLayout()
        bloco_titulo.setSpacing(2)

        titulo = QLabel("ArteFácil RH")
        titulo.setObjectName("titulo")

        subtitulo = QLabel(
            "Automação de artes para comunicação interna"
        )
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

        titulo_secao = QLabel("Preparar artes")
        titulo_secao.setObjectName("tituloSecao")

        descricao = QLabel(
            "Transforme sua planilha em dados prontos para o Canva."
        )
        descricao.setObjectName("descricao")

        layout.addWidget(titulo_secao)
        layout.addWidget(descricao)

        # =====================================================
        # CARD PLANILHA
        # =====================================================

        card_planilha = self.criar_card()

        layout_planilha = QVBoxLayout(card_planilha)
        layout_planilha.setContentsMargins(22, 20, 22, 20)
        layout_planilha.setSpacing(14)

        titulo_planilha = QLabel("📊  PLANILHA")
        titulo_planilha.setObjectName("tituloCard")

        layout_planilha.addWidget(titulo_planilha)

        linha_planilha = QHBoxLayout()
        linha_planilha.setSpacing(15)

        self.icone_arquivo = QLabel("📄")
        self.icone_arquivo.setObjectName("iconeArquivo")

        bloco_arquivo = QVBoxLayout()
        bloco_arquivo.setSpacing(3)

        self.label_arquivo = QLabel(
            "Nenhuma planilha selecionada"
        )
        self.label_arquivo.setObjectName("nomeArquivo")

        self.label_detalhe = QLabel(
            "Selecione a cópia da planilha fornecida pelo RH"
        )
        self.label_detalhe.setObjectName("detalheArquivo")

        bloco_arquivo.addWidget(self.label_arquivo)
        bloco_arquivo.addWidget(self.label_detalhe)

        botao_arquivo = QPushButton("Alterar")
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
        self.card_aniversarios = QFrame()
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

        selecionado = QLabel("●  SELECIONADO")
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
        layout_aniversarios.addWidget(
            selecionado
        )

        # TEMPO DE CASA
        self.card_tempo = QFrame()
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
            "Em breve"
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
            "✨   PREPARAR PARA O CANVA"
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

        status_titulo = QLabel("PRONTO")
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
            "ArteFácil RH  •  Preparação de dados para Canva"
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

            df = carregar_planilha(caminho)

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

    mes = self.combo_mes.currentData()

    try:
        aniversariantes = buscar_aniversariantes(
            self.df,
            mes,
        )

        if aniversariantes.empty:
            self.status.setText(
                f"Nenhum aniversariante encontrado em {MESES[mes]}."
            )

            QMessageBox.information(
                self,
                "Nenhum aniversariante",
                f"Nenhum aniversariante encontrado em "
                f"{MESES[mes]}.",
            )

            return

        artes = dividir_em_artes(
            aniversariantes
        )

        df_canva = preparar_dados_canva(
            artes,
            mes,
        )

        caminho_saida = (
            Path("saida")
            / f"aniversariantes_{MESES[mes].lower()}.csv"
        )

        arquivo = gerar_csv(
            df_canva,
            caminho_saida,
        )

        quantidade = len(aniversariantes)
        quantidade_artes = len(artes)

        self.status.setText(
            f"{quantidade} aniversariante(s) encontrados. "
            f"{quantidade_artes} arte(s) preparada(s)."
        )

        QMessageBox.information(
            self,
            "Processamento concluído",
            f"{quantidade} aniversariante(s) encontrados.\n\n"
            f"{quantidade_artes} arte(s) preparada(s).\n\n"
            f"Arquivo gerado em:\n{arquivo}",
        )

    except Exception as erro:

        QMessageBox.critical(
            self,
            "Erro ao preparar dados",
            str(erro),
        )

        if self.df is None:

            QMessageBox.warning(
                self,
                "Planilha não selecionada",
                "Selecione a planilha antes de continuar.",
            )

            return

        mes = self.combo_mes.currentData()

        aniversariantes = buscar_aniversariantes(
            self.df,
            mes,
        )

        quantidade = len(
            aniversariantes
        )

        self.status.setText(
            f"{quantidade} aniversariante(s) "
            f"encontrado(s) em {MESES[mes]}."
        )

        QMessageBox.information(
            self,
            "Aniversários encontrados",
            f"Foram encontrados {quantidade} "
            f"aniversariante(s) em "
            f"{MESES[mes]}.",
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
                background: #0F1115;
            }

            QWidget#central {
                background: #0F1115;
            }

            QLabel {
                color: #F5F7FA;
            }


            /* =============================================
               CABEÇALHO
            ============================================= */

            QLabel#logo {
                font-size: 34px;
            }

            QLabel#titulo {
                color: #F5F7FA;
                font-size: 25px;
                font-weight: 700;
            }

            QLabel#subtitulo {
                color: #8F96A5;
                font-size: 13px;
            }

            QLabel#statusHeader {
                color: #35D07F;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }


            /* =============================================
               TÍTULOS
            ============================================= */

            QLabel#tituloSecao {
                color: #F5F7FA;
                font-size: 27px;
                font-weight: 700;
                margin-top: 8px;
            }

            QLabel#descricao {
                color: #858C9B;
                font-size: 14px;
            }

            QLabel#tituloGrupo {
                color: #777F90;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
                margin-top: 5px;
            }


            /* =============================================
               CARDS
            ============================================= */

            QFrame#card {
                background: #171A21;
                border: 1px solid #292E38;
                border-radius: 14px;
            }

            QFrame#cardStatus {
                background: #14181E;
                border: 1px solid #252B34;
                border-radius: 10px;
            }

            QLabel#tituloCard {
                color: #AEB5C3;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }


            /* =============================================
               ARQUIVO
            ============================================= */

            QLabel#iconeArquivo {
                background: #20242D;
                border-radius: 10px;
                padding: 12px;
                font-size: 22px;
            }

            QLabel#nomeArquivo {
                color: #F5F7FA;
                font-size: 15px;
                font-weight: 600;
            }

            QLabel#detalheArquivo {
                color: #777F90;
                font-size: 12px;
            }


            /* =============================================
               BOTÕES
            ============================================= */

            QPushButton#botaoSecundario {
                background: #20242D;
                color: #C8CDD7;
                border: 1px solid #303642;
                border-radius: 8px;
                padding: 9px 18px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#botaoSecundario:hover {
                background: #292E38;
                border-color: #414857;
            }


            /* =============================================
               TIPOS DE ARTE
            ============================================= */

            QFrame#cardTipoSelecionado {
                background: #191722;
                border: 1px solid #7C5CFC;
                border-radius: 14px;
            }

            QFrame#cardTipoSelecionado:hover {
                background: #211D32;
                border-color: #9278FF;
            }

            QFrame#cardTipo {
                background: #15181E;
                border: 1px solid #252A33;
                border-radius: 14px;
            }

            QLabel#iconeTipo {
                font-size: 25px;
            }

            QLabel#nomeTipo {
                color: #F5F7FA;
                font-size: 16px;
                font-weight: 700;
            }

            QLabel#detalheTipo {
                color: #7D8595;
                font-size: 12px;
            }

            QLabel#selecionado {
                color: #9A82FF;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }


            /* =============================================
               COMBOBOX
            ============================================= */

            QComboBox {
                background: #171A21;
                color: #E7EAF0;
                border: 1px solid #292E38;
                border-radius: 9px;
                padding: 12px 15px;
                font-size: 14px;
                min-height: 20px;
            }

            QComboBox:hover {
                border-color: #414857;
            }

            QComboBox:focus {
                border-color: #7C5CFC;
            }

            QComboBox::drop-down {
                border: none;
                width: 35px;
            }

            QComboBox QAbstractItemView {
                background: #191D24;
                color: #F5F7FA;
                border: 1px solid #303642;
                selection-background-color: #7C5CFC;
                selection-color: white;
                padding: 5px;
            }


            /* =============================================
               BOTÃO PRINCIPAL
            ============================================= */

            QPushButton#botaoPrincipal {
                background: #7C5CFC;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }

            QPushButton#botaoPrincipal:hover {
                background: #8D72FF;
            }

            QPushButton#botaoPrincipal:pressed {
                background: #6949E8;
            }


            /* =============================================
               STATUS
            ============================================= */

            QLabel#indicadorStatus {
                color: #35D07F;
                font-size: 13px;
            }

            QLabel#statusTitulo {
                color: #35D07F;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#statusTexto {
                color: #858C9B;
                font-size: 12px;
            }


            /* =============================================
               RODAPÉ
            ============================================= */

            QLabel#rodape {
                color: #555D6C;
                font-size: 10px;
            }

            """
        ) #teste