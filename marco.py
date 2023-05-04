from pysat.solvers import Glucose3

# Parse the constraint set in CNF form using the pySAT library
cnf = [[1],[-1],[2],[-2],[1,2]]
# cnf = [[1, 2, 3], [-1, -2], [2, 3], [-3, -1], [1], [2]]
cnf = [[-1,2], [1,-2], [3], [-1,-3], [2,-3], [-3]]
cnf = [[-1,2],[-2,3],[-3]]

# Compute one minimum unsatisfiability sub-set from a random unsatisfiable constraint subset that we input.
def shrink(seed):
    for c in seed[:]:
        seed_copy = seed.copy()
        seed.remove(c)
        solver = Glucose3()
        for clause in seed:
            solver.add_clause(clause)
        if solver.solve():
            seed = seed_copy
    solver.delete()
    return seed

# Compute one maximum satisfiability sub-set from a random unsatisfiable constraint subset that we input.
def grow(seed):
    for c in cnf:
        while True:
            if c not in seed:
                solver = Glucose3()
                for clause in seed:
                    solver.add_clause(clause)
                solver.add_clause(c)
                if solver.solve():
                    seed += [c]
                else: break
            else: break
            solver.delete()
    return seed

def blockUp(mus):
    blockup_list=[]
    for i in mus: blockup_list.append(-cnf.index(i)-1)
    return blockup_list

def blockDown(mss):
    blockdown_list=[]
    for i in cnf: 
        if i not in mss:
            blockdown_list.append(cnf.index(i)+1)
    return blockdown_list

def getUnexplored(Map):
    solver = Glucose3()
    highest_num_positives = 0
    lists_with_highest_num_positives = []
    f = []
    for clause in Map:
        solver.add_clause(clause)
    solver.solve()
    # Iterate over each list
    for formula in solver.enum_models():
        # Count the number of positive values in the list
        num_positives = len(list(filter(lambda x: x > 0, formula)))
        if num_positives > highest_num_positives:
            highest_num_positives = num_positives
            lists_with_highest_num_positives = [formula]
        elif num_positives == highest_num_positives:
            lists_with_highest_num_positives.append(formula)
    for formula in lists_with_highest_num_positives:
        s = []
        for i in formula:
            if i>0:s.append(cnf[i-1])
        f.append(s)
    return f

def isSatifiable(problem):
    solver = Glucose3()
    for clause in problem:
        solver.add_clause(clause)
    flag = solver.solve()
    return flag

Map=[[i+1 for i in range(len(cnf))]]
mus_list = []
mss_list = []
while True:
    seed_list = getUnexplored(Map)
    for seed in seed_list:
        if isSatifiable(seed):
            mss = grow(seed)
            if mss not in mss_list:
                mss_list.append(mss)
                Map.append(blockDown(mss))
        else:            
            mus = shrink(seed)
            if mus not in mus_list: 
                mus_list.append(mus)
                Map.append(blockUp(mus))
        seed_list.remove(seed)
    if not isSatifiable(Map): 
        break
print("Maximum Satisfiable Subsets:")
for i in mss_list:
    print(i)
print("Minimum Unsatisfiable Subsets:")
for i in mus_list:
    print(i)
