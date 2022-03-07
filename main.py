import chess
import random

class Xadrez:
  def __init__(self):
    self.cores = ["White", "Black"]
    self.ultima_cor = None

  def inicializar(self, estado = None):
    if(estado is None):
      self.board = chess.Board()

  # Copia o estado atual do tabuleiro
  def retorna_estado(self):
    return self.board.copy()

  # Função que realiza o movimento das jogadas
  def jogar(self, acao, simbolo):
    self.board.push_san(acao)
    self.ultima_cor = simbolo

  def print_sucessora(self, lista_acoes):
    lista_moves = []
    lista_acoes = list(self.board.legal_moves)
    
    for index in range(0, len(lista_acoes)):
      var = lista_acoes[index]
      lista_moves.append(str(var))

    print(str(lista_moves) + "\n")
    return lista_moves
    
  # Mostra a lista de movimentos válidos, como a função sucessora da modelagem
  def sucessora(self):
    lista_movimentos = list(self.board.legal_moves)
    return lista_movimentos

  # Retorna 1 caso retorne vitória para a máquina, 0 caso retorne um empate e -1 caso retorne uma derrota
  def utilidade(self, turno):
    if(self.fim_de_jogo() != ""):
      if (self.fim_de_jogo() == "Empate" or self.fim_de_jogo() == "O jogo acabou"):
        return 0
      else:
        if self.ultima_cor == turno:
          return 1
        else:
          return -1

  # Heuristica - Abertura Italina: O objetivo é controlar rapidamente o centro com o seu peão e cavalo, e então colocar o bispo em uma das casas mais perigosas.
  def abertura_italiana(self, turno, count):
    abertura = ["e2e4", "g1f3", "f1c4"]
    return abertura[count]

  # Função que verifica os estados terminais, tais como checkmate(vitória), rei sem movimento(empate), não há peças para cheque-mate(empate) e jogo acabou
  def fim_de_jogo(self):
    if (self.board.is_checkmate()):
      return "Cheque-Mate"
    if (self.board.is_stalemate()):
      return "Empate" # - Rei sem movimento
    if (self.board.is_insufficient_material()):
      return "Empate" # - Não há peças para cheque-mate
    if (self.board.is_game_over()):
      return "O jogo acabou"
    return ""
      
    def __str__(self):
      return 'value of a = {} value of b =     {}'.format(self.a, self.b)

# O minimax é uma função que minimixa a perda e maximixa o ganho
def minimax(estado, acao, turno, simbolo_agente, guardaMov, copia_estado):
  copia_estado.board = estado.retorna_estado()
  
  if copia_estado.fim_de_jogo() != "":
    return copia_estado.utilidade(simbolo_agente)

  if simbolo_agente == turno:
    utilidade = -1000
    if guardaMov == True:
      copia_estado.jogar(str(acao), turno)
      turno = "Preto"
      utilidade = max(utilidade, minimax(copia_estado, acao, turno, "Branco", False, copia_estado))
      return utilidade
    else:
      acao = random.choice(copia_estado.sucessora())
      copia_estado.jogar(str(acao), turno)
      turno = "Preto"
      utilidade = max(utilidade, minimax(copia_estado, acao, turno, "Branco", False, copia_estado))
      return utilidade
  else:
    utilidade = +1000
    acao = random.choice(copia_estado.sucessora())
    copia_estado.jogar(str(acao), turno)
    turno = "Branco"
    utilidade = min(utilidade, minimax(copia_estado, acao, turno, "Branco", False, copia_estado))
    return utilidade

x = Xadrez()
x.inicializar()

copia_estado = Xadrez()
copia_estado.inicializar()

print("Tabuleiro Inicial\n")
print(x.board)

jogador_cor = "Branco"
turno = "Branco"

count = 0

while (not x.fim_de_jogo() != ""):
  # Turno das peças brancas / máquina
  if turno == "Branco":
    print("\n---- Maquina ----\n")
    if count < 3:
      acao = x.abertura_italiana(turno, count)
      x.jogar(str(acao), turno)
      turno = "Preto"
      print(x.board)
      count += 1
    else:
      while True:
        acao = random.choice(x.sucessora())
        retorno = minimax(x, acao, turno, "Branco", True, copia_estado)
        if retorno >= 0:
          x.jogar(str(acao), turno)
          print(x.board)
        if not retorno < 0:
          turno = "Preto"
          break

    # Turno das peças pretas / jogador
    print("\n---- jogador ---- \n")   
    while True:  
      bool = False
      lista_acao = x.print_sucessora(x.sucessora())
      acao = input("Digite o movimento: ")
      for index in lista_acao:
        retorno = index
        if acao == retorno:
          x.jogar(str(acao), turno)
          print(x.board)
          bool = True
      if bool == True:
        turno = "Branco"
        break

      # Automatiza as jogadas das peças Pretas  
      # acao = random.choice(x.sucessora())
      # retorno = minimax(x, acao, turno, "Preto", True, copia_estado)
      # if retorno >= 0:
      #   x.jogar(str(acao), turno)
      #   print(x.board)
      # if not retorno < 0:
      #   turno = "Branco"
      #   break
  
if(x.fim_de_jogo() == "Cheque-Mate"):
  print("O vencedor é " + x.ultima_cor)
else:
  print("Empate")