# Grupo 32:
# 95735 António Marçal
# 99122 Sofia Sancho

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
        
    def __str__(self):
        return 'ID: ' + str(self.id) + '\n' +  str(self.board)

    def __lt__(self, other):
        res1 = 0
        res2 = 0
        n = self.board.n
        for i in range(n):
            for j in range(n):
                if self.board.get_number(i, j) == 2:
                   res1 += 1
                if other.board.get_number(i, j) == 2:
                   res2 += 1
        return res1 < res2 


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, n, board):
        """O construtor especifica o estado inicial."""
        self.n = n
        self.board = board
        
    def __str__(self):
        s = ''
        for i in self.board:
            for j in i:
                s += str(j) + '\t'
            s = s[:len(s)-1] + '\n'
        return s[:len(s)-1]
    
    def copy_board(self):
        newBoard = []
        for v in self.board:
            line = []
            for col in v:
                line += [col]
            newBoard += [line]
        return Board(self.n, newBoard)

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""

        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente acima e abaixo,
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
                
        n = int((sys.stdin.readline()).rstrip('\n'))
        board_lst = [[] for x in range(n)]

        for i in range(n):
            board_lst[i] = [int(j) for j in sys.stdin.readline() if j != '\n' and j != '\t']

        return Board(n, board_lst)


class Takuzu(Problem):
    
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        board = state.board
        actions = []
        
        pos = []
        
        #contagem de 1's e 0's por linha e coluna
        rowCounts = [[0, 0] for x in range(board.n)]
        colCounts = [[0, 0] for x in range(board.n)]
        for i in range(board.n):
            for j in range(board.n):
                
                if board.get_number(i, j) in (0, 1): 
                    #se encontrar uma posicao preenchida, +1 nessa linha e coluna
                    rowCounts[i][board.get_number(i, j)] += 1
                    colCounts[j][board.get_number(i, j)] += 1
                else:
                    for value in (0, 1):
                        if value not in board.adjacent_horizontal_numbers(i, j)\
                            and value not in board.adjacent_vertical_numbers(i, j):
                            actions += [(i, j , value)]
                            pos += [(i,j)]
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
                             
                            if isgood == 'Maybe':
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
                                pos += [(i,j)]
        
        
            for x in range(len(pos)):
                if (pos.count(pos[x]) == 1):
                    return [actions[x]]
        
        max = board.n//2 + board.n%2      
        newActions = []
        once = True
        for act in actions:
            if (rowCounts[act[0]][0] < max and act[2] == 0) or\
                (rowCounts[act[0]][1] < max and act[2] == 1):
                    
                if (colCounts[act[1]][0] < max and act[2] == 0) or\
                (colCounts[act[1]][1] < max and act[2] == 1):
                    if newActions == []:
                        newActions += [act]
                    elif (newActions[-1][0] == act[0]) & (newActions[-1][1] == act[1]):
                        once = False
                        newActions += [act]
                    elif once:
                        return [newActions[-1]]
                    else:
                        once = True
                        newActions += [act] 
        
        #caso só houver posições com duas opções, ele escolhe a 1a
        return newActions[0:2]

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        newBoard = state.board.copy_board()
        newBoard.board[action[0]][action[1]] = action[2]
        return TakuzuState(newBoard)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        line = []
        col = []
        conjunto_line = []
        conjunto_col = []
        n = state.board.n

        for i in range(n):
            for j in range(n):
                pos_line = state.board.get_number(i, j)
                pos_col = state.board.get_number(j, i)
                line.append(pos_line)
                col.append(pos_col)

                if (pos_line == 2 or pos_col == 2): 
                    return False
					
            if n % 2 == 0:
                if line.count(1) != line.count(0) or line.count(1) + line.count(0) != n:
                    return False
                if col.count(1) != col.count(0) or col.count(1) + col.count(0) != n:
                    return False
				
            if n % 2 == 1:
                if abs(line.count(1) - line.count(0)) != 1 or line.count(1) + line.count(0) != n:
                    return False
                if abs(col.count(1) - col.count(0)) != 1 or col.count(1) + col.count(0) != n:
                    return False
				
            conjunto_line.append(line.copy())
            conjunto_col.append(col.copy())
            line = []
            col = []

        for i in range (len(conjunto_line)):
            if conjunto_line.count(conjunto_line[i]) > 1 or conjunto_col.count(conjunto_col[i]) > 1:
                return False

        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        res = 0
        n = node.state.board.n
        for i in range(n):
            for j in range(n):
                if node.state.board.get_number(i, j) == 2:
                   res += 1
        return res


if __name__ == "__main__":
    
    # Lê o tabuleiro do stdin
    board = Board.parse_instance_from_stdin()
    
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)

    # # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board, sep="")
