# ArteFácil RH

Aplicação desktop desenvolvida em **Python + PySide6** para automatizar a preparação de dados de funcionários e gerar arquivos **CSV compatíveis com o Canva – Criar em lote**.

O objetivo do projeto é transformar uma planilha de funcionários em dados organizados para criação automática de artes, reduzindo tarefas manuais e facilitando o trabalho do setor responsável.

## 🚀 Funcionalidades

### 🎂 Aniversários

* Seleção da planilha de funcionários.
* Seleção do mês desejado.
* Identificação automática dos aniversariantes.
* Ordenação por dia de nascimento.
* Divisão dos funcionários em grupos de até **12 pessoas por arte**.
* Formatação dos nomes para:

  * Primeiro nome + último sobrenome.
  * Letras minúsculas.
* Exibição de uma tela de pré-visualização.
* Geração de CSV para utilização no Canva.
* Arquivo gerado com os campos:

```text
MES
NOME_1 até NOME_12
DATA_1 até DATA_12
ARTE
```

### 🏆 Tempo de Casa

* Utiliza a mesma seleção de mês da funcionalidade de aniversários.
* Consulta a data de admissão dos funcionários.
* Identifica os marcos de:

```text
5 anos
10 anos
15 anos
20 anos
25 anos
```

* Cada funcionário elegível gera uma arte individual.
* Exibe nome, tempo de casa e data do marco.
* Gera CSV compatível com o Canva.

Formato:

```text
MES,NOME,TEMPO_DE_CASA,DATA
```

Exemplo:

```text
setembro,adriana duarte,5 ANOS,20/09
setembro,emanoela abreu,10 ANOS,20/09
```

## 📊 Planilha utilizada

O sistema foi desenvolvido para trabalhar com a planilha oficial de funcionários.

A aplicação utiliza a aba:

```text
QUADRO DE LOTAÇÃO
```

O projeto possui um leitor específico para transformar a estrutura da planilha oficial em um `DataFrame` organizado, contendo principalmente:

```text
Nome
Data de Nascimento
Data de Admissão
```

A planilha original **não é modificada** pelo sistema.

## 🏗️ Estrutura do projeto

```text
ArteFacilRH/
│
├── assets/
│   └── logo.ico
│
├── services/
│   ├── __init__.py
│   ├── aniversarios.py
│   ├── tempo_de_casa.py
│   └── leitor_oficial.py
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── preview_window.py
│   └── preview_tempo_window.py
│
├── output/
│
├── main.py
├── funcionarios.xlsx
└── README.md
```

## 🛠️ Tecnologias utilizadas

* **Python**
* **PySide6** — interface gráfica
* **Pandas** — tratamento dos dados
* **OpenPyXL** — leitura de arquivos Excel
* **Pathlib** — gerenciamento de caminhos e arquivos
* **PyInstaller** — criação do executável
* **Canva Criar em lote** — utilização dos CSVs gerados

## 🔄 Funcionamento

```text
             PLANILHA OFICIAL
                    │
                    ▼
          leitor_oficial.py
                    │
                    ▼
          DADOS ORGANIZADOS
                    │
             ┌──────┴──────┐
             ▼             ▼
       ANIVERSÁRIOS    TEMPO DE CASA
             │             │
             ▼             ▼
       FILTRAGEM       FILTRAGEM
        POR MÊS         POR MÊS
             │             │
             ▼             ▼
        PRÉVIA DA ARTE  PRÉVIA DA ARTE
             │             │
             └──────┬──────┘
                    ▼
                 CSV
                    │
                    ▼
          CANVA – CRIAR EM LOTE
```

## 📁 Saída dos arquivos

Os arquivos CSV são preparados para serem utilizados diretamente no recurso **Criar em lote** do Canva.

Por padrão, o sistema sugere a pasta:

```text
Downloads
```

Os nomes dos arquivos seguem o padrão:

```text
aniversariantes_setembro.csv
```

e:

```text
tempo_casa_setembro.csv
```

## 🎨 Interface
A aplicação possui uma interface desktop com tema escuro, seleção de tipo de arte, seleção de mês e telas de pré-visualização antes da geração dos arquivos.

Os recursos visuais da aplicação ficam dentro da pasta:

```text
assets/
```

Essa pasta também é incluída na versão executável através do PyInstaller.

## 📦 Gerando o executável

O projeto utiliza **PyInstaller** para transformar a aplicação Python em um executável para Windows.

Execute o comando abaixo no terminal do **VS Code**, estando na pasta raiz do projeto:

```powershell
python -m PyInstaller --noconfirm --clean --windowed --name "ArteFacilRH" --icon "assets\logo.ico" --add-data "assets;assets" main.py
```

Após a compilação, o executável será encontrado em:

```text
dist/
└── ArteFacilRH/
    └── ArteFacilRH.exe
```

> **Importante:** execute o `.exe` localizado dentro da pasta `dist`, e não o executável presente na pasta `build`.
