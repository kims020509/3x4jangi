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

def reset_board(board, catch):
    board = np.array([
    ['S0', '--', '--', 'S1'], 
    ['K0', 'Z0', 'Z1', 'K1'],
    ['J0', '--', '--', 'J1']])
    catch = [[], []]
    return board, catch

def getlocalXY(x, y): #return direction index
        return (1 - y) * 3 + 1 - x

def getBoardNow(board, xy):
    return board[xy[1] - 1][xy[0] - 1]

def isIn(x, y):
    if (x > 4) or y > 3: return False
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

def isWin(board, catch, turn):
    global stay_win
    for y in range(3):
        for x in range(4):
            piece = board[y][x]
            if piece[0] == 'K':
                if piece[1] == '0' and turn:
                    if x == 3:
                        stay_win[0] += 1
                    else:
                        stay_win[0] = 0
                elif piece[1] == '1'and not turn:
                    if x == 0:
                        stay_win[1] += 1
                    else:
                        stay_win[1] = 0
    if catch[0].count('K') > 0 or stay_win[0] == 2:
        print("┌───────────────────┐")
        print("│       승리!       │")
        print("└───────────────────┘")
        return True
    if catch[1].count('K') > 0 or stay_win[1] == 2:
        print("┌───────────────────┐")
        print("│       패배.       │")
        print("└───────────────────┘")
        return True
    return False

def findXY(board, new_xy, type_, turn):
    temp_xy = []
    for y in range(3):
        for x in range(4):
            if board[y][x] == f'{type_}{turn}':
                if isCanGo(board, new_xy, (x + 1, y + 1), type_, 0):
                    temp_xy.append(((x + 1), (y + 1)))
    # print(temp_xy)
    return temp_xy

def setPiece(board, new_xy, type_, turn):
    board[new_xy[1] - 1][new_xy[0] - 1] = f'{type_}{turn}'
    return board

def move(board, catch, old_xy, new_xy, type_ = '-', turn = '-'):
    if isCanGo(board, new_xy, old_xy, type_, turn):
        if not isEmpty(board, new_xy):
            if getBoardNow(board, new_xy)[0] == 'H':
                catch[turn].append('Z')
            else:   
                catch[turn].append(getBoardNow(board, new_xy)[0])
        if type_ == 'Z' and new_xy[0] == 4 - turn:
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

def Ai_(board, catch, depth):
    return Ai.Aing(board, catch, depth)

def input_command(board, catch):
    isMove = True
    while 1:
        print("수를 입력하세요...")
        command = input()
        arr = [i for i in command]
        if not (arr[0] in db.type_dic):
            print("존재하지 않는 말입니다.")
            continue
        if not (arr[1] in db.y_axis):
            print("y축 좌표가 잘못되었습니다.")
            continue
        if not (0 < int(arr[2]) < 5):
            print("x축 좌표가 잘못되었습니다.")
            continue
        com_xy = (int(arr[2]), db.y_axis[arr[1]])
        type_ = arr[0]
        if getBoardNow(board, com_xy)[1] == '0':
            continue
        if len(arr) == 3:
            temp_xy = findXY(board, com_xy, type_, 0)
            count = len(temp_xy)
            if  count == 1:
                old_xy = temp_xy[0]
                if isCanGo(board, com_xy, old_xy, type_, 0) :
                    break
                else:
                    print("움직일 수 없습니다.")
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
                if isCanGo(board, com_xy, old_xy, type_, 0) :
                    break
                else:
                    print("움직일 수 없습니다.")
        elif len(arr) == 4:
            if arr[-1] == "!" and isCatch(catch, type_, 0) and isEmpty(board, com_xy) and com_xy[0] < 4:
                isMove = False
                old_xy = (0, 0)
                break
        else:
            print("길이가 맞지 않는 입력입니다.")
    return old_xy, com_xy, type_, isMove

if __name__ == '__main__':
    print_(board, catch)
    while 1:
        old_xy, com_xy, type_, isMove  = input_command(board, catch)
        # print(old_xy, com_xy, type_, isMove)
        board, catch = Player(board, catch, old_xy, com_xy, type_, isMove)
        if isWin(board, catch, 0):
            continue
        print_(board, catch)
        board, catch = Ai_(board, catch, 3)
        print_(board, catch)
        if isWin(board, catch, 1):
            continue
