# -*- coding:utf-8 -*-
from numpy import *
import numpy as np
import math

def classcial_qr(data,n):
    temp2 = data.T.copy()
    R = np.identity(n)
    for i in range(n):
        for j in range(i):
            R[i][j] = temp2[j]*temp2[i].T
            temp2[i] -= temp2[j]*temp2[i].T*temp2[j]
        R[i][i] = sqrt(temp2[i]*temp2[i].T)
        temp2[i] = temp2[i] /sqrt(temp2[i]*temp2[i].T)
    print "Q矩阵"
    print temp2.T
    print "R矩阵"
    print R.T

def householder_reduction(data,n,rank):
    temp = data.copy()
    temp2 = data.copy()
    m = data.shape[0]
    q = np.identity(m)
    for i in range(n):
        u = temp[:,0].copy()
        u[0][0] = u[0][0]-sqrt(temp[:,0].T*temp[:,0])

        if((u==np.zeros(shape=(u.shape[0],1))).all()):
            break
        r_temp = np.identity(m-i)-float(2/(u.T*u))*(u*u.T)
        r = np.identity(m)
        r[i:, i:] = r_temp
        q = np.dot(r,q)
        temp2 = np.dot(r,temp2)
        temp = temp2[i+1:,i+1:]

    print "Q矩阵"
    print q.T
    print "R矩阵"
    if(m>n):
        print temp2[:rank,:]
    else:
        print temp2[:, :rank]

def givens_reduction(data,n,rank):
    m = data.shape[0]
    temp = data.copy()
    q = np.identity(m, float)
    for i in range(0,n):
        for j in range(i+1,m):
            c = float(temp[:,i][i])/sqrt(temp[:,i][i]*temp[:,i][i]+temp[:,i][j]*temp[:,i][j])
            s = float(temp[:,i][j])/sqrt(temp[:,i][i]*temp[:,i][i]+temp[:,i][j]*temp[:,i][j])
            p = np.identity(m, float)
            p[i][i] = c
            p[i][j] = s
            p[j][i] = -s
            p[j][j] = c
            q = np.dot(p,q)
            temp = p*temp
    print "Q矩阵"
    print q.T
    print "R矩阵"
    if (m > n):
        print temp[:rank, :]
    else:
        print temp[:, :rank]

class lu_fenjie:
    def __init__(self, input_matrix, weidu):
        self.a_matrix = input_matrix
        self.l_matrix = np.eye(weidu)
        self.p_matrix = np.zeros((weidu, weidu))
        self.n = weidu
        self.p = [i for i in range(1, self.n + 1)]
        self.move = []
        pass

    def get_max(self, row, colum):
        # 从第row行开始找第column列的最大元素
        maxnum = -10000
        maxi = 0
        for i in range(row, self.n):
            if math.fabs(self.a_matrix[i][colum]) > maxnum:
                maxnum = self.a_matrix[i][colum]
                maxi = i
        return maxi

    def gauss(self):
        count = 0
        for i in range(0, self.n):
            # 从第count行开始找第i列最大的元素,返回的是矩阵的实际行数
            maxi = self.get_max(count, i)
            # 两行交换
            if (maxi != count):
                self.p[maxi] = self.p[maxi] ^ self.p[count]
                self.p[count] = self.p[maxi] ^ self.p[count]
                self.p[maxi] = self.p[maxi] ^ self.p[count]
                temp = self.a_matrix[maxi].copy()
                self.a_matrix[maxi] = self.a_matrix[count]
                self.a_matrix[count] = temp
                for re in self.move:
                    if (re[2] == maxi):
                        re[2] = count
                    elif (re[2] == count):
                        re[2] = maxi
            for j in range(count + 1, self.n):
                # 从第count+1行向下清除元素
                if (self.a_matrix[j][count] == 0):
                    continue
                div = self.a_matrix[j][count] / self.a_matrix[count][count]
                self.a_matrix[j] = self.a_matrix[j] - div * self.a_matrix[count]
                self.move.append([div, count, j])
                # j = j-div*count,
            # print self.l_matrix
            count = count + 1
        for i in self.move:
            self.l_matrix[i[2]][i[1]] = i[0]
        row_num = 0
        for i in self.p:
            self.p_matrix[row_num][i - 1] = 1
            row_num = row_num + 1
        print "P矩阵为："
        print self.p_matrix

        print "U矩阵为："
        print self.a_matrix

        print "L矩阵为："
        print self.l_matrix
        # 即为U矩阵


if __name__ == "__main__":
    weidu = int(raw_input("请输入矩阵的行数： "))
    lieshu = int(raw_input("请输入矩阵的列数： "))
    # print weidu
    a_matrix = np.arange(weidu * lieshu).reshape(weidu, lieshu)
    a_matrix.dtype = float
    input_matrix = raw_input("请按行输入矩阵元素(每个元素用空格分割)")
    input_matrix = input_matrix.split(" ")

    count = 0
    for i in range(0, weidu):
        for j in range(0, lieshu):
            a_matrix[i][j] = input_matrix[count]
            count = count + 1
    print "输入的矩阵为:"
    print a_matrix

    rank = np.linalg.matrix_rank(a_matrix)
    n = a_matrix.shape[1]
    old_martix = a_matrix.copy()
    a_matrix = mat(a_matrix)
    model = int(raw_input("请输入操作模式：1:LU分解 2:QR分解 3:Household约减 4:Givens约减 5:退出"))
    while(model!=5):
        if(model == 1):
            if (len(input_matrix) != weidu * weidu):
                print "输入矩阵元素个数不符合维度要求"
            else:

                a_det = np.linalg.det(old_martix)
                if (a_det == 0):
                    print "输入矩阵是奇异矩阵，无法LU分解"
                else:
                    test = lu_fenjie(old_martix, weidu)
                    test.gauss()



        elif(model == 2):

            classcial_qr(a_matrix, n)
        elif(model == 3):
            householder_reduction(a_matrix, n, rank)
        elif(model == 4):
            givens_reduction(a_matrix, n, rank)
        else:
            print "不存在该操作模式"
        model = int(raw_input("请输入操作模式：1:LU分解 2:QR分解 3:Household约减 4:Givens约减 5:退出"))
        if(model == 5):
            break