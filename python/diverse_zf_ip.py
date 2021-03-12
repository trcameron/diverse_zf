# Jakob Loedding
# Zero Forcing Diameter IP
from sys import stdin
from cplex import Cplex
from networkx import Graph, draw
from matplotlib import pyplot as plt
from nauty_geng_reader import graph6
from numpy import array, concatenate, ones, sum, zeros
from zero_forcing_ip import zf_std



###############################################
###           zero forcing diameter         ###
###############################################
def ZFD(a,s):
    n,_ = a.shape # number of vertices
    edges = [] # set of edges
    m = 0 # number of edges

    # populate edge set
    for i in range(n):
     for j in range(n):
         if(a[i,j] == 1):
             edges.append((i,j))
             m+=1

    # objective function -> (s, s', x, x', y, y', z)
    obj = concatenate((zeros(n), zeros(n), zeros(n), zeros(n), zeros(m), zeros(m), ones(n)))
    
    T = n - 1 # max propogation time

    # lower/upper bounds
    lb = concatenate((zeros(n),zeros(n),zeros(n), zeros(n), zeros(m), zeros(m), zeros(n))) 
    ub = concatenate((ones(n), ones(n), T*ones(n), T*ones(n), ones(m), ones(m), ones(n)))

    # initialize data for model setup
    count = 0; sense = ""; rows = []; cols = []; vals = []; rhs = []

    # constraint 1
    for v in range(n):
        # s_v
        rows.append(count)
        cols.append(v) 
        vals.append(1)
        for k in range(m):
            # y_e with e = (u,v)
            rows.append(count)
            cols.append(3*n + k)
            vals.append(1)

        rhs.append(1)
        sense += "E"
        count += 1

    # constraint 2
    for v in range(n):
        # s_v'
        rows.append(count) 
        cols.append(n + v) 
        vals.append(1) 
        for k in range(m):
            # y_e' with e = (u,v)
            rows.append(count)
            cols.append(4*n + m + k) # n+n+n+n+m+k
            vals.append(1)

        rhs.append(1)
        sense += "E"
        count += 1

    # constraint 3
    for k in range(m):
        # x_u - x_v + (T+1)y_e with e = (u,v)
        rows.extend([count, count, count])
        cols.extend([2*n + edges[k][0], 2*n + edges[k][1], 4*n + k])
        vals.extend([1, -1, T + 1])
        rhs.append(T) # <= T
        sense  += "L"
        count += 1

    # constraint 4
    for k in range(m):
        # x_u' - x_v' + (T+1)y_e' with e = (u,v)
        rows.extend([count, count, count])
        cols.extend([3*n + edges[k][0], 3*n + edges[k][1], 4*n + m + k])
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
                cols.extend([2*n + w, 2*n + edges[k][1], 4*n + k])
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
                cols.extend([3*n + w, 3*n + edges[k][1], 4*n + m + k])
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
        cols.append(n + v) 
        vals.append(1) 

    rhs.append(s)
    sense += "E"
    count += 1

    # constraint 9
    for v in range(n):
        #s_v + s_v' - z_v <= 1
        rows.extend([count, count, count])
        cols.extend([v, n + v, 4*n + 2*m + v])
        vals.extend([1, 1, -1])
        rhs.append(1)
        sense  += "L"
        count += 1


    IP = Cplex() # integer program/cplex problem
    IP.set_results_stream(None)
    
    IP.objective.set_sense(IP.objective.sense.minimize) # minimization problem
    
    # variables
    IP.variables.add(obj = obj, lb = lb, ub = ub)
    for j in range(IP.variables.get_num()):
        IP.variables.set_types(j,IP.variables.type.integer)
        
    # linear constraints
    IP.linear_constraints.add(rhs = rhs, senses = sense)
    IP.linear_constraints.set_coefficients(zip(rows, cols, vals))

    # write lp file
    # IP.write("diverse_zf_ip.lp")
    
    # alg method
    alg = IP.parameters.lpmethod.values
    IP.parameters.lpmethod.set(alg.auto)
    
    # solve integer program
    IP.solve()
    
    # solution variables
    var = IP.solution.get_values()

    # solutions for each variable
    s1 = var[0:n] # s
    s2 = var[n:2*n] # s'
    x1 = var[2*n:3*n] # x
    x2 = var[3*n:4*n] # x'
    y1 = var[4*n:4*n + m] # y
    y2 = var[4*n + m:4*n + 2*m] # y'
    z = var[4*n + 2*m:5*n + 2*m] # z

    # optimal solution
    optSol = IP.solution.get_objective_value()
    
    return opt, s1, s2, x1, x2, y1, y2

    
###############################################
###             main                        ###
###############################################
def main():
    #try:
        # read input stream
        #for line in stdin:
    # path graph
    a = array([[0,1,0,0,0],[1,0,1,0,0], [0,1,0,1,0], [0,0,1,0,1],[0,0,0,1,0]])
    opt = zf_std(a)
    ZFD(a,opt[0])
            
    #except Exception as e:
     #   print(e)
        
if __name__ == '__main__':
    main()
