import numpy as np
import dicBoard as db
import Ai

board = np.array([
    ['S0', '--', '--', 'S1'], 
    ['K0', 'Z0', 'Z1', 'K1'],
    ['J0', '--', '--', 'J1']])
catch = [[], []]

stay_win = [0, 0]

def print_(board, catch):
    print("┌───────────────────┐")
    for y in range(3):
        print("│    ", end= "")
        for x in range(4):
            print(board[y][x], end=' ')
        print("   │")
    print('└───────────────────┘')
    print('PL : ', end='')
    for piece in catch[0]:
        print(piece, end=' ')
    print()
    print('AI : ', end='')
    for piece in catch[1]:
        print(piece, end=' ')
    print()
    print("─────────────────────")

def getlocalXY(x, y): #return direction index
        return (1 - y) * 3 + 1 - x

def getBoardNow(board, xy):
    return board[xy[1] - 1][xy[0] - 1]

def isIn(x, y):
    if x > 4 or y > 3: return False
    return True

def isEmpty(board, xy):
    if board[xy[1] - 1][xy[0] - 1] == "--": return True
    return False

def isCatch(catch, type_, turn):
    if catch[turn].count(type_) > 0: return True
    return False

def isCanGo(board, new_xy, old_xy, type_, turn):
    type_num = db.type_dic[type_]
    dx, dy = (new_xy[0] - old_xy[0], new_xy[1] - old_xy[1])
    if turn: dx = -dx
    index = getlocalXY(dx, dy)
    if not db.piece_go[type_num][index]: return False
    if getBoardNow(board, new_xy)[1] == turn: return False
    return True

def findXY(board, new_xy, type_, turn):
    temp_xy = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            dx, dy = (new_xy[0] + x - 1, new_xy[1] + y - 1)
            if isIn(dx, dy):
                if board[dy][dx] == f'{type_}{turn}':
                    temp_xy.append(((dx + 1), (dy + 1)))
    return temp_xy

def setPiece(board, new_xy, type_, turn):
    board[new_xy[1] - 1][new_xy[0] - 1] = f'{type_}{turn}'
    return board

def move(board, catch, old_xy, new_xy, type_ = '-', turn = '-'):
    if isCanGo(board, new_xy, old_xy, type_, turn):
        if not isEmpty(board, new_xy):
            catch[turn].append(getBoardNow(board, new_xy)[0])
        if type_ == 'Z' and new_xy[0] == 3 - turn:
            board = setPiece(board, new_xy, 'H', turn)
            board = setPiece(board, old_xy, '-', '-')
        else:
            board = setPiece(board, new_xy, type_, turn)
            board = setPiece(board, old_xy, '-', '-')
    return board, catch

def place(board, catch, new_xy, type_, turn):
    board = setPiece(board, new_xy, type_, turn)
    catch[turn].remove(type_)
    return board, catch

def Player(board, catch, old_xy, com_xy, type_, isMove):
    if isMove:
        return move(board, catch, old_xy, com_xy, type_, 0)
    else:
        return place(board, catch, com_xy, type_, 0)

def Ai_(board, catch):
    return Ai.Aing(board, catch, 3)

def input_command(board, catch):
    isMove = True
    while 1:
        print("다음 수를 입력하세요...")
        command = input()
        arr = [i for i in command]
        if (arr[0] in db.type_dic) and (arr[1] in db.y_axis) and (0 < int(arr[2]) < 5):
            com_xy = (int(arr[2]), db.y_axis[arr[1]])
            type_ = arr[0]
            if len(arr) == 3:
                temp_xy = findXY(board, com_xy, type_, 0)
                count = len(temp_xy)
                if  count == 1:
                    old_xy = temp_xy[0]
                    break
                elif count > 1:
                    print("움직일 말을 선택해 주세요...")
                    for i in range(count):
                        print(f"{i} : {type_}{temp_xy[i][1]}{temp_xy[i][0]}", end=" ")
                    print()
                    print("선택할 말의 번호를 입력해 주세요...", end= " ")
                    t = input()
                    while 1:
                        if t.isdigit() and (-1 < int(t) < count):
                            break
                        print("다시 입력해주세요...", end= " ")
                        t = input()
                    old_xy = temp_xy[int(t)]
                    break
                else:
                    print("가능하지 않습니다.")
            elif len(arr) == 4:
                if arr[-1] == "!" and isCatch(catch, type_, 0) and isEmpty(board, com_xy) and com_xy[0] < 3:
                    isMove = False
                    old_xy = (0, 0)
                    break
                else:
                    print("잘못된 입력입니다.")
            else:
                print("길거나 짧은 입력입니다.")
        else:
            print("잘못된 입력입니다")
    return old_xy, com_xy, type_, isMove

if __name__ == '__main__':
    print_(board, catch)
    while 1:
        old_xy, com_xy, type_, isMove  = input_command(board, catch)
        print(old_xy, com_xy, type_, isMove)
        board, catch = Player(board, catch, old_xy, com_xy, type_, isMove)
        print_(board, catch)
        board, catch = Ai_(board, catch)
        print_(board, catch)
