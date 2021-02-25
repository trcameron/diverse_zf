# cplex example
from cplex import Cplex
from numpy import array, zeros

###############################################
###             linear program             ##
###############################################
def lp(a,b,c):
    # number of equations (m) and unknowns (n)
    m,n = a.shape
    # objective function and lower bounds
    obj = c.copy()
    lb = zeros(n)
    # constraints
    count = 0; sense = ""
    rows = []; cols = []; vals = []; rhs = []
    for i in range(m):
        rows.extend([count for k in range(n)])
        cols.extend([k for k in range(n)])
        vals.extend(a[i,:])
        rhs.append(b[i])
        sense += "L"
        count += 1
    # cplex problem variable
    prob = Cplex()
    # quiet results
    #prob.set_results_stream(None)
    # maximiation problem
    prob.objective.set_sense(prob.objective.sense.maximize)
    # problem variables
    prob.variables.add(obj=obj, lb=lb)
    #for j in range(prob.variables.get_num()):
    #    prob.variables.set_types(j,prob.variables.type.integer)
    # linear constraints
    prob.linear_constraints.add(rhs=rhs, senses=sense)
    prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
    # alg method
    alg = prob.parameters.lpmethod.values
    prob.parameters.lpmethod.set(alg.auto)
    # solve problem
    prob.solve()
    # solution variables
    var = prob.solution.get_values()
    x = var[0:n]
    opt = prob.solution.get_objective_value()
    # return
    return opt, x
###############################################
###             main                        ###
###############################################
def main():
    a = array([[1,2],[4,2],[-1,1]],dtype=float)
    b = array([4,12,1],dtype=float)
    c = array([1,1],dtype=float)
    
    opt, x = lp(a,b,c)
    print("optimal value: ",opt)
    print("optimal solution: ",x)
if __name__ == '__main__':
    main()
