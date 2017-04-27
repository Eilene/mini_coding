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

'''
初始化参数
'''
n,feature_num = trainX.shape
feature_num = feature_num+1#有一个常数项
b = [1]*(n)
n1 = n/3

trainX = np.c_[trainX,b]#所有训练样本加一个常数项

'''
LR分类器
'''
alpha = 0.001#步长
maxiter = 1000

def sigmod(thetaX):
	return 1.0/(1+math.exp(-thetaX))

def lr(trainX,trainY,feature_num):

	sample_num = trainX.shape[0]
	w = np.ones((feature_num, 1)) # init w

	for k in range(maxiter):
		for i in range(sample_num):
			result = sigmod(np.dot(trainX[i,:],w)[0])
			error = trainY[i]-result
			temp = trainX[i,:]
			temp.shape = (feature_num,1)
			w = w + alpha*temp*error

	return w

'''
三个分类器训练
'''
#训练第一个弱分类器
randomnum = np.array(random.sample(range(n),n1))#从n里面随机选n1个
remnent = set(range(n))-set(randomnum)#剩余样本

trainC1X = []
trainC1Y = []
for i in randomnum:
	trainC1X.append(trainX[i,:])
	trainC1Y.append(trainY[i])

trainC1X = np.array(trainC1X)
wc1 = lr(trainC1X,trainC1Y,feature_num)

#训练第二个分类器
right = []#记录被c1分类正确的样本
trainC2X = []
trainC2Y = []

count = 0
while(count <= n1):#保证c2分类器也接受1/3的样本
	count += 1
	value = random.sample(range(2),1)#模拟抛硬币

	if(value==0):#正面
		for i in remnent:
			remnent.remove(i)#选择一个剩余样本点并删除
			result = sigmod(np.dot(trainX[i,:],wc1)[0])#利用c1分类
			if((trainY[i]==1 and result>=0.5) or(trainY[i]==-1 and result<0.5)):#分类正确
				right.append(i)
			else:#错误则加入第二个分类器的训练样本
				trainC2X.append(trainX[i,:])
				trainC2Y.append(trainY[i])
				break
	else:#反面，选择一个c1正确分类的加入
		if(len(right)>0):
			trainC2X.append(trainX[right[-1],:])
			trainC2Y.append(trainY[right[-1]])
			right = right[:-1]
		else:
			for i in randomnum:#从n1里面选择
				result = sigmod(np.dot(trainX[i,:],wc1)[0])
				if((trainY[i]==1 and result>=0.5) or(trainY[i]==-1 and result<0.5)):
					if(i+1<len(randomnum)):
						randomnum = randomnum[i+1:]#把选过的删掉
					trainC2X.append(trainX[i,:])#加入c2的训练集
					trainC2Y.append(trainY[i])
					break


trainC2X = np.array(trainC2X)
wc2 = lr(trainC2X,trainC2Y,feature_num)


#训练第三个分类器
trainC3X = []
trainC3Y = []

for i in remnent:
	result1 = sigmod(np.dot(trainX[i,:],wc1)[0])
	result2 = sigmod(np.dot(trainX[i,:],wc2)[0])
	if((result2>=0.5 and result1<0.5) or(result2<0.5 and result1>=0.5)):#两个分类器结果不同
		trainC3X.append(trainX[i,:])
		trainC3Y.append(trainY[i])

trainC3X = np.array(trainC3X)
wc3 = lr(trainC3X,trainC3Y,feature_num)

print "使用lr分类器，样本特征数为2，另外加上常数项，分类器参数为三维"
print "第一个分类器参数:"
print wc1
print "第二个分类器参数:"
print wc2
print "第三个分类器参数:"
print wc3

'''
上面部分完成三个分类器的训练，结果存在wc1,wc2,wc3中，对一条新的预测样本，先接上常数项1
然后用三个分类器预测做投票
'''
def predict(x):
	x.append(1)
	result1 = sigmod(np.dot(x,wc1)[0])
	result2 = sigmod(np.dot(x,wc2)[0])
	result3 = sigmod(np.dot(x,wc3)[0])
	if(result1>=0.5 and result>=0.5):
		return 1
	elif(result1<0.5 and result2<0.5):
		return -1
	elif(result3>=0.5):
		return 1
	else:
		return -1

count = 0
for i in range(len(testX)):
	result = predict(testX[i])
	if(result == testY[i]):
		count += 1

print "共预测"+str(len(testX))+"个样本，其中正确"+str(count)+"个，准确率为"+str(float(count)/len(testX))
