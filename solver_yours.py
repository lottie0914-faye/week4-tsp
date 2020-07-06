import math
import random
import sys
import copy
import time
from common import print_solution, read_input

#simulated annealing

#starting temperature finishing temperature
T0 = 80
Tend = 1e-5
#attenuation coefficient
a = 0.985


def init_dis_matrix(length):
    distance_matrix = [[0 for col in range(length)] for raw in range(length)]
    return distance_matrix
    
    
def load_position(cities):
    city_x = []
    city_y = []
    for i in range(len(cities)):
        city_x.append(cities[i][0])
        city_y.append(cities[i][1])
    return city_x,city_y
#create the initial reference matrix
def getdistance(city_x,city_y,n_len,distance):
    for i in range(n_len):
        for j in range(n_len):
            x = pow(city_x[i] - city_x[j], 2)
            y = pow(city_y[i] - city_y[j], 2)
            distance[i][j] = pow(x + y, 0.5)
    for i in range(n_len):
        for j in range(n_len):
            if distance[i][j] == 0:
                distance[i][j] = sys.maxsize

#calculate the distence
def cacl_best(rou,n_len,distence):
    sumdis = 0.0
    for i in range(n_len-1):
        sumdis += distence[rou[i]][rou[i+1]]
    sumdis += distence[rou[n_len-1]][rou[0]]     
    return sumdis

#get the new route
def getnewroute(route, time,n_len):
    
    current = copy.copy(route)
    #even
    if time % 2 == 0:
        u = random.randint(0, n_len-1)
        v = random.randint(0, n_len-1)
        temp = current[u]
        current[u] = current[v]
        current[v] = temp
    #odd 
    else:
        temp2 = random.sample(range(0, n_len), 3)
        temp2.sort()
        u = temp2[0]
        v = temp2[1]
        w = temp2[2]
        w1 = w + 1
        temp3 = [0 for col in range(v - u + 1)]
        j =0
        for i in range(u, v + 1):
            temp3[j] = current[i]
            j += 1
        
        for i2 in range(v + 1, w + 1):
            current[i2 - (v-u+1)] = current[i2]
        w = w - (v-u+1)
        j = 0
        for i3 in range(w+1, w1):
            current[i3] = temp3[j]
            j += 1
    
    return current

import solver_greedy
def solve(cities):
    city_x,city_y = load_position(cities)
    n_len = len(city_x)
    city_x = [x*1000 for x in city_x]
    city_y = [x*1000 for x in city_y]
    distence = init_dis_matrix(n_len)
    #distance maxtrix
    getdistance(city_x,city_y,n_len,distence)
    #initial
    route = solver_greedy.solve(cities) 
    total_dis = cacl_best(route,n_len,distence)
    newroute = []
    new_total_dis = 0.0
    best = route
    best_total_dis = total_dis
    t = T0
    
    while True:
        if t <= Tend:
            break
        #set the initial temp
        for rt2 in range(600):
            newroute = getnewroute(route, rt2,n_len)
            new_total_dis = cacl_best(newroute,n_len,distence)
            delt = new_total_dis - total_dis
            if delt <= 0:
                route = newroute
                total_dis = new_total_dis
                if best_total_dis > new_total_dis:
                    best = newroute
                    best_total_dis = new_total_dis
            elif delt > 0:
                p = math.exp(-delt / t)
                ranp = random.uniform(0, 1)
                if ranp < p:
                    route = newroute
                    total_dis = new_total_dis
        t = t * a
    

    return best

    
if __name__=="__main__":
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    result = solve(cities)
    print_solution(result)