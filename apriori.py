# -*- coding: UTF-8 -*-

def apriori(T,minsup):
	item = {}
	for t in T:
		for i in t:
			if i in item:
				item[i] += 1
			else:
				item[i] = 1
	citems = []
	for i in item.keys():
		citems.append([i])
	fitems = []
	all_count_items = []
	citems.sort()
	for key in citems:
		if item[key[0]]>=minsup:
			fitems.append(key)
			all_count_items.append(item[key[0]])
	

	all_fitems = fitems
	while fitems !=[]:
		citems = c_gen(fitems)
		count_items = get_count(T,citems)
		fitems = get_fitems(citems,count_items,minsup,T,all_count_items)
		for key in fitems:
			all_fitems.append(key)


	return all_fitems,all_count_items

def get_fitems(citems,count_items,minsup,T,all_count_items):
	'''
	从citems中找出来高于minsup的元素，然后返回
	'''
	temp = []
	for i in range(len(citems)):
		if count_items[i]>minsup:
			temp.append(citems[i])
			all_count_items.append(count_items[i])

	return temp




def get_count(T,citems):
	'''
	判断T中citems每个元素出现的次数，并返回频数数组
	'''
	count = []
	for key in citems:
		c = 0
		for t in T:
			flag = True;
			for i in key:
				if i not in t:
					flag = False
			if flag:
				c +=1
		count.append(c)
	return count

def c_gen(fitems):
	'''
	从fitems中生成下一个集合的citems，
	'''
	temp=[]
	for i in fitems:
		for j in fitems:
			key = []
			if(i !=j and i[:-1]==j[:-1]):
				key = i[:-1]
				key.append(i[-1])
				key.append(j[-1])
				key.sort()
			if key not in temp and key !=[]:
				temp.append(key)
	return temp

T = [['1','3','4'],['2','3','5'],['1','2','3','5'],['2','5']]
minsup = len(T)*0.3
F = apriori(T, minsup)
print F
