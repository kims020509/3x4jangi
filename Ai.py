import numpy as np
import dicBoard as db

Tree = []

type_dic = {'K' : 0, 'S' : 1, 'J' : 2, 'Z' : 3, 'H' : 4}
piece_score_dic = {'K' : 100 , 'S' : 3, 'J' : 3, 'H' : 2, 'Z' : 1}
x_score_dic = {0 : 0.1, 1 : 0.2, 2 : 0.2, 3 : 0.1}
y_score_dic = {0 : -0.1 , 1 : 0, 2 : -0.1}

def print_(board):
    print('-'*11)
    for y in range(3):
        for x in range(4):
            print(board[y][x], end=' ')
        print()
    print('-'*11)

def calc_expt(board):
    total_score = 0
    for y in range(3):
        for x in range(4):
            piece = board[y][x]
            if piece == '--' : continue
            own_score = 1 if piece[1] == '1' else -1
            piece_socre = piece_score_dic[piece[0]]
            special_socre = -1 if piece_socre == 2 else 1
            xy_score = (1 + x_score_dic[x] * special_socre)*(1 + y_score_dic[y])
            score = piece_socre * xy_score * own_score
            print(f'{piece}: {score:.2f}, ', end= ' ')
            total_score += score
    print()
    return total_score
            
def checkCASE(board):
    global Tree
    for y in range(3):
        for x in range(4):
            piece = board[y][x]
            if piece[0] == '-' : continue
            if piece[1] == '0' : continue
            ptype = type_dic[piece[0]]
            nx = [1, 0, -1, 1, 0, -1, 1, 0, -1]
            ny = [1, 1, 1, 0, 0, 0, -1, -1, -1]
            for idx in range(9):
                dx, dy = x + nx[idx], y +ny[idx]
                if not -1 < dx < 4 or not -1 < dy < 3: continue 
                tpiece = board[dy][dx]
                if tpiece[1] == '1': continue
                if db.piece_go[ptype][idx]:
                    tmp_board = [item[:] for item in board]
                    tmp_board[dy][dx] = piece
                    tmp_board[y][x] = '--'
                    print_(tmp_board)
                    print(calc_expt(tmp_board))
                    tmp_board[dy][dx] = tpiece
                    tmp_board[y][x] = piece
                    
def minimax():
    for item in Tree:
        print(calc_expt(item))