# -*- coding: utf-8 -*-
import numpy as np
import math
import sys
class byes:
	def __init__(self):
		self.data1 = np.array([[1,0,1],[0,0,0],[1,1,0],[1,0,0]])
		self.data2 = np.array([[0,0,1],[0,1,1],[1,1,1],[0,1,0]])
		self.character_num = len(self.data1[0])
		self.p1 = 0.5
		self.p2 = 0.5

	def get_m(self,data):
		list=np.zeros(self.character_num)
		for i in data:
			for j in range(0,self.character_num):
				list[j] = list[j]+i[j]
		list = (1.0/len(data))*list
		return list
	
	def get_c(self,data,m):
		c = np.zeros(shape=(self.character_num,self.character_num))
		x = np.zeros(shape=(self.character_num,self.character_num))
		for i in range(0,len(data)):
			temp = data[i]-m
			temp.shape = (self.character_num,1)
			temp2 = data[i]-m
			temp2.shape = (1,self.character_num)
			c = c + np.dot(temp,temp2)
		c = (1.0/len(data))*c
		return c

	def get_diff(self,c1,c2,m1,m2,p1,p2,inputx=np.array([0,0,1])):
		if(c1.all()==c2.all()):
			cn =  np.linalg.inv(c1)
			temp = math.log(p1,math.e)-math.log(p2,math.e)
			m1.shape = (1,self.character_num)
			m2.shape = (1,self.character_num)
			b = temp-0.5*float(np.dot(np.dot(m1,cn),m1.T))+0.5*float(np.dot(np.dot(m2,cn),m2.T))
			coe_matrix = np.dot((m1-m2),cn)
			coe_re = coe_matrix*inputx
			result = 0
			for i in coe_re[0]:
				result = result+i
			result = result+b
			if(result>0):
				return 1
			else:
				return 2
		else:
			cn1 = np.linalg.inv(c1)
			cn2 = np.linalg.inv(c2)
			d1 = math.log(p1,math.e)-0.5*math.log(np.linalg.det(c1),math.e)
			d2 = math.log(p2,math.e)-0.5*math.log(np.linalg.det(c2),math.e)
			temp = inputx-m1
			temp.shape = (1,self.character_num)
			d1 = d1-0.5*np.dot(np.dot(temp,cn1),temp.T)
			temp = inputx-m2
			temp.shape = (1,self.character_num)
			d2 = d2-0.5*np.dot(np.dot(temp,cn2),temp.T)
			if d1-d2>0:
				return 1
			else:
				return 2



if __name__ == '__main__':
	test = byes()
	test.m1 = test.get_m(test.data1)
	test.m2 = test.get_m(test.data2)
	test.c1 = test.get_c(test.data1,test.m1)
	test.c2 = test.get_c(test.data2,test.m2)
	inputx = raw_input("请输入x(属性值间用空格分割)： ")
	inputx = inputx.split(" ")
	for i in range(0,len(inputx)):
		inputx[i] = float(inputx[i])
	inputx = np.array(inputx)
	result = test.get_diff(test.c1,test.c2,test.m1,test.m2,test.p1,test.p2,inputx)
	print "所属类别："
	print str(result)

	

