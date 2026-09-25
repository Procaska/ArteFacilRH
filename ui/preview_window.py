from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QWidget,
    QFileDialog,
    QMessageBox,
)

from services.aniversarios import (
    preparar_dados_canva,
    gerar_csv as gerar_csv_arquivo,
)


class PreviewWindow(QDialog):

    def __init__(
        self,
        parent,
        mes,
        mes_numero,
        aniversariantes,
        artes,
    ):
        super().__init__(parent)

        self.mes = mes
        self.mes_numero = mes_numero
        self.aniversariantes = aniversariantes
        self.artes = artes

        self.setWindowTitle("Conferir aniversários")
        self.resize(900, 700)

        self.criar_interface()
        self.aplicar_estilo()

    # =========================================================
    # INTERFACE
    # =========================================================

    def criar_interface(self):

        layout_principal = QVBoxLayout(self)

        layout_principal.setContentsMargins(
            30, 25, 30, 25
        )

        layout_principal.setSpacing(20)

        # =====================================================
        # CABEÇALHO
        # =====================================================

        titulo = QLabel(
            "Conferir aniversários"
        )

        titulo.setObjectName("titulo")

        subtitulo = QLabel(
            f"{self.mes} • "
            f"{len(self.aniversariantes)} aniversariante(s) • "
            f"{len(self.artes)} arte(s)"
        )

        subtitulo.setObjectName("subtitulo")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        # =====================================================
        # ÁREA DE SCROLL
        # =====================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        conteudo = QWidget()

        layout_conteudo = QVBoxLayout(
            conteudo
        )

        layout_conteudo.setContentsMargins(
            5, 5, 5, 5
        )

        layout_conteudo.setSpacing(20)

        # =====================================================
        # ARTES
        # =====================================================

        for numero_arte, grupo in enumerate(
            self.artes,
            start=1
        ):

            card = QFrame()

            card.setObjectName(
                "card_arte"
            )

            layout_card = QVBoxLayout(card)

            layout_card.setContentsMargins(
                20, 18, 20, 18
            )

            layout_card.setSpacing(12)

            # -----------------------------------------------
            # TÍTULO DA ARTE
            # -----------------------------------------------

            titulo_arte = QLabel(
                f"ARTE {numero_arte}"
            )

            titulo_arte.setObjectName(
                "titulo_arte"
            )

            layout_card.addWidget(
                titulo_arte
            )

            # -----------------------------------------------
            # FUNCIONÁRIOS
            # -----------------------------------------------

            for posicao, (_, funcionario) in enumerate(
                grupo.iterrows(),
                start=1
            ):

                linha = QFrame()

                linha.setObjectName(
                    "linha_funcionario"
                )

                layout_linha = QHBoxLayout(
                    linha
                )

                layout_linha.setContentsMargins(
                    12, 8, 12, 8
                )

                numero = QLabel(
                    f"{posicao:02d}"
                )

                numero.setFixedWidth(40)

                numero.setObjectName(
                    "numero"
                )

                nome = QLabel(
                    str(funcionario["Nome"])
                )

                nome.setObjectName(
                    "nome"
                )

                data = QLabel(
                    funcionario[
                        "Data de Nascimento"
                    ].strftime("%d/%m")
                )

                data.setFixedWidth(70)

                data.setAlignment(
                    Qt.AlignmentFlag.AlignRight
                )

                layout_linha.addWidget(
                    numero
                )

                layout_linha.addWidget(
                    nome
                )

                layout_linha.addStretch()

                layout_linha.addWidget(
                    data
                )

                layout_card.addWidget(
                    linha
                )

            layout_conteudo.addWidget(
                card
            )

        layout_conteudo.addStretch()

        scroll.setWidget(
            conteudo
        )

        layout_principal.addWidget(
            scroll
        )

        # =====================================================
        # BOTÕES
        # =====================================================

        layout_botoes = QHBoxLayout()

        layout_botoes.setSpacing(12)

        self.botao_voltar = QPushButton(
            "← VOLTAR"
        )

        self.botao_voltar.setObjectName(
            "botao_voltar"
        )

        self.botao_gerar = QPushButton(
            "GERAR CSV →"
        )

        self.botao_gerar.setObjectName(
            "botao_gerar"
        )

        layout_botoes.addWidget(
            self.botao_voltar
        )

        layout_botoes.addStretch()

        layout_botoes.addWidget(
            self.botao_gerar
        )

        layout_principal.addLayout(
            layout_botoes
        )

        # =====================================================
        # EVENTOS
        # =====================================================

        self.botao_voltar.clicked.connect(
            self.reject
        )

        self.botao_gerar.clicked.connect(
            self.gerar_csv
        )

    # =========================================================
    # GERAR CSV
    # =========================================================

    def gerar_csv(self):

        try:

            # -------------------------------------------------
            # PREPARAR DADOS PARA O CANVA
            # -------------------------------------------------

            df_canva = preparar_dados_canva(
                self.artes,
                self.mes_numero,
            )

            # -------------------------------------------------
            # NOME SUGERIDO
            # -------------------------------------------------

            nome_sugerido = (
                f"aniversariantes_"
                f"{self.mes.lower()}.csv"
            )

            # -------------------------------------------------
            # ESCOLHER LOCAL
            # -------------------------------------------------

            caminho, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar arquivo CSV",
                nome_sugerido,
                "Arquivo CSV (*.csv)",
            )

            # Usuário cancelou
            if not caminho:
                return

            # -------------------------------------------------
            # GARANTIR EXTENSÃO
            # -------------------------------------------------

            if not caminho.lower().endswith(
                ".csv"
            ):
                caminho += ".csv"

            # -------------------------------------------------
            # GERAR ARQUIVO
            # -------------------------------------------------

            arquivo = gerar_csv_arquivo(
                df_canva,
                Path(caminho),
            )

            # -------------------------------------------------
            # SUCESSO
            # -------------------------------------------------

            QMessageBox.information(
                self,
                "CSV gerado",
                "O arquivo foi gerado com sucesso!\n\n"
                f"Local:\n{arquivo}",
            )

            # Fecha a pré-visualização
            self.accept()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro ao gerar CSV",
                str(erro),
            )

    # =========================================================
    # ESTILO
    # =========================================================

    def aplicar_estilo(self):

        self.setStyleSheet(
            """
            QDialog {
                background-color: #111827;
                color: #ffffff;
            }

            QLabel {
                color: #ffffff;
            }

            #titulo {
                font-size: 26px;
                font-weight: bold;
            }

            #subtitulo {
                font-size: 15px;
                color: #9ca3af;
            }

            #card_arte {
                background-color: #1f2937;
                border: 1px solid #374151;
                border-radius: 12px;
            }

            #titulo_arte {
                font-size: 17px;
                font-weight: bold;
                color: #60a5fa;
                padding-bottom: 4px;
            }

            #linha_funcionario {
                background-color: #111827;
                border-radius: 7px;
            }

            #numero {
                color: #6b7280;
                font-weight: bold;
            }

            #nome {
                font-size: 14px;
            }

            #botao_voltar {
                background-color: #374151;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
            }

            #botao_voltar:hover {
                background-color: #4b5563;
            }

            #botao_gerar {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
            }

            #botao_gerar:hover {
                background-color: #1d4ed8;
            }

            QScrollBar:vertical {
                background-color: #111827;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #374151;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            """
        )