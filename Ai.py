import numpy as np
import math

Tree = np.array([])

piece_score_dic = {'K' : 100 , 'S' : 3, 'J' : 3, 'H' : 2, 'Z' : 1}
x_score_dic = {0 : 0.1, 1 : 0.2, 2 : 0.2, 3 : 0.1}
y_score_dic = {0 : -0.1 , 1 : 0, 2 : -0.1}

class case:
    def __init__(self, BOARD):
        self.board = BOARD

    def calc_expt(self):
        total_score = 0
        for i in range(3):
            for j in range(4):
                piece = self.board[i][j]
                if piece == '--' : continue
                own_score = 1 if piece[1] == '1' else -1
                piece_socre = piece_score_dic[piece[0]]
                special_socre = -1 if piece_socre == 2 else 1
                xy_score = (1 + x_score_dic[j] * special_socre)*(1 + y_score_dic[i])
                score = piece_socre * xy_score * own_score
                print(f'{piece}: {score:.2f}, ', end='')
                total_score += score
        print()
        return total_score
            
def checkCASE():
    pass
