# -*- coding: utf-8 -*-
import numpy as np

def boost(data,n):
    w = np.zeros(n)
    w.shape = (fiture_num,1)
    while True:
        w_last = w
        for i in data:
            if(float(np.dot(i,w))>0):
                continue
            else:
                temp = i
                temp.shape = (fiture_num,1)
                w = w+temp
        if (w_last== w).all():
            print "最终的参数为："
            w.shape = (1,fiture_num)
            print w[0]
            break
if __name__ == '__main__':
    list1 = [[0,0,0],[1,0,0],[1,0,1],[1,1,0]]
    # list1 = [[0,0],[0,1]]
    for i in list1:
        i.append(1)
    list2 = [[0,0,1],[0,1,1],[0,1,0],[1,1,1]]
    # list2 = [[1,0],[1,1]]
    for i in list2:
        for j in range(len(i)):
            i[j] = -i[j];
        i.append(-1)
    data = np.array(list1+list2)
    fiture_num = len(list1[0])
    boost(data,fiture_num)