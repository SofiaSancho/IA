# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# Antonio criei (temporaria) __str__
class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1
        
    def __str__(self):
        return 'ID: ' + str(self.id) + str(self.board)

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    #Sofia. criei a função __init__, fiz a get_number, adjacentes e parce_instance_from_stdin
    #Antonio criei (temporaria) __str__ e ajustei o get_number para colunas de 0 a n-1

    def __init__(self, n, board):
        """O construtor especifica o estado inicial."""
        self.n = n
        self.board = board
        
    def __str__(self):
        s = ''
        for i in self.board:
            for j in i:
                s += str(j) + '\t'
            s = s[:len(s)] + '\n'
        return s[:len(s)]

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""

        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        anterior = None if row-1 < 0 else self.board[row-1][col]
        posterior = None if row >= self.n - 1 else self.board[row + 1][col]

        return (anterior, posterior)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        anterior = None if col-1 < 0 else self.board[row][col-1]
        posterior = None if col >= self.n - 1 else self.board[row][col+1]

        return (anterior, posterior)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        #Leitura do input. n -> tamanho do tabuleiro. board_lst -> lista com os valores de cada posição do tabuleiro
        #retorna uma instância do Board com os atributos que leu do input
        
        # Antonio. ignora estes comentarios. E so para eu conseguir testar no IDE
        # try:
        # f = open ('testes-takuzu/input_T01', 'r')
        # n = int((f.readline()).rstrip('\n'))
        # # except:
        # board_lst = [[] for x in range(n)]

        # for i in range(n):
        #     board_lst[i] = [int(j) for j in f.readline() if j != '\n' and j != '\t']
            
        # f.close()
        # return Board(n, board_lst)
                
        n = int((sys.stdin.readline()).rstrip('\n'))
        board_lst = [[] for x in range(n)]

        for i in range(n):
            board_lst[i] = [int(j) for j in sys.stdin.readline() if j != '\n' and j != '\t']

        return Board(n, board_lst)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    
    # adicionei __init__, result e actions
    # Sofia: fiz o goal_test
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        board = state.board
        actions = []
        rowCounts = [[0, 0] for x in range(board.n)]
        colCounts = [[0, 0] for x in range(board.n)]
        for i in range(board.n):
            for j in range(board.n):
                
                if board.get_number(i, j) in (0, 1):
                    rowCounts[i][board.get_number(i, j)] += 1
                    colCounts[j][board.get_number(i, j)] += 1
                else:
                    for value in (0, 1):
                            
                        if value not in board.adjacent_horizontal_numbers(i, j)\
                            and value not in board.adjacent_vertical_numbers(i, j):
                            actions += [(i, j , value)]
                        else:
                            # horizontais
                            isgood = 'Yes'
                            if board.adjacent_horizontal_numbers(i, j)[0] == value:
                                
                                isgood = 'Maybe'
                                
                                if board.adjacent_horizontal_numbers(i, j - 1)[0] == value:
                                    isgood = 'No'
                                
                            if isgood != 'No' and board.adjacent_horizontal_numbers(i, j)[1] == value:
                                
                                if isgood == 'Maybe':
                                    isgood = 'No'
                                elif board.adjacent_horizontal_numbers(i, j + 1)[1] == value:
                                    isgood = 'No'
                                else:
                                    isgood = 'Yes'
                                    
                            # verticais 
                            if isgood != 'No' and board.adjacent_vertical_numbers(i, j)[0] == value:
                                
                                isgood = 'Maybe'
                                
                                if board.adjacent_vertical_numbers(i - 1, j)[0] == value:
                                    isgood = 'No'
                                
                            if isgood != 'No' and board.adjacent_vertical_numbers(i, j)[1] == value:
                                
                                if isgood == 'Maybe':
                                    isgood = 'No'
                                
                                elif board.adjacent_vertical_numbers(i + 1, j)[1] == value:
                                    isgood = 'No'
                            
                            if isgood != 'No':
                                actions += [(i, j , value)]
                                
        newActions = []
        for act in actions:
            if (rowCounts[act[0]][0] < board.n/2 and act[2] == 0) or\
                (rowCounts[act[0]][1] < board.n/2 and act[2] == 1):
                    
                if (colCounts[act[1]][0] < board.n/2 and act[2] == 0) or\
                (colCounts[act[1]][1] < board.n/2 and act[2] == 1):
                    newActions += [act]
                
        return newActions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        newBoard = state.board.board.copy()
        newBoard[action[0]][action[1]] = action[2]
        return TakuzuState(Board(len(newBoard), newBoard))

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        board = state.board

        line = []
        n = state.board.n
        #muda aqui o nheco, tava sem ideias, haha ok
        for fila in ("linha", "coluna"):
            for i in range(n):
                for j in range(n):
                    pos = state.board.get_number(i, j) if fila == "linha" else state.board.get_number(j,i)
                    line.append(pos)
                    if (pos == 2):
                        return False
                if (n % 2 == 0 and line.count(1) != line.count(0)):
                    return False
                if (n % 2 == 1 and (line.count(1) != line.count(0) + 1 or line.count(1) != line.count(0) - 1)):
                    return False
                line = []

        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


# Antonio acrescentei mais dados de teste
if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance_from_stdin()
    puzzle = Takuzu(board)
    initial = TakuzuState(board)
    """ pra testar o goal_test (no teste 1)
    newState = puzzle.result(initial, (0,0,0))
    newState = puzzle.result(initial, (0,1,1))
    newState = puzzle.result(initial, (1,2,0))
    newState = puzzle.result(initial, (2,1,1))
    newState = puzzle.result(initial, (3,1,0))
    newState = puzzle.result(initial, (3,2,1))
    newState = puzzle.result(initial, (3,3,0))

    print(newState)

    print(puzzle.goal_test(newState))
    """
    
    newState = puzzle.result(initial, (0, 1, 0))
    puzzle.actions(newState)
