import numpy as np

type_dic = {'K' : 0, 'S' : 1, 'J' : 2, 'Z' : 3, 'H' : 4}
piece_go = np.loadtxt('piece_go.csv', bool, delimiter=',')
y_axis = {'a' : 1, 'b' : 2, 'c' : 3, 1 : 'a', 2 : 'b', 3 : 'c'}