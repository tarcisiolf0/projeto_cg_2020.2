# kitchenOpenGL
## Cozinha modelada com PyOpenGL

### Projeto da disciplina de Computação Gráfica do curso de Ciência da Computação IC-UFAL
### Professor: Marcelo Costa Oliveira
### Dupla: Leandro e Tarcísio
#### 2020.2

Demonstração: 


#### Requisitos para rodar:
- python3 instalado
- PyOpenGL e PyOpenGL_accelerate
- pygame e pyglm

#### Instalação dos Requisitos:
- download e instalação do Python3 em https://www.python.org/downloads/
- PyOpenGL e PyOpenGL_accelerate podem ser instalados via PIP, para isto basta usar o comando:

`pip install PyOpenGL PyOpenGL_accelerate`

Mais informações em: https://pypi.org/project/PyOpenGL/

No entanto, há diversos relatos de erro ao instalar dessa forma, então é recomendado baixar o pacote externamente e instalá-lo via PIP, para isto:
- acessar https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

- baixar os seguintes pacotes:
PyOpenGL_accelerate-3.1.5-cp39-cp39-win_amd64.whl
PyOpenGL-3.1.5-cp39-cp39-win_amd64.whl

fique atento a versão do seu python, se for 32 bits,
baixar os pacotes sendo win32 no lugar de win_amd64

- após o download, basta instalá-los com o PIP, exemplo:

`pip install PyOpenGL_accelerate-3.1.5-cp39-cp39-win_amd64.whl`

`pip install PyOpenGL-3.1.5-cp39-cp39-win_amd64.whl`

- instalar pygame e pyglm utilizando o PIP:

`pip install pygame`

`pip install PyGLM`

Mais informações em: https://pypi.org/project/PyGLM/ e https://pypi.org/project/pygame/

#### Executando:
- Para rodar basta entrar na pasta do projeto e executar com: `py main.py`

#### Controles:
- wasd movimentam a câmera
- clicar e arrastar o mouse mudam o angulo da câmera
- 'i' ativa a iluminação, 'I' desativa
- 'l' ativa spotlight, 'L' desativa
- 'o' abre a porta, 'O' fecha
- 'j' abre as janelas, 'J' fecha as janelas

O projeto foi desenvolvido com o Vscode.


#### Referência:
- Implementação de um quarto no openGL

https://github.com/myrondavid/bedroomOpenGL