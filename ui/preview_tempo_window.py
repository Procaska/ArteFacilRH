from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from services.tempo_de_casa import preparar_dados_canva, gerar_csv


class PreviewTempoCasaWindow(QDialog):

    def __init__(self, parent, mes, mes_numero, marcos):
        super().__init__(parent)

        self.mes = mes
        self.mes_numero = mes_numero
        self.marcos = marcos

        self.setWindowTitle("Conferir tempo de casa")
        self.setMinimumSize(760, 650)
        self.resize(820, 720)

        self.criar_interface()
        self.aplicar_estilo()

    def criar_interface(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        titulo = QLabel("Conferir tempo de casa")
        titulo.setObjectName("titulo")

        subtitulo = QLabel(
            f"{self.mes.upper()} • {len(self.marcos)} funcionário(s)"
        )
        subtitulo.setObjectName("subtitulo")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scroll")

        conteudo = QWidget()
        lista = QVBoxLayout(conteudo)
        lista.setContentsMargins(4, 4, 4, 4)
        lista.setSpacing(12)

        for numero, (_, funcionario) in enumerate(self.marcos.iterrows(), start=1):
            card = QFrame()
            card.setObjectName("cardArte")
            card.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,
            )

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 18, 20, 18)
            card_layout.setSpacing(6)

            rotulo = QLabel(f"ARTE {numero}")
            rotulo.setObjectName("rotulo")

            nome = QLabel(str(funcionario["Nome"]))
            nome.setObjectName("nome")
            nome.setWordWrap(True)

            tempo = QLabel(f"{funcionario['Tempo de Casa']} ANOS")
            tempo.setObjectName("tempo")

            card_layout.addWidget(rotulo)
            card_layout.addWidget(nome)
            card_layout.addWidget(tempo)

            lista.addWidget(card)

        lista.addStretch()
        scroll.setWidget(conteudo)
        layout.addWidget(scroll, 1)

        botoes = QHBoxLayout()
        botoes.setSpacing(10)

        voltar = QPushButton("VOLTAR")
        voltar.setObjectName("botaoSecundario")
        voltar.setCursor(Qt.CursorShape.PointingHandCursor)
        voltar.clicked.connect(self.reject)

        gerar = QPushButton("GERAR CSV")
        gerar.setObjectName("botaoPrincipal")
        gerar.setCursor(Qt.CursorShape.PointingHandCursor)
        gerar.setMinimumHeight(46)
        gerar.clicked.connect(self.gerar_csv)

        botoes.addWidget(voltar)
        botoes.addStretch()
        botoes.addWidget(gerar)

        layout.addLayout(botoes)
        self.setLayout(layout)

    def gerar_csv(self):
        try:
            df_canva = preparar_dados_canva(self.marcos)

            pasta_padrao = Path.cwd() / "output" / "tempo_casa"
            pasta_padrao.mkdir(parents=True, exist_ok=True)

            nome_arquivo = f"tempo_casa_{self.mes.lower()}.csv"
            caminho_padrao = pasta_padrao / nome_arquivo

            caminho, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar CSV para o Canva",
                str(caminho_padrao),
                "Arquivo CSV (*.csv)",
            )

            if not caminho:
                return

            arquivo = gerar_csv(df_canva, caminho)

            QMessageBox.information(
                self,
                "CSV gerado",
                f"Arquivo pronto para o Canva:\n\n{arquivo}",
            )

            self.accept()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao gerar CSV",
                str(erro),
            )

    def aplicar_estilo(self):
        self.setStyleSheet(
            """
        QDialog {
            background: #0F1012;
        }

        QLabel {
            color: #F5F5F5;
        }

        QLabel#titulo {
            color: #F5F5F5;
            font-size: 26px;
            font-weight: 700;
        }

        QLabel#subtitulo {
            color: #898E98;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 1px;
        }

        QScrollArea#scroll {
            background: transparent;
            border: none;
        }

        QFrame#cardArte {
            background: #18191D;
            border: 1px solid #2B2D33;
            border-radius: 12px;
        }

        QLabel#rotulo {
            color: #737881;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        QLabel#nome {
            color: #F5F5F5;
            font-size: 19px;
            font-weight: 700;
        }

        QLabel#tempo {
            color: #E04A4A;
            font-size: 15px;
            font-weight: 700;
        }

        QPushButton#botaoSecundario {
            background: #222428;
            color: #C8CBD1;
            border: 1px solid #34363C;
            border-radius: 8px;
            padding: 11px 20px;
            font-size: 12px;
            font-weight: 700;
        }

        QPushButton#botaoSecundario:hover {
            background: #2C2E34;
        }

        QPushButton#botaoPrincipal {
            background: #A92525;
            color: white;
            border: none;
            border-radius: 9px;
            padding: 0 24px;
            font-size: 12px;
            font-weight: 700;
        }

        QPushButton#botaoPrincipal:hover {
            background: #D13A3A;
        }
        """
  )
