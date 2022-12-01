import numpy as np
import dicBoard as db
from anytree import Node, RenderTree

board = np.array([
    ['S0', '--', '--', 'S1'], 
    ['K0', 'Z0', 'Z1', 'K1'],
    ['J0', '--', '--', 'J1']])
catch = [[], []]
win = [0, 0]

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

# root = Node("root", data= board, expt= calc_expt(board))        

def Aing(board, catch, depth):
    root = Node("root", data= board, expt= calc_expt(board)) 
    Best = minimax(root, depth, -np.inf, np.inf, True)
    print("=="*20)
    for row in RenderTree(root):
        pre, fill, node = row
        print(f"{pre}{node.name}, expt: {node.expt:.2f}")
    print("=="*20)
    for i in range(depth - 1):
        Best = Best.parent
    print("=" * 8 + "Recommand" + "="*8)
    print_(board)
    print_(Best.data)
    print("=" * 25)
    return Best.data


def minimax(node, depth, alp, bet, maximizingPlayer):
    if depth == 0 : return node
    minimax_value(node, depth, maximizingPlayer)
    if len(node.children) == 0 : return 0

    alpha = Node("alpha", data= None, expt= alp)
    beta = Node("beta", data= None, expt= bet)
    if maximizingPlayer:
        for child in node.children:
            val = minimax(child, depth - 1, alpha.expt, beta.expt, False)
            if alpha.expt < val.expt:
                alpha = val
            if beta.expt <= alpha.expt:
                break
        return alpha
    else:
        for child in node.children:
            val = minimax(child, depth - 1, alpha.expt, beta.expt, True)
            if beta.expt > val.expt:
                beta = val
            if beta.expt <= alpha.expt:
                break
        return beta

def minimax_value(node, depth, maximaizingPlayer):
    print("==" * 22)
    print(f"{depth} 단계 탐색")
    print("==" * 22)

    sf = int(maximaizingPlayer)
    ot = int(not maximaizingPlayer)

    for y in range(3):
        for x in range(4):
            piece = node.data[y][x]
            if piece[0] == '-' : continue
            if piece[1] == f'{ot}' : continue
            ptype = type_dic[piece[0]] + 5*sf
            nx = [1, 0, -1, 1, 0, -1, 1, 0, -1]
            ny = [1, 1, 1, 0, 0, 0, -1, -1, -1]
            for idx in range(9):
                dx, dy = x + nx[idx], y +ny[idx]
                if not -1 < dx < 4 or not -1 < dy < 3: continue 
                tpiece = node.data[dy][dx]
                if tpiece[1] == f'{sf}': continue
                if db.piece_go[ptype][idx]:
                    if ptype == 8 and dx < 2 :
                        node.data[dy][dx] = 'H1'
                    elif ptype == 3 and dx > 1:
                        node.data[dy][dx] = 'H0'
                    else:
                        node.data[dy][dx] = piece
                    node.data[y][x] = '--'
                    print_(node.data)
                    new_Node = Node(f"{chr(64+depth)}{ptype}{idx}", node, data= np.array(node.data), expt= calc_expt(node.data))
                    node.data[dy][dx] = tpiece
                    node.data[y][x] = piece

if __name__ == '__main__':
    Aing(board, catch, 3)
