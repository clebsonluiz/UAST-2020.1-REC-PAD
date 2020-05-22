# UAST 2020.1 PyGame Alien Game IA
###### Projeto de Disciplina baseado no Jogo do Dinossauro do Google :)
--------

Projeto simples feito em Python usando Pygame para a disciplina de Reconhecimento de Padrões, O Jogo envolve o uso de Rede Neural e Algoritmo Genético para seleção. Como é o primeiro projeto feito usando tais ferramentas logo, o código fonte pode estar ruim/feio ou mal optimizado. 

## Imagens do Game
#### Tela principal do Modo IA

![](/assets/capturas/tela1.png)

#### Telas de Informações do Modo IA

![**](/assets/capturas/tela2.png)

**Nota: As imagens da Rede Neural não representam o próprio funcionamento da Rede Neural, é apenas uma abstração informativa para identificar quais foram as saídas escolhidas pelas funções de ativação

## Começando a Testar

##### No Arquivo main na pasta raiz, exite o seguinte main file.

```bash

|_ assets
|_ game
|_ __main__.py <- Esse File Aqui

```
##### Localizando o trecho de código a seguir: 
 
```python


GAME_AI_MODE = True

pg.init()

try:
    set_render_type({'NORMAL': True, 'COLISION': False, 'DEBUG': True})
    if GAME_AI_MODE:
        game = GameIA()
    else:
        game = Game()
    game.start()
except Exception as ex:
    print(ex)
```
- Para Jogar o Game, faça:

```python
GAME_AI_MODE = False
```
- Para Deixar a IA Jogando
```python
GAME_AI_MODE = True
```
- Se já existir uma seed cromossomial salva no file.txt localizada em:

```bash
|_ assets
  |_ capturas
  |_ images
  |_ txt
    |_ backup.txt
    |_ file.txt <- Esse File Aqui
|_ game
|_ __main__.py 
```
O jogo irá carregar-la e usar como continuação da geração, caso contrário, se quiser que a IA aprenda novamente tudo do Zero, apague o conteúdo de dentro do file.txt