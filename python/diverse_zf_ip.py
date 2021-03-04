# Jakob Loedding
# Diverse Zero Forcing IP
from sys import stdin
from cplex import Cplex
from networkx import Graph, draw
from matplotlib import pyplot as plt
from nauty_geng_reader import graph6
from numpy import array, concatenate, ones, sum, zeros
from zero_forcing_ip import zf_std



###############################################
###           diverse zero forcing          ###
###############################################
def dv_zf(a,s):
    n,_ = a.shape # number of vertices
    edges = [] # set of edges
    m = 0 # number of edges

    # populate edge set
    for i in range(n):
     for j in range(n):
         if(a[i,j] == 1):
             edges.append((i,j))
             m+=1

    # objective function
    # minimize sum(z_v) for all v in V
    
    T = n - 1 # max propogation time
    lb = concatenate((zeros(n),zeros(n),zeros(m))) # lower bounds 
    ub = concatenate((ones(n),T*ones(n),ones(m))) # upper bounds

    # initialize data for model setup
    count = 0; sense = ""; rows = []; cols = []; vals = []; rhs = []

    # constraint 1
    for v in range(n):
        # s_v
        rows.append(count) # row indices
        cols.append(v) # colum indices
        vals.append(1) # coefficents
        for k in range(m):
            # y_e with e = (u,v)
            rows.append(count)
            cols.append(2 * n + k)
            vals.append(1)

        rhs.append(1)
        sense += "E"
        count += 1

    # constraint 2
    for v in range(n):
        # s_v'
        rows.append(count) # row indices
        cols.append(v) # colum indices
        vals.append(1) # coefficents
        for k in range(m):
            # y_e' with e = (u,v)
            rows.append(count)
            cols.append(2 * n + k)
            vals.append(1)

        rhs.append(1)
        sense += "E"
        count += 1

    # constraint 3
    for k in range(m):
        # x_u - x_v + (T+1)y_e with e = (u,v)
        rows.extend([count, count, count])
        cols.extend([n + edges[k][0], n + edges[k][1], 2 * n + k])
        vals.extend([1, -1, T + 1])
        rhs.append(T) # <= T
        sense  += "L"
        count += 1

    # constraint 4
    for k in range(m):
        # x_u' - x_v' + (T+1)y_e' with e = (u,v)
        rows.extend([count, count, count])
        cols.extend([n + edges[k][0], n + edges[k][1], 2 * n + k])
        vals.extend([1, -1, T + 1])
        rhs.append(T) # <= T
        sense  += "L"
        count += 1

    # constraint 5
    for k in range(m):
        for w in range(n):
            if(w != edges[k][1] and a[edges[k][0],w] == 1):
                # x_w - x_v + (T+1)y_e, where e = (u,v) and w!=v, u~w
                rows.extend([count, count, count])
                cols.extend([n + w, n + edges[k][1], 2 * n + k])
                vals.extend([1, -1, T + 1])
                rhs.append(T) #<= T
                sense += "L"
                count += 1

    # constraint 6
    for k in range(m):
        for w in range(n):
            if(w != edges[k][1] and a[edges[k][0],w] == 1):
                # x_w' - x_v' + (T+1)y_e', where e = (u,v) and w!=v, u~w
                rows.extend([count, count, count])
                cols.extend([n + w, n + edges[k][1], 2 * n + k])
                vals.extend([1, -1, T + 1])
                rhs.append(T) # <= T
                sense += "L"
                count += 1

    # constraint 7
    for v in range(n):
        # s_v
        rows.append(count)
        cols.append(v) 
        vals.append(1) 

    rhs.append(s)
    sense += "E"
    count += 1

    # comtraint 8
    for v in range(n):
        # s_v'
        rows.append(count)
        cols.append(v) 
        vals.append(1) 

    rhs.append(s)
    sense += "E"
    count += 1

    # constraint 9
    #s_v + s_v' - z_v <= 1
        
    
###############################################
###             main                        ###
###############################################
def main():
    #try:
        # read input stream
        #for line in stdin:
            # path graph
    a = [[0,1,0,0,0],[1,0,1,0,0], [0,1,0,1,0], [0,0,1,0,1],[0,0,0,1,0]]
    opt = zf_std(a)
    opt
    dv_zf(a,opt[0])
            
    #except Exception as e:
     #   print(e)
        
if __name__ == '__main__':
    main()
