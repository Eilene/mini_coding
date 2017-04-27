#coding:utf-8
class Solution(object):
    def decodeString(self, s):
        """
        :type s: str
        :rtype: str
        """
        s_num = []
        s_str = []
        num_temp = 0
        t = ''
        for i in s:
            if (i > '0' and i <'9'):
                num_temp = num_temp*10 +int(i)
            elif(i=='['):
                s_num.append(num_temp)
                num_temp = 0
                s_str.append(t)
                t = ''
            elif(i==']'):
                k = s_num[-1]
                s_num.pop()
                for j in range(k):
                    s_str[-1] += t
                t = s_str[-1]
                s_str.pop()
            else:
                t += i
        print t
        return t
test = Solution()
test.decodeString('3[a2[c]]')
