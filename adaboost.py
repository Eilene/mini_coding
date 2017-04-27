#coding:utf-8
import numpy as np
import random
import math

'''
读取testSet中的数据8:2构造训练样本和测试样本
'''
trainX = []
trainY = []
testX = []
testY = []
f = open("testSet.txt")
test = f.read()
test = test[:-1].split("\n")
length = len(test)

for i in test[0:int(length*0.8)]:
	i = i[:-1].split("	")
	for j in range(len(i)-1):
		i[j] = float(i[j])
	trainX.append(i[0:-1])
	trainY.append(int(i[-1]))

for i in test[int(length*0.8):]:
	i = i[:-1].split("	")
	for j in range(len(i)-1):
		i[j] = float(i[j])
	testX.append(i[0:-1])
	testY.append(int(i[-1]))


trainX = np.array(trainX)
trainY = np.array(trainY)


T = 10   #训练十个弱分类器
'''
LR分类器
'''
alpha = 0.001
maxiter = 1000

def sigmod(thetaX):
	return 1.0/(1+math.exp(-thetaX))

def lr(trainX,trainY,feature_num,data_weight):

	sample_num = trainX.shape[0]
	w = np.ones((feature_num, 1)) 

	for k in range(maxiter):
		for i in range(sample_num):
			result = sigmod(np.dot(trainX[i],w)[0])
			error = trainY[i]-result
			w = w + alpha*trainX[i]*error
			#w = w + alpha*trainX[i]*error*data_weight[i]

	return w


'''
初始化基本参数
'''
posnum = list(trainY).count(1)#计算正样本的个数

n,feature_num = trainX.shape#样本数和特征数
feature_num = feature_num+1#有一个常数项
b = [1]*(n)

trainX = np.c_[trainX,b]#连接常数项

'''
初始化每个数据权重，1/2m,1/2l
'''
w = [0]*n#初始化每个数据的权重
pos_w = 1.0/(2*posnum)
neg_w = 1.0/(2*(n-posnum))

for i in range(n):
	if(trainY[i]==1):
		w[i] = pos_w
	else:
		w[i] = neg_w

'''
adaboost开始训练
'''

best_alpha = []#每一轮最好的特征的权重，由错误率计算
best_theta = []#每一轮最好的分类器的参数，用于预测
best_feature = []#每一轮最好的特征

sum_w = 0.0   #用于归一化权重
for i in range(T):#迭代的轮数
	sum_w = sum(i for i in w)
	for i in range(len(w)):
		w[i] = w[i]/sum_w   #归一化权重
	
	'''
	初始化参数用于找出当前轮最好的特征
	'''
	min_error = 10000 #用于记录找到误差最小的特征
	min_theta = 0.0 #用于保留最好的特征对应分类器的参数
	min_train = [] #用于保留最好的分类器对应得训练数据
	min_j = 0#用于保留最好的分类器对应特征

	for j in range(feature_num-1):
		#对每一个特征训练一个分类器
		train = trainX[:,j]#取出所有样本第j个特征值
		theta = lr(train,trainY,1,w)

		temp = 0.0#计算每个特征作为分类器的误差
		for k in range(n):
			temp += w[k]*abs(sigmod(np.dot(train[k],theta)[0])-trainY[k])

		if(temp<min_error):
			min_error = temp
			min_theta = theta
			min_train = train
			min_j = j

	beta = min_error/(1-min_error)#更新beta

	'''
	保留当前轮最好的参数及错误率,用于数据预测
	'''
	best_alpha.append(math.log(1/beta))
	best_theta.append(min_theta)
	best_feature.append(min_j)

	'''
	更新下一轮数据的权重
	'''
	for m in range(n):#更新权重
		result = sigmod(np.dot(min_train[m],min_theta)[0])
		if((trainY[m]==1 and result>=0.5) or(trainY[m]==-1 and result<0.5)):#分类正确
			w[m] = w[m]*beta#权重变小
			#否则权重不变

print "使用lr分类器，样本特征数为2，另外加上常数项，分类器参数为三维，共训练10轮"
print "各分类器权重参数为："
print best_alpha
print "各分类器分类参数为："
print best_theta

def predict(x):
	sum1 = 0
	sum2 = 0
	for i in range(len(best_alpha)):
		sum1 = sum1 + best_alpha[i]*sigmod(np.dot(x[best_feature[i]],best_theta[i])[0])
		sum2 = sum2 + best_alpha[i]
	if(sum1*2 >= sum2):
		return 1
	else:
		return -1


count = 0
for i in range(len(testX)):
	result = predict(testX[i])
	if(result == testY[i]):
		count += 1

print "准确率为"+str(float(count)/len(testX))

