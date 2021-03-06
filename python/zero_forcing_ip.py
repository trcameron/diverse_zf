# Zero Forcing IP
from sys import stdin
from cplex import Cplex
from networkx import Graph, draw
from matplotlib import pyplot as plt
from nauty_geng_reader import graph6
from numpy import array, concatenate, ones, sum, zeros

###############################################
###         zero forcing standard rule      ###
###############################################
def zf_std(a):
    # number of vertices
    n,_ = a.shape
    # Edge set
    edges = []
    m = 0 # number of edges
    for i in range(n):
        for j in range(n):
            if(a[i,j]==1):
                edges.append((i,j))
                m += 1
    # objective function
    T = n-1 # maximal propogation time
    obj = concatenate((ones(n),zeros(n),zeros(m)))
    # lower and upper bounds
    lb = concatenate((zeros(n),zeros(n),zeros(m)))
    ub = concatenate((ones(n),T*ones(n),ones(m)))
    # constraints
    count = 0; sense = ""
    rows = []; cols = []; vals = []; rhs = []
    # constraint 1
    for v in range(n):
        # s_{v}
        rows.append(count)
        cols.append(v)
        vals.append(1)
        for k in range(m):
            if(edges[k][1]==v):
                # y_{e}, where e = (u,v)
                rows.append(count)
                cols.append(2*n+k)
                vals.append(1)
        # = 1
        rhs.append(1)
        sense += "E"
        count += 1
    # constraint 2
    for k in range(m):
        # x_{u} - x_{v} + (T+1)y_{e}, where e = (u,v)
        rows.extend([count,count,count])
        cols.extend([n+edges[k][0],n+edges[k][1],2*n+k])
        vals.extend([1,-1,T+1])
        # <= T
        rhs.append(T)
        sense  += "L"
        count += 1
    # constraint 3
    for k in range(m):
        for w in range(n):
            if(w!=edges[k][1] and a[edges[k][0],w]==1):
                # x_{w} - x_{v} + (T+1)y_{e}, where e = (u,v) and w!=v, u~w
                rows.extend([count,count,count])
                cols.extend([n+w,n+edges[k][1],2*n+k])
                vals.extend([1,-1,T+1])
                # <= T
                rhs.append(T)
                sense += "L"
                count += 1
    # cplex problem variable
    prob = Cplex()
    # quiet results
    prob.set_results_stream(None)
    # maximiation problem
    prob.objective.set_sense(prob.objective.sense.minimize)
    # problem variables
    prob.variables.add(obj=obj, lb=lb, ub=ub)
    for j in range(prob.variables.get_num()):
        prob.variables.set_types(j,prob.variables.type.integer)
    # linear constraints
    prob.linear_constraints.add(rhs=rhs, senses=sense)
    prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
    # write lp file
    # prob.write("zero_forcing.lp")
    # alg method
    alg = prob.parameters.lpmethod.values
    prob.parameters.lpmethod.set(alg.auto)
    # solve problem
    prob.solve()
    # solution variables
    var = prob.solution.get_values()
    s = var[0:n]
    x = var[n:2*n]
    y = var[2*n:]
    opt = prob.solution.get_objective_value()
    # return
    return opt, s, x, y
###############################################
###             main                        ###
###############################################
def main():
    try:
        # read input stream
        for line in stdin:
            a = graph6(bytes(line.rstrip(),'utf-8'))
            opt,s,x,y = zf_std(a)
            
            print(x)
            
            g = Graph(a)
            color_map = []
            for i in range(len(s)):
                if(s[i]==1):
                    color_map.append('#0000FF')
                else:
                    color_map.append('#C0C0C0')
            draw(g,with_labels=True,node_color=color_map,ax=plt.subplot(111))
            plt.show()
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()
