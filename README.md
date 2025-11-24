🧩 Zelda Chess
📌 Sobre o projeto

Este é um jogo de xadrez com interface gráfica em **Tkinter**, IA
baseada em **Minimax** e peças personalizadas.\
As imagens das peças e telas do jogo **estão armazenadas em outra branch
do mesmo repositório**.

------------------------------------------------------------------------

🛠️ Requisitos para rodar o projeto

✔️ 1. Ter o Python instalado

Versão recomendada: **Python 3.10+**

Verifique sua versão:

    python --version

------------------------------------------------------------------------

✔️ 2. Instalar as dependências

O projeto utiliza duas bibliotecas externas:

-   **python-chess** → lógica do xadrez\
-   **Pillow (PIL)** → tratamento de imagens

Instale com:

    pip install python-chess pillow

------------------------------------------------------------------------

✔️ 3. Baixar as imagens do projeto

As imagens **NÃO estão na branch main**.\
Acesse a branch onde elas estão (ex: `imagens`, `assets` ou outro nome
definido).

Depois:

1.  Baixe a pasta `imagens/`
2.  Coloque-a na **mesma pasta** do arquivo `xadrez.py`

Estrutura recomendada:

    /projeto
     ├── xadrez.py
     └── imagens/
          ├── white_pawn.png
          ├── black_queen.png
          ├── ganhou.png
          ├── perdeu.png
          └── ...

------------------------------------------------------------------------

▶️ Como executar o jogo

Dentro da pasta do projeto, rode:

    python xadrez.py

No Windows com Python 3.11:

    python3.11 xadrez.py

------------------------------------------------------------------------

❗ Erro comum: "No module named chess"

Isso acontece quando o `python-chess` não está instalado.

Para resolver:

    pip install python-chess
