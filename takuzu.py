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
        return str(self.board)

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    #Sofia. criei a função __init__, fiz a get_number, adjacentes e parce_instance_from_stdin
    #Antonio criei (temporaria) __str__ e ajustei o get_number para colunas de 0 a n-1

    def __init__(self, n, board):
        self.n = n
        self.board = board
        
    def __str__(self):
        s = str(self.n)
        for i in board.board:
            s += '\n' + str(i)
        return s

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""

        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        anterior = None if row-2 < 0 else self.board[row-2][col-1]
        posterior = None if row >= self.n else self.board[row][col-1]

        return (anterior, posterior)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        anterior = None if col-2 < 0 else self.board[row-1][col-2]
        posterior = None if col >= self.n else self.board[row-1][col]

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

        
        n = int((sys.stdin.readline()).rstrip('\n'))

        board_lst = [[] for x in range(n)]

        for i in range(n):
            board_lst[i] = [int(j) for j in sys.stdin.readline() if j != '\n' and j != '\t']

        return Board(n, board_lst)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    
    # adicionei __init__, result e actions
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        actions = []
        for i in range(state.board.n):
            for j in range(state.board.n):
                if state.board.get_number(i, j) == 2:
                    actions += [(i, j, 0)] + [(i, j, 1)]
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        newBoard = state.board
        newBoard.board[action[0]][action[1]] = action[2]
        return TakuzuState(newBoard)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

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
    newState = puzzle.result(initial, (2, 2, 6))
    pass
