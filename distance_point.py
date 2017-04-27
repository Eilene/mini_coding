# -*- coding:utf-8 -*-
import sys
import math
class distance_point:
    def __init__(self,point):
        self.point_set = point
        pass
    def distance(self,nodea,nodeb):
        distance = math.sqrt((nodea[0]-nodeb[0])*(nodea[0]-nodeb[0])+(nodea[1]-nodeb[1])*(nodea[1]-nodeb[1]))
        return distance
    def min_distance(self,left,right):
        if(left+1==right):
            return self.distance(self.point_set[left],self.point_set[right])
        if(left+2==right):
            d1 = self.distance(self.point_set[left],self.point_set[left+1])
            d2 = self.distance(self.point_set[left], self.point_set[right])
            d3 = self.distance(self.point_set[right], self.point_set[left + 1])
            small_distance = min(d1,min(d2,d3))
            return small_distance
        mid = (left+right)/2
        result = min(self.min_distance(left,mid),self.min_distance(mid+1,right))
        lr_point = []
        for i in range(left,right+1):
            if (self.point_set[i]<=self.point_set[mid]+result) and (self.point_set[i]>=self.point_set[mid]-result):
                lr_point.append(self.point_set[i])
        lr_point.sort(key = lambda l:(l[1]))
        for i in range(0,len(lr_point)):
            mini = min(i+11,len(lr_point))
            for j in range(i,mini):
                if self.point_set[j][1]-self.point_set[i][1]>=result:
                    break
                result = min(result,self.distance(self.point_set[i],self.point_set[j]))
        return result

if __name__ == "__main__":
    input_point = raw_input("请输入点，按照xy的顺序，以空格分开")
    input_point = input_point.split(" ")
    point = []
    i = 0
    j = 1
    while j < len(input_point):
        point.append([int(input_point[i]),int(input_point[j])])
        i += 2
        j += 2
    print point.sort(key=lambda l:(l[0]))
    test = distance_point(point)
    print test.min_distance(0,len(point)-1)
