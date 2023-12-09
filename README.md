O programa tem as seguintes funcionalidades:

Permite ao usuário escolher entre iniciar o jogo, ver o manual, ver os créditos ou sair do jogo na tela do menu.
Mostra as regras do jogo e os créditos em telas separadas, com a opção de voltar ao menu.
Cria um tabuleiro de 64 casas, alternando entre as cores preta e branca, e distribui 12 peças vermelhas e 12 peças brancas nas extremidades do tabuleiro.
Controla o turno dos jogadores, alternando entre o jogador vermelho e o jogador branco, e mostrando na tela a quem pertence o turno.
Permite ao usuário clicar em uma peça e ver os movimentos possíveis em verde, e clicar em uma casa vazia para mover a peça ou capturar uma peça do oponente.
Verifica se uma peça chegou à última linha do tabuleiro e a transforma em dama, que pode se mover para frente e para trás na diagonal.
Verifica se há uma situação de empate, vitória do vermelho ou vitória do branco, e mostra a tela do vencedor com a opção de voltar ao menu.
O programa faz isso usando os seguintes passos:

Importa as bibliotecas necessárias para o funcionamento do jogo, como pygame, string, heapq e spacy.
Define as constantes e as cores que serão usadas no jogo, como a largura, a altura, o preto, o branco, o vermelho, etc.
Define as funções auxiliares que serão usadas no jogo, como a função text_objects, que cria um objeto de texto na tela, a função cria_botao, que cria um botão na tela, a função coluna_clicada, que retorna o índice da coluna clicada pelo mouse, e a função linha_clicada, que retorna o índice da linha clicada pelo mouse.
Define as funções que criam as telas do jogo, como a função creditos, que mostra os créditos do jogo, a função regras, que mostra as regras do jogo, a função tela_vencedor, que mostra a tela do vencedor do jogo, e a função menu_jogo, que mostra a tela do menu do jogo.
Define a classe Jogo, que representa o estado do jogo e contém os atributos e os métodos necessários para o funcionamento do jogo, como a matriz_jogadores, que armazena as peças do tabuleiro, o turno, que armazena o turno atual, o status, que armazena o status do jogo, o desenha, que desenha o tabuleiro e as peças na tela, o avalia_clique, que avalia o clique do usuário e realiza o movimento ou a captura da peça, e o verifica_vencedor, que verifica se há um vencedor ou um empate no jogo.
Cria um objeto da classe Jogo e executa a função menu_jogo, que inicia o jogo e permite ao usuário escolher entre as opções do menu.
Executa a função loop_jogo, que executa o loop principal do jogo, verificando os eventos da tela, atualizando o display e o relógio, e chamando os métodos do objeto jogo.
Encerra o pygame e o programa quando o usuário sair do jogo.
