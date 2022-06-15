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


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    #Sofia. criei a função __init__, fiz a get_number, adjacentes e parce_instance_from_stdin

    def __init__(self, n, board):
        self.n = n
        self.board = board

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""

        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        anterior = None if row-2 < 0 else self.board[row-1][col]
        posterior = None if row >= self.n else self.board[row+1][col]

        return (anterior, posterior)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        anterior = None if col-2 < 0 else self.board[row][col-1]
        posterior = None if col >= self.n else self.board[row][col+1]

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
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

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


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    #Sofia
    board = Board.parse_instance_from_stdin()
    """" prints pra testar
    print(board.n) 
    for i in board.board:
        print(i)

    print(board.adjacent_horizontal_numbers(3,2))
    """
    pass
