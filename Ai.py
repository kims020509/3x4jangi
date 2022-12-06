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
piece_score = {'K' : 100 , 'S' : 3, 'J' : 3, 'H' : 2, 'Z' : 1}
x_score_dic = {0 : 0.1, 1 : 0.2, 2 : 0.2, 3 : 0.1}
y_score_dic = {0 : -0.1 , 1 : 0, 2 : -0.1}

def print_(board, catch):
    print('='*11)
    for y in range(3):
        for x in range(4):
            print(board[y][x], end=' ')
        print()
    print('-'*11)
    print('PL : ', end='')
    for piece in catch[0]:
        print(piece, end=' ')
    print()
    print('AI : ', end='')
    for piece in catch[1]:
        print(piece, end=' ')
    print()
    print('='*11)

def calc_expt(board, catch):
    total_score = 0
    K_in = [False, False]
    for y in range(3):
        for x in range(4):
            piece = board[y][x]
            if piece == '--' : continue
            ptype = type_dic[piece[0]]
            ttype = int(piece[1])
            if ptype == 0: K_in[ttype] = True
            score_index = y * 4 + x
            score = db.score[ptype + 5*ttype][score_index]
            if ttype: total_score += score
            else: total_score -= score
    if len(catch[0]):
        for p in catch[0]:
            total_score += piece_score[p]
    if len(catch[1]):
        for a in catch[1]:
            total_score += piece_score[a]
    
    if not K_in[0]: return np.inf
    if not K_in[1]: return -np.inf
    return total_score

# root = Node("root", data= board, expt= calc_expt(board))        

def Aing(board, catch, depth):
    root = Node("root", data1= board, data2= catch, expt= calc_expt(board, catch)) 
    Best = minimax(root, depth, -np.inf, np.inf, True)
    # print("=="*20)
    # for row in RenderTree(root):
    #     pre, fill, node = row
    #     print(f"{pre}{node.name}, expt: {node.expt:.2f}")
    # print("=="*20)
    for i in range(depth - 1):
        Best = Best.parent
    # print("=" * 8 + "Recommand" + "="*8)
    # print_(board, catch)
    # print_(Best.data1, Best.data2)
    # print("=" * 25)
    return Best.data1, Best.data2


def minimax(node, depth, alp, bet, maximizingPlayer):
    if depth == 0 : return node
    if node.expt == np.inf or node.expt == -np.inf: return node
    minimax_value(node, depth, maximizingPlayer)
    if len(node.children) == 0 : return 0

    alpha = Node("alpha", data1= None, data2= None, expt= alp)
    beta = Node("beta", data1= None, data2= None, expt= bet)
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
    sf = int(maximaizingPlayer)
    ot = int(not maximaizingPlayer)
    for y in range(3):
        for x in range(4):
            piece = node.data1[y][x]
            if piece[0] == '-' :
                if len(node.data2[sf]):
                    if sf: key = x > 1
                    else: key = x < 2
                    if key:
                        for i in range(len(node.data2[sf])):
                            temp = node.data2[sf][i]
                            del node.data2[sf][i]
                            node.data1[y][x] = f'{temp}{sf}'
                            name = f"{chr(64+depth)}@{i}"
                            new_Node = Node(name, node, data1= np.array(node.data1), data2= [node.data2[0][:], node.data2[1][:]],  expt= calc_expt(node.data1, node.data2))
                            node.data1[y][x] = '--'
                            node.data2[sf].insert(i, temp)
                continue
            if piece[1] == f'{ot}' : continue
            ptype = type_dic[piece[0]] + 5*sf
            nx = [1, 0, -1, 1, 0, -1, 1, 0, -1]
            ny = [1, 1, 1, 0, 0, 0, -1, -1, -1]
            for idx in range(9):
                dx, dy = x + nx[idx], y +ny[idx]
                if not -1 < dx < 4 or not -1 < dy < 3: continue 
                tpiece = node.data1[dy][dx]
                if tpiece[1] == f'{sf}': continue
                if db.piece_go[ptype][idx]:
                    iscatch = False
                    if tpiece[1] == f'{ot}':
                        if tpiece[0] == 'H': node.data2[sf].append('Z')
                        else: node.data2[sf].append(tpiece[0])
                        iscatch = True
                    if ptype == 8 and dx < 2 :
                        node.data1[dy][dx] = 'H1'
                    elif ptype == 3 and dx > 1:
                        node.data1[dy][dx] = 'H0'
                    else:
                        node.data1[dy][dx] = piece
                    node.data1[y][x] = '--'
                    # print_(node.data1, node.data2)
                    name = f"{chr(64+depth)}{ptype}{idx}"
                    new_Node = Node(name, node, data1= np.array(node.data1), data2= [node.data2[0][:], node.data2[1][:]],  expt= calc_expt(node.data1, node.data2))
                    if iscatch: 
                        if tpiece[0] == 'H': node.data2[sf].remove('Z')
                        else: node.data2[sf].remove(tpiece[0])
                    node.data1[dy][dx] = tpiece
                    node.data1[y][x] = piece
if __name__ == '__main__':
    Aing(board, catch, 1)
