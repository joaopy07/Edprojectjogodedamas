import pygame # Importa o módulo pygame, que é uma biblioteca para desenvolver jogos
from pygame.locals import * # Importa todas as constantes e funções do módulo pygame.locals

pygame.init() # Inicializa todos os módulos do pygame

# VARIÁVEIS DE VALOR CONSTANTE
LARGURA = 800 # Define a largura da janela do jogo em pixels
ALTURA = 600 # Define a altura da janela do jogo em pixels

# Define as cores que serão usadas no jogo em formato RGB (Red, Green, Blue)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
VERMELHO = (120, 0, 0)
VERDE_ESCURO = (0, 120, 0)
VERDE_CLARO = (0, 255, 0)
VERMELHO_CLARO = (255, 0, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TABULEIRO = (0, 31, 0)

# INICIANDO PROGRAMAÇÃO DO DISPLAY
display = pygame.display.set_mode((LARGURA, ALTURA)) # Cria uma janela do jogo com as dimensões especificadas
pygame.display.set_caption('Jogo de Damas') # Define o título da janela do jogo
pygame.font.init() # Inicializa o módulo de fontes do pygame
clock = pygame.time.Clock() # Cria um objeto para controlar o tempo do jogo

# Classe principal
class Jogo:
	# Classe para tomar conta do status do jogo
	def __init__(self):
		self.status = 'jogando' # Define o status inicial do jogo como 'jogando'
		self.turno = 1 # Define o turno inicial do jogo como 1
		self.jogadores = ('x', 'o') # Define os símbolos dos jogadores como 'x' e 'o'
		self.cedula_selecionada = None # Define a cédula selecionada pelo jogador como nenhuma
		self.pulando = False # Define se o jogador está pulando uma cédula adversária como falso
		# Define a matriz que representa o tabuleiro do jogo, onde cada elemento é uma cédula
		# As cédulas vazias são representadas por '-', as cédulas do jogador 'x' por 'x' e as do jogador 'o' por 'o'
		self.matriz_jogadores = [['x','-','x','-','x','-','x','-'],
							    ['-','x','-','x','-','x','-','x'],
				  			    ['x','-','x','-','x','-','x','-'],
							    ['-','-','-','-','-','-','-','-'],
							    ['-','-','-','-','-','-','-','-'],
							    ['-','o','-','o','-','o','-','o'],
							    ['o','-','o','-','o','-','o','-'],
							    ['-','o','-','o','-','o','-','o']]

	def avalia_clique(self, pos):
		# Método para avaliar o clique do mouse do jogador e realizar a ação correspondente
		if self.status == "jogando": # Se o status do jogo for 'jogando'
			linha, coluna = linha_clicada(pos), coluna_clicada(pos) # Obtém a linha e a coluna da cédula clicada a partir da posição do mouse
			if self.cedula_selecionada: # Se o jogador já tiver selecionado uma cédula
				movimento = self.is_movimento_valido(self.jogadores[self.turno % 2], self.cedula_selecionada, linha, coluna) # Verifica se o movimento da cédula selecionada para a cédula clicada é válido
				if movimento[0]: # Se o movimento for válido
					self.jogar(self.jogadores[self.turno % 2], self.cedula_selecionada, linha, coluna, movimento[1]) # Realiza o movimento
				elif linha == self.cedula_selecionada[0] and coluna == self.cedula_selecionada[1]: # Se o jogador clicou na mesma cédula que já estava selecionada
					movs = self.movimento_obrigatorio(self.cedula_selecionada) # Obtém os movimentos obrigatórios da cédula selecionada
					if movs[0] == []: # Se não houver movimentos obrigatórios
						if self.pulando: # Se o jogador estava pulando uma cédula adversária
							self.pulando = False # Define o pulando como falso
							self.proximo_turno() # Passa para o próximo turno
					self.cedula_selecionada = None # Deseleciona a cédula
			else: # Se o jogador não tiver selecionado uma cédula
				if self.matriz_jogadores[linha][coluna].lower() == self.jogadores[self.turno % 2]: # Se a cédula clicada pertencer ao jogador da vez
					self.cedula_selecionada = [linha, coluna] # Seleciona a cédula

	# VERIFICANDO SE UM MOVIMENTO REALIZADO PELO JOGADOR É VÁLIDO
	def is_movimento_valido(self, jogador, localizacao_cedula, linha_destino, coluna_destino):
		# Método para verificar se um movimento realizado pelo jogador é válido
		# Retorna uma tupla (booleano, cédula), onde o booleano indica se o movimento é válido ou não, e a cédula é a cédula adversária que foi pulada, se houver

		linha_originaria = localizacao_cedula[0] # Obtém a linha da cédula de origem
		coluna_originaria = localizacao_cedula[1] # Obtém a coluna da cédula de origem

		obrigatorios = self.todos_obrigatorios() # Obtém todos os movimentos obrigatórios do turno

		if obrigatorios != {}: # Se houver movimentos obrigatórios
			if (linha_originaria, coluna_originaria) not in obrigatorios: # Se a cédula de origem não estiver entre os movimentos obrigatórios
				return False, None # Retorna falso e nenhuma cédula
			elif [linha_destino, coluna_destino] not in obrigatorios[(linha_originaria, coluna_originaria)]: # Se a cédula de destino não estiver entre os movimentos obrigatórios da cédula de origem
				return False, None # Retorna falso e nenhuma cédula

		movimento, pulo = self.movimentos_possiveis(localizacao_cedula) # Obtém os movimentos possíveis e as cédulas puladas da cédula de origem

		if [linha_destino, coluna_destino] in movimento: # Se a cédula de destino estiver entre os movimentos possíveis
			if pulo: # Se houver cédulas puladas
				if len(pulo) == 1: # Se houver apenas uma cédula pulada
					return True, pulo[0] # Retorna verdadeiro e a cédula pulada
				else: # Se houver mais de uma cédula pulada
					for i in range(len(pulo)): # Para cada cédula pulada
						if abs(pulo[i][0] - linha_destino) == 1 and abs(pulo[i][1] - coluna_destino) == 1: # Se a cédula pulada estiver adjacente à cédula de destino
							return True, pulo[i] # Retorna verdadeiro e a cédula pulada

			if self.pulando: # Se o jogador estiver pulando uma cédula adversária
				return False, None # Retorna falso e nenhuma cédula

			return True, None # Retorna verdadeiro e nenhuma cédula

		return False, None # Retorna falso e nenhuma cédula

	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UM TURNO
	def todos_obrigatorios(self):
		# Método para retornar todos os movimentos obrigatórios de um turno
		# Retorna um dicionário onde as chaves são as cédulas que têm movimentos obrigatórios e os valores são as listas de cédulas de destino possíveis
		todos = {} # Cria um dicionário vazio

		for r in range(len(self.matriz_jogadores)): # Para cada linha da matriz do tabuleiro
			for c in range(len(self.matriz_jogadores[r])): # Para cada coluna da matriz do tabuleiro
				ob, pulos = self.movimento_obrigatorio((r, c)) # Obtém os movimentos obrigatórios e as cédulas puladas da cédula atual
				if  ob != []: # Se houver movimentos obrigatórios
					todos[(r, c)] = ob # Adiciona a cédula atual e os movimentos obrigatórios ao dicionário

		return todos # Retorna o dicionário com os movimentos obrigatórios


	# Método para verificar se existe algum movimento possível para o jogador da vez
	def existe_possivel(self):
			for l in range(len(self.matriz_jogadores)): # Para cada linha da matriz do tabuleiro
				for c in range(len(self.matriz_jogadores[l])): # Para cada coluna da matriz do tabuleiro
					if self.movimentos_possiveis((l, c))[0]: # Se a cédula atual tiver algum movimento possível
						return True # Retorna verdadeiro
			return False # Se nenhum movimento possível for encontrado, retorna falso

	# Método para retornar os movimentos obrigatórios de uma cédula que pode ser jogada em determinado turno
	def movimento_obrigatorio(self, localizacao_cedula):
		obrigatorios = [] # Cria uma lista vazia para armazenar os movimentos obrigatórios
		posicao_cedula_pulada = [] # Cria uma lista vazia para armazenar as cédulas puladas

		l = localizacao_cedula[0] # Obtém a linha da cédula
		c = localizacao_cedula[1] # Obtém a coluna da cédula

		jogador = self.jogadores[self.turno % 2] # Obtém o símbolo do jogador da vez
		index = self.jogadores.index(jogador) # Obtém o índice do jogador da vez

		array = [jogador.lower(), jogador.upper(), '-'] # Cria uma lista com os símbolos do jogador e a cédula vazia

		if self.matriz_jogadores[l][c].islower() and self.matriz_jogadores[l][c] == jogador and \
		self.turno % 2 == index: # Se a cédula for uma peça normal do jogador da vez
				if l > 0: # Se a cédula não estiver na primeira linha
					if c < 7: # Se a cédula não estiver na última coluna
						if self.matriz_jogadores[l - 1][c + 1].lower() not in array: # Se a cédula na diagonal superior direita for uma peça adversária
							l_x = l - 1 # Obtém a linha da cédula adversária
							l_c = c + 1 # Obtém a coluna da cédula adversária

							if l_x - 1 >= 0 and l_c + 1 <= 7: # Se a cédula na diagonal superior direita da cédula adversária estiver dentro do tabuleiro
								if self.matriz_jogadores[l_x - 1][l_c + 1] == '-': # Se a cédula na diagonal superior direita da cédula adversária estiver vazia
									obrigatorios.append([l_x - 1, l_c + 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
									posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas
					if c > 0: # Se a cédula não estiver na primeira coluna
						if self.matriz_jogadores[l - 1][c - 1].lower() not in array: # Se a cédula na diagonal superior esquerda for uma peça adversária
							l_x = l - 1 # Obtém a linha da cédula adversária
							l_c = c - 1 # Obtém a coluna da cédula adversária

							if l_x - 1 >= 0 and l_c - 1 >= 0: # Se a cédula na diagonal superior esquerda da cédula adversária estiver dentro do tabuleiro
								if self.matriz_jogadores[l_x - 1][l_c - 1] == '-': # Se a cédula na diagonal superior esquerda da cédula adversária estiver vazia
									obrigatorios.append([l_x - 1, l_c - 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
									posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas
				if l < 7: # Se a cédula não estiver na última linha
					if c < 7: # Se a cédula não estiver na última coluna
						if self.matriz_jogadores[l + 1][c + 1].lower() not in array: # Se a cédula na diagonal inferior direita for uma peça adversária
							l_x = l + 1 # Obtém a linha da cédula adversária
							l_c = c + 1 # Obtém a coluna da cédula adversária

							if l_x + 1 <= 7 and l_c + 1 <= 7: # Se a cédula na diagonal inferior direita da cédula adversária estiver dentro do tabuleiro
								if self.matriz_jogadores[l_x + 1][l_c + 1] == '-': # Se a cédula na diagonal inferior direita da cédula adversária estiver vazia
									obrigatorios.append([l_x + 1, l_c + 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
									posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas
					if c > 0: # Se a cédula não estiver na primeira coluna
						if self.matriz_jogadores[l + 1][c - 1].lower() not in array: # Se a cédula na diagonal inferior esquerda for uma peça adversária
							l_x = l + 1 # Obtém a linha da cédula adversária
							l_c = c - 1 # Obtém a coluna da cédula adversária

							if l_x + 1 <= 7 and l_c - 1 >= 0: # Se a cédula na diagonal inferior esquerda da cédula adversária estiver dentro do tabuleiro
								if self.matriz_jogadores[l_x + 1][l_c - 1] == '-': # Se a cédula na diagonal inferior esquerda da cédula adversária estiver vazia
									obrigatorios.append([l_x + 1, l_c - 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
									posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas

		elif self.matriz_jogadores[l][c].isupper() and self.matriz_jogadores[l][c] == jogador.upper() and \
		self.turno % 2 == index: # Se a cédula for uma peça promovida do jogador da vez
			conta_linha = l # Define uma variável para armazenar a linha da cédula
			conta_coluna = c # Define uma variável para armazenar a coluna da cédula
			while True: # Inicia um laço infinito
				if conta_linha - 1 < 0 or conta_coluna - 1 < 0: break # Se a cédula estiver na primeira linha ou na primeira coluna, sai do laço
				else: # Senão
					if self.matriz_jogadores[conta_linha - 1][conta_coluna - 1] not in array: # Se a cédula na diagonal superior esquerda for uma peça adversária
						l_x = conta_linha - 1 # Obtém a linha da cédula adversária
						l_c = conta_coluna - 1 # Obtém a coluna da cédula adversária

						if l_x - 1 >= 0 and l_c - 1 >= 0: # Se a cédula na diagonal superior esquerda da cédula adversária estiver dentro do tabuleiro
							if self.matriz_jogadores[l_x - 1][l_c - 1] == '-': # Se a cédula na diagonal superior esquerda da cédula adversária estiver vazia
								posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas
								while True: # Inicia outro laço infinito
									if l_x - 1 < 0 or l_c - 1 < 0: # Se a cédula estiver na primeira linha ou na primeira coluna, sai do laço
										break
									else: # Senão
										if self.matriz_jogadores[l_x - 1][l_c - 1] == '-': # Se a cédula na diagonal superior esquerda estiver vazia
											
											obrigatorios.append([l_x - 1, l_c - 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
										else: # Senão
											break # Sai do laço
									l_x -= 1 # Decrementa a linha da cédula
									l_c -= 1 # Decrementa a coluna da cédula
						break # Sai do laço
				conta_linha -= 1 # Decrementa a linha da cédula
				conta_coluna -= 1 # Decrementa a coluna da cédula

			conta_linha = l # Define a variável para armazenar a linha da cédula
			conta_coluna = c # Define a variável para armazenar a coluna da cédula
			while True: # Inicia um laço infinito
				if conta_linha - 1 < 0 or conta_coluna + 1 > 7: break # Se a cédula estiver na primeira linha ou na última coluna, sai do laço
				else: # Senão
					if self.matriz_jogadores[conta_linha - 1][conta_coluna + 1] not in array: # Se a cédula na diagonal superior direita for uma peça adversária
						l_x = conta_linha - 1 # Obtém a linha da cédula adversária
						l_c = conta_coluna + 1 # Obtém a coluna da cédula adversária

						if l_x - 1 >= 0 and l_c + 1 <= 7: # Se a cédula na diagonal superior direita da cédula adversária estiver dentro do tabuleiro
							if self.matriz_jogadores[l_x - 1][l_c + 1] == '-': # Se a cédula na diagonal superior direita da cédula adversária estiver vazia
								posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas
								while True: # Inicia outro laço infinito
									if l_x - 1 < 0 or l_c + 1 > 7: # Se a cédula estiver na primeira linha ou na última coluna, sai do laço
										break
									else: # Senão
										if self.matriz_jogadores[l_x -1][l_c + 1] == '-': # Se a cédula na diagonal superior direita estiver vazia
											obrigatorios.append([l_x - 1, l_c + 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
										else: # Senão
											break # Sai do laço
									l_x -= 1 # Decrementa a linha da cédula
									l_c += 1 # Incrementa a coluna da cédula
						break # Sai do laço
				conta_linha -= 1 # Decrementa a linha da cédula
				conta_coluna += 1 # Incrementa a coluna da cédula
			# Essa parte do código verifica as outras duas diagonais da cédula promovida
			conta_linha = l # Define a variável para armazenar a linha da cédula
			conta_coluna = c # Define a variável para armazenar a coluna da cédula
			while True: # Inicia um laço infinito
				if conta_linha + 1 > 7 or conta_coluna + 1 > 7: break # Se a cédula estiver na última linha ou na última coluna, sai do laço
				else: # Senão
					if self.matriz_jogadores[conta_linha + 1][conta_coluna + 1] not in array: # Se a cédula na diagonal inferior direita for uma peça adversária
						l_x = conta_linha + 1 # Obtém a linha da cédula adversária
						l_c = conta_coluna + 1 # Obtém a coluna da cédula adversária

						if l_x + 1 <= 7 and l_c + 1 <= 7: # Se a cédula na diagonal inferior direita da cédula adversária estiver dentro do tabuleiro
							if self.matriz_jogadores[l_x + 1][l_c + 1] == '-': # Se a cédula na diagonal inferior direita da cédula adversária estiver vazia
								posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas
								while True: # Inicia outro laço infinito
									if l_x + 1 > 7 or l_c + 1 > 7: # Se a cédula estiver na última linha ou na última coluna, sai do laço
										break
									else: # Senão
										if self.matriz_jogadores[l_x + 1][l_c + 1] == '-': # Se a cédula na diagonal inferior direita estiver vazia
											obrigatorios.append([l_x + 1, l_c + 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
										else: # Senão
											break # Sai do laço
									l_x += 1 # Incrementa a linha da cédula
									l_c += 1 # Incrementa a coluna da cédula
						break # Sai do laço
				conta_linha += 1 # Incrementa a linha da cédula
				conta_coluna += 1 # Incrementa a coluna da cédula

			conta_linha = l # Define a variável para armazenar a linha da cédula
			conta_coluna = c # Define a variável para armazenar a coluna da cédula
			while True: # Inicia um laço infinito
				if conta_linha + 1 > 7 or conta_coluna - 1 < 0: break # Se a cédula estiver na última linha ou na primeira coluna, sai do laço
				else: # Senão
					if self.matriz_jogadores[conta_linha + 1][conta_coluna - 1] not in array: # Se a cédula na diagonal inferior esquerda for uma peça adversária
						l_x = conta_linha + 1 # Obtém a linha da cédula adversária
						l_c = conta_coluna - 1 # Obtém a coluna da cédula adversária

						if l_x + 1 <= 7 and l_c - 1 >= 0: # Se a cédula na diagonal inferior esquerda da cédula adversária estiver dentro do tabuleiro
							if self.matriz_jogadores[l_x + 1][l_c - 1] == '-': # Se a cédula na diagonal inferior esquerda da cédula adversária estiver vazia
								posicao_cedula_pulada.append((l_x, l_c)) # Adiciona a cédula adversária às cédulas puladas
								while True: # Inicia outro laço infinito
									if l_x + 1 > 7 or l_c - 1 < 0: # Se a cédula estiver na última linha ou na primeira coluna, sai do laço
										break
									else: # Senão
										if self.matriz_jogadores[l_x + 1][l_c - 1] == '-': # Se a cédula na diagonal inferior esquerda estiver vazia
											obrigatorios.append([l_x + 1, l_c - 1]) # Adiciona a cédula vazia aos movimentos obrigatórios
										else: # Senão
											break # Sai do laço
									l_x += 1 # Incrementa a linha da cédula
									l_c -= 1 # Decrementa a coluna da cédula
						break # Sai do laço
				conta_linha += 1 # Incrementa a linha da cédula
				conta_coluna -= 1 # Decrementa a coluna da cédula

		return obrigatorios, posicao_cedula_pulada # Retorna a lista dos movimentos obrigatórios e a lista das cédulas puladas


	# MOSTRA OS MOVIMENTOS POSSÍVEIS DE UMA PEÇA SELECIONADA
# Método para retornar os movimentos possíveis e as cédulas puladas de uma cédula que pode ser jogada em determinado turno
	def movimentos_possiveis(self, localizacao_cedula):
		movimentos, pulos = self.movimento_obrigatorio(localizacao_cedula) # Obtém os movimentos obrigatórios e as cédulas puladas da cédula

		if movimentos == []: # Se não houver movimentos obrigatórios
			linha_atual = localizacao_cedula[0] # Obtém a linha da cédula
			coluna_atual = localizacao_cedula[1] # Obtém a coluna da cédula

			if self.matriz_jogadores[linha_atual][coluna_atual].islower(): # Se a cédula for uma peça normal
				if self.matriz_jogadores[linha_atual][coluna_atual] == 'o': # Se a cédula for uma peça do jogador 'o'
					if linha_atual > 0: # Se a cédula não estiver na primeira linha
						if coluna_atual < 7: # Se a cédula não estiver na última coluna
							if self.matriz_jogadores[linha_atual - 1][coluna_atual + 1] == '-': # Se a cédula na diagonal superior direita estiver vazia
								movimentos.append([linha_atual - 1, coluna_atual + 1]) # Adiciona a cédula vazia aos movimentos possíveis
						if coluna_atual > 0: # Se a cédula não estiver na primeira coluna
							if self.matriz_jogadores[linha_atual - 1][coluna_atual - 1] == '-': # Se a cédula na diagonal superior esquerda estiver vazia
								movimentos.append([linha_atual - 1, coluna_atual - 1]) # Adiciona a cédula vazia aos movimentos possíveis
				
				elif self.matriz_jogadores[linha_atual][coluna_atual] == 'x': # Se a cédula for uma peça do jogador 'x'
					if linha_atual < 7: # Se a cédula não estiver na última linha
						if coluna_atual < 7: # Se a cédula não estiver na última coluna
							if self.matriz_jogadores[linha_atual + 1][coluna_atual + 1] == '-': # Se a cédula na diagonal inferior direita estiver vazia
								movimentos.append([linha_atual + 1, coluna_atual + 1]) # Adiciona a cédula vazia aos movimentos possíveis
						if coluna_atual > 0: # Se a cédula não estiver na primeira coluna
							if self.matriz_jogadores[linha_atual + 1][coluna_atual - 1] == '-': # Se a cédula na diagonal inferior esquerda estiver vazia
								movimentos.append([linha_atual + 1, coluna_atual - 1]) # Adiciona a cédula vazia aos movimentos possíveis
			elif self.matriz_jogadores[linha_atual][coluna_atual].isupper(): # Se a cédula for uma peça promovida
				conta_linha = linha_atual # Define uma variável para armazenar a linha da cédula
				conta_coluna = coluna_atual # Define uma variável para armazenar a coluna da cédula
				while True: # Inicia um laço infinito
					if conta_linha - 1 < 0 or conta_coluna - 1 < 0: break # Se a cédula estiver na primeira linha ou na primeira coluna, sai do laço
					else: # Senão
						if self.matriz_jogadores[conta_linha - 1][conta_coluna - 1] == '-': # Se a cédula na diagonal superior esquerda estiver vazia
							movimentos.append([conta_linha - 1, conta_coluna - 1]) # Adiciona a cédula vazia aos movimentos possíveis
						else: break # Senão, sai do laço
					conta_linha -= 1 # Decrementa a linha da cédula
					conta_coluna -= 1 # Decrementa a coluna da cédula

				conta_linha = linha_atual # Define a variável para armazenar a linha da cédula
				conta_coluna = coluna_atual # Define a variável para armazenar a coluna da cédula
				while True: # Inicia um laço infinito
					if conta_linha - 1 < 0 or conta_coluna + 1 > 7: break # Se a cédula estiver na primeira linha ou na última coluna, sai do laço
					else: # Senão
						if self.matriz_jogadores[conta_linha - 1][conta_coluna + 1] == '-': # Se a cédula na diagonal superior direita estiver vazia
							movimentos.append([conta_linha - 1, conta_coluna + 1]) # Adiciona a cédula vazia aos movimentos possíveis
						else: break # Senão, sai do laço
					conta_linha -= 1 # Decrementa a linha da cédula
					conta_coluna += 1 # Incrementa a coluna da cédula

				conta_linha = linha_atual # Define a variável para armazenar a linha da cédula
				conta_coluna = coluna_atual # Define a variável para armazenar a coluna da cédula
				while True: # Inicia um laço infinito
					if conta_linha + 1 > 7 or conta_coluna + 1 > 7: break # Se a cédula estiver na última linha ou na última coluna, sai do laço
					else: # Senão
						if self.matriz_jogadores[conta_linha + 1][conta_coluna + 1] == '-': # Se a cédula na diagonal inferior direita estiver vazia
							movimentos.append([conta_linha + 1, conta_coluna + 1]) # Adiciona a cédula vazia aos movimentos possíveis
						else: break # Senão, sai do laço
					conta_linha += 1 # Incrementa a linha da cédula
					conta_coluna += 1 # Incrementa a coluna da cédula

				conta_linha = linha_atual # Define a variável para armazenar a linha da cédula
				conta_coluna = coluna_atual # Define a variável para armazenar a coluna da cédula
				while True: # Inicia um laço infinito
					if conta_linha + 1 > 7 or conta_coluna - 1 < 0: break # Se a cédula estiver na última linha ou na primeira coluna, sai do laço
					else: # Senão
						if self.matriz_jogadores[conta_linha + 1][conta_coluna - 1] == '-': # Se a cédula na diagonal inferior esquerda estiver vazia
							movimentos.append([conta_linha + 1, conta_coluna - 1]) # Adiciona a cédula vazia aos movimentos possíveis
						else: break # Senão, sai do laço
					conta_linha += 1 # Incrementa a linha da cédula
					conta_coluna -= 1 # Decrementa a coluna da cédula
				
		return movimentos, pulos # Retorna a lista dos movimentos possíveis e a lista das cédulas puladas


# Método para executar uma jogada de um jogador em uma cédula para um destino, com ou sem pulo
	def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
		linha_atual = localizacao_cedula[0] # Obtém a linha da cédula
		coluna_atual = localizacao_cedula[1] # Obtém a coluna da cédula
		char = self.matriz_jogadores[linha_atual][coluna_atual] # Obtém o símbolo da cédula

		self.matriz_jogadores[linha_destino][coluna_destino] = char # Coloca o símbolo da cédula no destino
		self.matriz_jogadores[linha_atual][coluna_atual] = '-' # Deixa a cédula original vazia

		if (jogador == 'x' and linha_destino == 7) or (jogador == 'o' and linha_destino == 0): # Se a cédula chegou na última linha do tabuleiro
			self.matriz_jogadores[linha_destino][coluna_destino] = char.upper() # Promove a cédula para uma peça que pode se mover em qualquer direção

		if pulo: # Se a jogada foi um pulo
			self.matriz_jogadores[pulo[0]][pulo[1]] = '-' # Deixa a cédula pulada vazia
			self.cedula_selecionada = [linha_destino, coluna_destino] # Seleciona a cédula que pulou para continuar pulando
			self.pulando = True # Define o estado de pulando como verdadeiro

		else: # Se a jogada não foi um pulo
			self.cedula_selecionada = None # Deseleciona a cédula
			self.proximo_turno() # Passa para o próximo turno
		vencedor = self.verifica_vencedor() # Verifica se há um vencedor

		if vencedor != None: # Se houver um vencedor
			self.status = 'game over' # Define o status do jogo como terminado

	# Método para passar para o próximo turno
	def proximo_turno(self):
		self.turno += 1 # Incrementa o contador de turnos

	# Método para verificar se há um vencedor
	def verifica_vencedor(self):

		x = sum([contador.count('x') + contador.count('X') for contador in self.matriz_jogadores]) # Conta o número de peças do jogador 'x'
		o = sum([contador.count('o') + contador.count('O') for contador in self.matriz_jogadores]) # Conta o número de peças do jogador 'o'

		if x == 0: # Se o jogador 'x' não tiver mais peças
			return 'o' # Retorna o jogador 'o' como vencedor

		if o == 0: # Se o jogador 'o' não tiver mais peças
			return 'x' # Retorna o jogador 'x' como vencedor

		if x == 1 and o == 1: # Se cada jogador tiver apenas uma peça
			return 'empate' # Retorna um empate

		if self.cedula_selecionada: # Se houver uma cédula selecionada
			if not self.movimentos_possiveis(self.cedula_selecionada)[0]: # Se a cédula selecionada não tiver mais movimentos possíveis
				if x == 1 and self.turno % 2 == 0: # Se o jogador 'x' tiver apenas uma peça e for a sua vez
					return 'o' # Retorna o jogador 'o' como vencedor
				if o == 1 and self.turno % 2 == 1: # Se o jogador 'o' tiver apenas uma peça e for a sua vez
					return 'x' # Retorna o jogador 'x' como vencedor

		if not self.existe_possivel(): # Se não houver mais movimentos possíveis para nenhum jogador
			return 'empate' # Retorna um empate


		return None # Se não houver um vencedor, retorna None

	# Método para desenhar o tabuleiro e as peças do jogo de damas usando a biblioteca pygame
	def desenha(self):
		matriz = [] # Cria uma lista vazia para armazenar a matriz do tabuleiro

		for i in range(8): # Percorre as oito linhas do tabuleiro
			if i % 2 == 0: # Se a linha for par
				matriz.append(['#','-','#','-','#','-','#','-']) # Adiciona uma lista com o padrão de cores alternadas
			else: # Se a linha for ímpar
				matriz.append(['-','#','-','#','-','#','-', '#']) # Adiciona uma lista com o padrão de cores invertido

		y = 0 # Define uma variável para armazenar a coordenada y do retângulo
		for l in range(len(matriz)): # Percorre as linhas da matriz
			x = 0 # Define uma variável para armazenar a coordenada x do retângulo
			for c in range(len(matriz[l])): # Percorre as colunas da matriz
				if matriz[l][c] == '#': # Se o elemento da matriz for '#'
					pygame.draw.rect(display, COR_TABULEIRO, (x, y, 75, 75)) # Desenha um retângulo com a cor do tabuleiro
				else: # Se o elemento da matriz for '-'
					pygame.draw.rect(display, BRANCO, (x, y, 75, 75)) # Desenha um retângulo com a cor branca
				x += 75 # Incrementa a coordenada x em 75 pixels
			y += 75 # Incrementa a coordenada y em 75 pixels

		if self.cedula_selecionada: # Se houver uma cédula selecionada
			obrigatorios = self.todos_obrigatorios() # Obtém os movimentos obrigatórios de todas as cédulas
			movs = self.movimentos_possiveis(self.cedula_selecionada) # Obtém os movimentos possíveis da cédula selecionada

			if obrigatorios != {}: # Se houver movimentos obrigatórios
				if (self.cedula_selecionada[0], self.cedula_selecionada[1]) not in obrigatorios: # Se a cédula selecionada não for uma das que tem movimento obrigatório
					x_vermelho = ALTURA / 8 * self.cedula_selecionada[1] # Obtém a coordenada x da cédula selecionada
					y_vermelho = ALTURA / 8 * self.cedula_selecionada[0] # Obtém a coordenada y da cédula selecionada

					pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75)) # Desenha um retângulo vermelho claro sobre a cédula selecionada
				else: # Se a cédula selecionada for uma das que tem movimento obrigatório
					if movs[0] == []: # Se a cédula selecionada não tiver mais movimentos possíveis
						x_vermelho = ALTURA / 8 * self.cedula_selecionada[1] # Obtém a coordenada x da cédula selecionada
						y_vermelho = ALTURA / 8 * self.cedula_selecionada[0] # Obtém a coordenada y da cédula selecionada

						pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75)) # Desenha um retângulo vermelho claro sobre a cédula selecionada
					else: # Se a cédula selecionada tiver movimentos possíveis
						for i in range(len(movs[0])): # Percorre os movimentos possíveis
							x_possivel = ALTURA / 8 * movs[0][i][1] # Obtém a coordenada x do movimento possível
							y_possivel = ALTURA / 8 * movs[0][i][0] # Obtém a coordenada y do movimento possível

							pygame.draw.rect(display, VERDE_CLARO, (x_possivel, y_possivel, 75, 75)) # Desenha um retângulo verde claro sobre o movimento possível
			else: # Se não houver movimentos obrigatórios
				if self.pulando: # Se a cédula selecionada estiver pulando
					x_vermelho = ALTURA / 8 * self.cedula_selecionada[1] # Obtém a coordenada x da cédula selecionada
					y_vermelho = ALTURA / 8 * self.cedula_selecionada[0] # Obtém a coordenada y da cédula selecionada

					pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75)) # Desenha um retângulo vermelho claro sobre a cédula selecionada
				else: # Se a cédula selecionada não estiver pulando
					if movs[0] == []: # Se a cédula selecionada não tiver mais movimentos possíveis
						x_vermelho = ALTURA / 8 * self.cedula_selecionada[1] # Obtém a coordenada x da cédula selecionada
						y_vermelho = ALTURA / 8 * self.cedula_selecionada[0] # Obtém a coordenada y da cédula selecionada

						pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75)) # Desenha um retângulo vermelho claro sobre a cédula selecionada
					else: # Se a cédula selecionada tiver movimentos possíveis
						for i in range(len(movs[0])): # Percorre os movimentos possíveis
							x_possivel = ALTURA / 8 * movs[0][i][1] # Obtém a coordenada x do movimento possível
							y_possivel = ALTURA / 8 * movs[0][i][0] # Obtém a coordenada y do movimento possível

							pygame.draw.rect(display, VERDE_CLARO, (x_possivel, y_possivel, 75, 75)) # Desenha um retângulo verde claro sobre o movimento possível

		for l in range(len(self.matriz_jogadores)): # Percorre as linhas da matriz de jogadores
			for c in range(len(self.matriz_jogadores[l])): # Percorre as colunas da matriz de jogadores
				elemento = self.matriz_jogadores[l][c] # Obtém o elemento da matriz de jogadores
				if elemento != '-': # Se o elemento não for vazio
					x = ALTURA / 8 * c + ALTURA / 16 # Obtém a coordenada x do centro da cédula
					y = ALTURA / 8 * l + ALTURA / 16 # Obtém a coordenada y do centro da cédula

					if elemento.lower() == 'x': # Se o elemento for uma peça do jogador 'x'
						pygame.draw.circle(display, VERMELHO, (x, y), 20, 0) # Desenha um círculo vermelho sobre a cédula
						if elemento == 'X': # Se o elemento for uma peça promovida do jogador 'x'
							pygame.draw.circle(display, PRETO, (x, y), 10, 0) # Desenha um círculo preto sobre o círculo vermelho
							pygame.draw.circle(display, AZUL, (x, y), 5, 0) # Desenha um círculo azul sobre o círculo preto
					else: # Se o elemento for uma peça do jogador 'o'
						pygame.draw.circle(display, BRANCO, (x, y), 20, 0) # Desenha um círculo branco sobre a cédula
						if elemento == 'O': # Se o elemento for uma peça promovida do jogador 'o'
							pygame.draw.circle(display, PRETO, (x, y), 10, 0) # Desenha um círculo preto sobre o círculo branco
							pygame.draw.circle(display, AZUL, (x, y), 5, 0) # Desenha um círculo azul sobre o círculo preto

		fonte = pygame.font.Font(None, 20) # Define a fonte para o texto
		
		x = sum([contador.count('x') + contador.count('X') for contador in self.matriz_jogadores]) # Conta o número de peças do jogador 'x'
		o = sum([contador.count('o') + contador.count('O') for contador in self.matriz_jogadores]) # Conta o número de peças do jogador 'o'

		if self.status != 'game over': # Se o jogo não estiver terminado

			surface_texto, rect_texto = text_objects("Vermelho: " + str(12 - o), fonte, VERMELHO_CLARO) # Cria um objeto de texto com o número de peças capturadas pelo jogador vermelho
			rect_texto.center = (650, 30) # Define o centro do retângulo do texto
			display.blit(surface_texto, rect_texto) # Desenha o texto na tela

			surface_texto, rect_texto = text_objects("Branco: " + str(12 - x), fonte, BRANCO) # Cria um objeto de texto com o número de peças capturadas pelo jogador branco
			rect_texto.center = (650, ALTURA - 30) # Define o centro do retângulo do texto
			display.blit(surface_texto, rect_texto) # Desenha o texto na tela

			if self.turno % 2 == 1: # Se for o turno do jogador branco
				surface_texto, rect_texto = text_objects("Turno do branco", fonte, BRANCO) # Cria um objeto de texto com a mensagem "Turno do branco"
				rect_texto.center = (700, ALTURA / 2) # Define o centro do retângulo do texto
				display.blit(surface_texto, rect_texto) # Desenha o texto na tela
			else: # Se for o turno do jogador vermelho
				surface_texto, rect_texto = text_objects("Turno do vermelho", fonte, VERMELHO_CLARO) # Cria um objeto de texto com a mensagem "Turno do vermelho"
				rect_texto.center = (700, ALTURA / 2) # Define o centro do retângulo do texto
				display.blit(surface_texto, rect_texto) # Desenha o texto na tela
		else: # Se o jogo estiver terminado
			surface_texto, rect_texto = text_objects("Game over", fonte, AZUL) # Cria um objeto de texto com a mensagem "Game over"
			rect_texto.center = (700, ALTURA / 3) # Define o centro do retângulo do texto
			display.blit(surface_texto, rect_texto) # Desenha o texto na tela

# --- FUNÇÕES A SEREM UTILIZADAS  ---

# Função para definir o padrão de textos na tela
def text_objects(text, font, color):
	textSurface = font.render(text, True, color) # Cria uma superfície de texto com a fonte, a cor e o antialiasing
	return textSurface, textSurface.get_rect() # Retorna a superfície de texto e o retângulo que a contém

# Função para criar um botão na tela
def cria_botao(msg, sqr, cor1, cor2, cor_texto, acao=None):
	mouse = pygame.mouse.get_pos() # Obtém a posição do mouse
	clique = pygame.mouse.get_pressed() # Obtém o estado dos botões do mouse

	if sqr[0] + sqr[2] > mouse[0] > sqr[0] and sqr[1] + sqr[3] > mouse[1] > sqr[1]: # Se o mouse estiver sobre o botão
		pygame.draw.rect(display, cor2, sqr) # Desenha o botão com a cor alternativa
		if clique[0] == 1 and acao != None: # Se o botão esquerdo do mouse for pressionado e houver uma ação associada ao botão
			acao() # Executa a ação
	else: # Se o mouse não estiver sobre o botão
		pygame.draw.rect(display, cor1, sqr) # Desenha o botão com a cor normal

	fontePequena = pygame.font.SysFont('comicsansms', 20) # Define a fonte pequena para o texto do botão
	surface_texto, rect_texto = text_objects(msg, fontePequena, cor_texto) # Cria um objeto de texto com a mensagem, a fonte e a cor do texto
	rect_texto.center = (sqr[0] + 60, sqr[1] + 20) # Define o centro do retângulo do texto
	display.blit(surface_texto, rect_texto) # Desenha o texto na tela

def creditos(): # Função para exibir os créditos do jogo
	sair = False # Define uma variável para controlar o laço
	while not sair: # Enquanto não sair
		for evento in pygame.event.get(): # Percorre os eventos da tela
			if evento.type == pygame.QUIT: # Se o evento for de sair
				pygame.quit() # Encerra o pygame
				quit() # Encerra o programa
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN: # Se o evento for de pressionar uma tecla ou um botão do mouse
				sair = True # Define a variável de sair como verdadeira

		display.fill(PRETO) # Preenche a tela com a cor preta
		fonte = pygame.font.SysFont('comicsansms', 20) # Define a fonte para o texto
		surface_texto, rect_texto = text_objects("", fonte, BRANCO) # Cria um objeto de texto vazio com a fonte e a cor branca
		rect_texto.center = ((LARGURA / 2), ALTURA / 3) # Define o centro do retângulo do texto
		display.blit(surface_texto, rect_texto) # Desenha o texto na tela

		surface_texto, rect_texto = text_objects("", fonte, BRANCO) # Cria outro objeto de texto vazio com a fonte e a cor branca
		rect_texto.center = ((LARGURA / 2), ALTURA / 2.7) # Define o centro do retângulo do texto
		display.blit(surface_texto, rect_texto) # Desenha o texto na tela

		surface_texto, rect_texto = text_objects("Versao Python: 2.7.x", fonte, VERMELHO_CLARO) # Cria um objeto de texto com a versão do Python usada, a fonte e a cor vermelha clara
		rect_texto.center = ((LARGURA / 2), ALTURA / 1.5) # Define o centro do retângulo do texto
		display.blit(surface_texto, rect_texto) # Desenha o texto na tela

		surface_texto, rect_texto = text_objects("Versao Pygame: 1.9.1", fonte, VERMELHO_CLARO) # Cria um objeto de texto com a versão do Pygame usada, a fonte e a cor vermelha clara
		rect_texto.center = ((LARGURA / 2), ALTURA / 1.3) # Define o centro do retângulo do texto
		display.blit(surface_texto, rect_texto) # Desenha o texto na tela

		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO) # Cria um objeto de texto com a mensagem de voltar ao menu, a fonte e a cor verde clara
		display.blit(voltar, (25, 550)) # Desenha o texto na tela

		pygame.display.update() # Atualiza a tela
		clock.tick(15) # Define o relógio para 15 FPS

def regras(): # Função para exibir as regras do jogo
	sair = False # Define uma variável para controlar o laço

	while not sair: # Enquanto não sair
		for evento in pygame.event.get(): # Percorre os eventos da tela
			if evento.type == pygame.QUIT: # Se o evento for de sair
				sair = True # Define a variável de sair como verdadeira
				pygame.quit() # Encerra o pygame
				quit() # Encerra o programa
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN: # Se o evento for de pressionar uma tecla ou um botão do mouse
				sair = True # Define a variável de sair como verdadeira

		display.fill(PRETO) # Preenche a tela com a cor preta

		fonte = pygame.font.SysFont('comicsansms', 20) # Define a fonte para o texto

		info1 = fonte.render('O jogo de damas eh praticado em um tabuleiro de 64 casas.', False, (AZUL)) # Cria um objeto de texto com a primeira regra do jogo, a fonte e a cor azul
		info2 = fonte.render('O objetivo do jogo eh capturar todas as pecas do oponente.', False, (VERDE_ESCURO)) # Cria um objeto de texto com a segunda regra do jogo, a fonte e a cor verde escuro
		info3 = fonte.render('A peca anda soh para frente, uma casa de cada vez, na diagonal.', False, (VERDE_ESCURO)) # Cria um objeto de texto com a terceira regra do jogo, a fonte e a cor verde escuro
		info4 = fonte.render('Quando a peca atinge a oitava linha do tabuleiro ela vira dama.', False, (VERDE_ESCURO)) # Cria um objeto de texto com a quarta regra do jogo, a fonte e a cor verde escuro
		info5 = fonte.render('A dama eh uma peca de movimentos mais amplos. Ela anda para frente e para tras,', False, (AZUL)) # Cria um objeto de texto com a quinta regra do jogo, a fonte e a cor azul
		info6 = fonte.render('quantas casas quiser, nao podendo saltar sobre uma peca da mesma cor. ', False, (AZUL)) # Cria um objeto de texto com a sexta regra do jogo, a fonte e a cor azul
		info7 = fonte.render('A captura e obrigatoria, ou seja, nao existe sopro.', False, (VERDE_ESCURO)) # Cria um objeto de texto com a sétima regra do jogo, a fonte e a cor verde escuro
		info8 = fonte.render('Duas ou mais pecas juntas, na mesma diagonal, nao podem ser capturadas.', False, (VERDE_ESCURO)) # Cria um objeto de texto com a oitava regra do jogo, a fonte e a cor verde escuro
		info9 = fonte.render('A peca e a dama podem capturar tanto para frente como para tras.', False, (AZUL)) # Cria um objeto de texto com a nona regra do jogo, a fonte e a cor azul
		info10 = fonte.render('O movimento de captura pode ser encadeado sem que o jogador passe a vez.', False, (AZUL)) # Cria um objeto de texto com a décima regra do jogo, a fonte e a cor azul
		
		
		game1 = fonte.render('Durante o jogo, ao clicar em uma peca, sera exibido em verde os movimentos', False, (VERMELHO)) # Cria um objeto de texto com a primeira dica do jogo, a fonte e a cor vermelha
		game2 = fonte.render('possiveis da mesma. Se nada acontecer ao clicar em uma peca, significa que', False, (VERMELHO)) # Cria um objeto de texto com a segunda dica do jogo, a fonte e a cor vermelha
		game3 = fonte.render('ela nao tem movimentos possiveis ou o turno pertence ao outro jogador.', False, (VERMELHO)) # Cria um objeto de texto com a terceira dica do jogo, a fonte e a cor vermelha

		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO) # Cria um objeto de texto com a mensagem de voltar ao menu, a fonte e a cor verde clara

		display.blit(info1, (25, 25)) # Desenha o texto da primeira regra na tela
		display.blit(info2, (25, 50)) # Desenha o texto da segunda regra na tela
		display.blit(info3, (25, 75)) # Desenha o texto da terceira regra na tela
		display.blit(info4, (25, 100)) # Desenha o texto da quarta regra na tela
		display.blit(info5, (25, 125)) # Desenha o texto da quinta regra na tela
		display.blit(info6, (25, 150)) # Desenha o texto da sexta regra na tela
		display.blit(info7, (25, 175)) # Desenha o texto da sétima regra na tela
		display.blit(info8, (25, 200)) # Desenha o texto da oitava regra na tela
		display.blit(info9, (25, 225)) # Desenha o texto da nona regra na tela
		display.blit(info10, (25, 250)) # Desenha o texto da décima regra na tela

		display.blit(game1, (25, 300)) # Desenha o texto da primeira dica na tela
		display.blit(game2, (25, 325)) # Desenha o texto da segunda dica na tela
		display.blit(game3, (25, 350)) # Desenha o texto da terceira dica na tela

		display.blit(voltar, (25, 550)) # Desenha o texto de voltar ao menu na tela

		pygame.display.update() # Atualiza a tela
		clock.tick(15) # Define o relógio para 15 FPS
# Função para exibir a tela do vencedor do jogo
def tela_vencedor(vencedor):
	sair = False # Define uma variável para controlar o laço

	while not sair: # Enquanto não sair
		for evento in pygame.event.get(): # Percorre os eventos da tela
			if evento.type == pygame.QUIT: # Se o evento for de sair
				sair = True # Define a variável de sair como verdadeira
				pygame.quit() # Encerra o pygame
				quit() # Encerra o programa
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN: # Se o evento for de pressionar uma tecla ou um botão do mouse
				sair = True # Define a variável de sair como verdadeira

		display.fill(PRETO) # Preenche a tela com a cor preta

		fonte = pygame.font.SysFont('comicsansms', 50) # Define a fonte para o texto

		surface_texto, rect_texto = None, None # Define duas variáveis para armazenar o objeto de texto e o retângulo que o contém

		if vencedor == "empate": # Se o vencedor for um empate
			surface_texto, rect_texto = text_objects("EMPATE!", fonte, BRANCO) # Cria um objeto de texto com a mensagem "EMPATE!", a fonte e a cor branca
		elif vencedor == "x": # Se o vencedor for o jogador 'x'
			surface_texto, rect_texto = text_objects("VITORIA DO  VERMELHO", fonte, VERMELHO) # Cria um objeto de texto com a mensagem "VITORIA DO VERMELHO", a fonte e a cor vermelha
		elif vencedor == "o": # Se o vencedor for o jogador 'o'
			surface_texto, rect_texto = text_objects("VITORIA DO BRANCO", fonte, BRANCO) # Cria um objeto de texto com a mensagem "VITORIA DO BRANCO", a fonte e a cor branca

		rect_texto.center = ((LARGURA / 2), ALTURA / 3) # Define o centro do retângulo do texto
		display.blit(surface_texto, rect_texto) # Desenha o texto na tela

		fonte = pygame.font.Font(None, 30) # Define a fonte para o texto de voltar ao menu
		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO) # Cria um objeto de texto com a mensagem de voltar ao menu, a fonte e a cor verde clara

		display.blit(voltar, (25, 550)) # Desenha o texto de voltar ao menu na tela

		pygame.display.update() # Atualiza a tela
		clock.tick(60) # Define o relógio para 60 FPS


# Função para exibir a tela do menu do jogo
def menu_jogo():
	while True: # Enquanto o jogo estiver rodando
		for evento in pygame.event.get(): # Percorre os eventos da tela
			if evento.type == pygame.QUIT: # Se o evento for de sair
				pygame.quit() # Encerra o pygame
				quit() # Encerra o programa

		display.fill(PRETO) # Preenche a tela com a cor preta
		fonte = pygame.font.SysFont('comicsansms', 50) # Define a fonte para o texto do título
		surface_texto, rect_texto = text_objects("Jogo de Damas", fonte, BRANCO) # Cria um objeto de texto com o título do jogo, a fonte e a cor branca
		rect_texto.center = ((LARGURA / 2), ALTURA / 3) # Define o centro do retângulo do texto
		display.blit(surface_texto, rect_texto) # Desenha o texto na tela

		# Cria quatro botões na tela, cada um com uma mensagem, uma posição, duas cores, uma cor de texto e uma ação
		cria_botao("INICIAR",(LARGURA - 760, ALTURA / 2, 120, 40), VERDE_CLARO, VERDE_ESCURO, BRANCO, loop_jogo) # Botão para iniciar o jogo, que chama a função loop_jogo
		cria_botao("MANUAL",(LARGURA - 560, ALTURA / 2, 120, 40), BRANCO, CINZA, PRETO, regras) # Botão para ver o manual do jogo, que chama a função regras
		cria_botao("CREDITOS",(LARGURA - 360, ALTURA / 2, 120, 40), BRANCO, CINZA, PRETO, creditos) # Botão para ver os créditos do jogo, que chama a função creditos
		cria_botao("SAIR",(LARGURA - 160, ALTURA / 2, 120, 40), VERMELHO_CLARO, VERMELHO, BRANCO, sair) # Botão para sair do jogo, que chama a função sair

		pygame.display.update() # Atualiza a tela
		clock.tick(15) # Define o relógio para 15 FPS

# Função para sair do jogo
def sair():
	pygame.quit() # Encerra o pygame
	quit() # Encerra o programa

# Funções auxiliares no loop do jogo
def coluna_clicada(pos):
	x = pos[0] # Obtém a coordenada x da posição do mouse
	for i in range(1, 8): # Percorre as oito colunas do tabuleiro
		if x < i * ALTURA / 8: # Se a coordenada x for menor que o limite da coluna
			return i - 1 # Retorna o índice da coluna
	return 7 # Se não encontrar nenhuma coluna, retorna 7

def linha_clicada(pos):
	y = pos[1] # Obtém a coordenada y da posição do mouse
	for i in range(1, 8): # Percorre as oito linhas do tabuleiro
		if y < i * ALTURA / 8: # Se a coordenada y for menor que o limite da linha
			return i - 1 # Retorna o índice da linha
	return 7 # Se não encontrar nenhuma linha, retorna 7

# Função para executar o loop da tela do jogo de damas
def loop_jogo():
	sair = False # Define uma variável para controlar o laço

	jogo = Jogo() # Cria um objeto da classe Jogo

	while not sair: # Enquanto não sair
		for evento in pygame.event.get(): # Percorre os eventos da tela
			if evento.type == pygame.QUIT: # Se o evento for de sair
				sair = True # Define a variável de sair como verdadeira
				pygame.quit() # Encerra o pygame
				quit() # Encerra o programa
			if evento.type == pygame.MOUSEBUTTONDOWN: # Se o evento for de clicar com o mouse
				jogo.avalia_clique(pygame.mouse.get_pos()) # Chama o método avalia_clique do objeto jogo, passando a posição do mouse


		display.fill(PRETO) # Preenche a tela com a cor preta
		jogo.desenha() # Chama o método desenha do objeto jogo

		vencedor = jogo.verifica_vencedor() # Chama o método verifica_vencedor do objeto jogo e armazena o resultado na variável vencedor

		if vencedor is not None: # Se houver um vencedor
			sair = True # Define a variável de sair como verdadeira
			tela_vencedor(vencedor) # Chama a função tela_vencedor, passando o vencedor

		pygame.display.update() # Atualiza a tela
		clock.tick(60) # Define o relógio para 60 FPS

menu_jogo() # Chama a função menu_jogo
pygame.quit() # Encerra o pygame
quit() # Encerra o programa
