from random import random,gauss,randint
import math
C = 10.0
arm_num = 9
arm_args = []
ALL_TIMES = 72

for i in range(arm_num):
    arm_args.append((random()*C,random()*C))

def try_arm_dive_times(all_times):
    bandit = 0.0
    for i in range(arm_num):
        arm_times = all_times / arm_num
        if i <all_times % arm_num:
            arm_times +=1
        a,b = arm_args[i]
        for j in range(arm_times):
            bandit += gauss(a,b)
    return bandit

def try_arm_once_and_run_best(all_times):
    bandit = 0.0
    best_pos = 0
    try_arrs = []
    all_times = all_times - arm_num
    for i in range(arm_num):
        try_arrs.append(gauss(arm_args[i][0],arm_args[i][1]))
    for i in range(arm_num):
        if try_arrs[i]>try_arrs[best_pos]:
            best_pos = i
    a,b = arm_args[best_pos]
    for i in range(all_times):
        bandit += gauss(a,b)
    return bandit

def e_greedy(all_times,e):
    bandit = 0.0
    arms_bandit = [0 for i in range(arm_num)]
    arms_count = [0 for i in range(arm_num)]
    for i in range(all_times):
        k = 0
        if random()<e:
            k = randint(0,arm_num-1)
        else:
            for j in range(arm_num):
                if arms_bandit[j] > arms_bandit[k]:
                    k = j
        v = gauss(arm_args[k][0],arm_args[k][1])
        bandit = bandit+v
        arms_bandit[k] = (arms_bandit[k]*arms_count[k]+v)/(arms_count[k]+1)
        arms_count[k] = arms_count[k]+1
    return bandit

def soft_max(all_times,r):
    bandit = 0.0
    arms_bandit = [0 for i in range(arm_num)]
    arms_count = [0 for i in range(arm_num)]
    probs = [0 for i in range(arm_num)]
    for i in range(all_times):
        prob_sum = 0.0
        for j in range(arm_num):
            probs[j] = math.pow(math.e,arms_bandit[j]/r)
            prob_sum += probs[j]
        k = 0
        sel_random = random() * prob_sum
        sel_sum = 0.0
        for j in range(arm_num):
            sel_sum += probs[j]
            if sel_sum > sel_random:
                k = j
                break
        v = gauss(arm_args[k][0],arm_args[k][1])
        bandit += v
        arms_bandit[k] = (arms_bandit[k]*arms_count[k]+v)/(arms_count[k]+1)
        arms_count[k] = arms_count[k]+1
    return bandit

def ucb1(all_times):
    bandit = 0.0
    arms_bandit = [0 for i in range(arm_num)]
    arms_count = [0 for i in range(arm_num)]
    for i in range(arm_num):
        v = gauss(arm_args[i][0],arm_args[i][1])
        arms_bandit[i] = v
        bandit += v
        arms_count[i] = 1
        all_times -=1
    for i in range(1,all_times+1):
        k = 0
        m = -100000000
        for j in range(arm_num):
            tmp_ucb = arms_bandit[j] + math.sqrt(2.0*math.log(i+arm_num)/arms_count[j])
            if tmp_ucb>m:
                k = j
                m = tmp_ucb
        v = gauss(arm_args[k][0],arm_args[k][1])
        bandit = bandit + v
        arms_bandit[k] = (arms_bandit[k]*arms_bandit[k]+v)/(arms_count[k]+1)
        arms_count[k] = arms_count[k]+1
    return bandit


print("try_arm_dive_times")
print(try_arm_dive_times(ALL_TIMES))
print("")

print("try_arm_once_and_run_best")
print(try_arm_once_and_run_best(ALL_TIMES))
print("")

print("e_greedy")
print(e_greedy(ALL_TIMES,0.15))
print("")

print("soft_max")
print(soft_max(ALL_TIMES,1.0))
print("")

print("ucb1")
print(ucb1(ALL_TIMES))
print("")






























