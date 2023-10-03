from math import inf
import os
import random
import time
import psutil
from revision.replace_largest import replace_larger_elements
from revision.gen import generate_nested_lists
from revision.symbols import boolpy
# from revision.conv_test import reduce_array
from set import Set
from pysat.solvers import Glucose4
from revision.forget import forget
from revision.negation import negate
from typing import Optional,Tuple,List



class BeliefRevision:
  """This class represents an algorithm designed to perform belief revision in a knowledge base.
  Belief revision is the process of updating or modifying a set of beliefs (knowledge base) based
  on new information or evidence."""

  def __init__(self):
    #The initial set of beliefs or knowledge base.

    # here = os.path.dirname(os.path.abspath(__file__))
    # filename = os.path.join(here, 'RTI_k3_n100_m429_1.cnf')
    # self.beliefs = Set(filename=filename)
    # K = self.beliefs.elements

    self.beliefs = Set(filename="RTI_k3_n100_m429/RTI_k3_n100_m429_0.cnf")
    # for i in range(1,100):
    #   string = f"RTI_k3_n100_m429/RTI_k3_n100_m429_{i}.cnf"
    #   self.beliefs += Set(filename=string)
    K = self.beliefs.elements
    # # #The new information or evidence to be incorporated into the knowledge base.
    # self.info = Set("sets/info.cnf")
    # # #The integrity constraints of a domain
    # self.integrityConstraints = Set("sets/ic.cnf")
    # # #The given query that need to be checked 
    # self.query = Set("sets/query.cnf")
    # logging.debug("initializing sets")
    # K = [[1, 2], [3, -1, 4, -2], [-1, 2], [1, 5], [-2, -5], [-4,-5]]
    A = [[-1,-2]]
    B = [[1],[-5]]

    self.max_element = max([element for row in K for element in row])
    # Generate a dictionary with random values
    self.weights = {i: random.randint(1, 5) for i in range(1,self.max_element+1)}
    K,A,B,self.weights = replace_larger_elements(K,A,B,self.weights)
    self.beliefs = Set(elements = K) 
    self.info = Set(elements = A)
    self.query = Set(elements = B)
    try: 
      self.K_IC = self.beliefs + self.integrityConstraints
      self.f_IC = self.info + self.integrityConstraints
    except AttributeError: 
      self.K_IC = Set(elements = K)
      self.f_IC = Set(elements = A)

  def solve_SAT(self, cnf , find_worlds = False, assumptions = []) -> Tuple[bool, Optional[List[int]]]:
    worlds = []
    solver = Glucose4()
    for clause in cnf:
      solver.add_clause(clause)
    flag = solver.solve(assumptions)
    if find_worlds == True:
      for model in solver.enum_models():
        worlds.append(model)
    solver.delete()
    return flag, worlds

  def implies(self, source, query, assumption = []):
    #Need to check cases where query are sub-lists of the source    
    prob = source.elements + negate(query.elements)
    return not self.solve_SAT(prob, assumptions = assumption)[0]
    
  def query_answering(self):
    #Step 1
    K_IC_flag = self.solve_SAT(self.K_IC.elements)
    if not K_IC_flag: return self.implies(self.info, self.query)
    #Step 1.5
    K_r = Set(elements = forget(self.K_IC.elements,list(self.f_IC.language)))
    #Step 2
    if len(self.f_IC.language.intersection(self.query.language)) == 0: 
      print(self.implies(K_r,self.query))
      return
    #Step 3
    f_IC_flag, f_IC_worlds = self.solve_SAT(self.f_IC.elements, find_worlds=True)
    if not f_IC_flag: return "New Information contain inconsistencies"
    #Steps 4-5
    self.Q = self.find_Q(f_IC_worlds)
    self.S = self.find_S(self.Q)
    if self.S is None:
      print("S is empty,no new info worlds satisfy the Knowledge Base")
      return 
    print("S:",self.S)
    #Step 6
    self.T = self.find_T(f_IC_worlds,self.S)
    print("T:",self.T)
    #Step 7
    self.W = [item[1] for item in self.T]
    print("W:",self.W)
    #Step 8
    # temp_dict = {item: [self.weights[atom]] for atom in self.W for item in atom}
    temp_dict ={}
    for atom in self.W:
      c=0
      for item in atom:
        if item == 0:
          temp_dict[tuple(atom)] = 0
        else:
          c+=self.weights[item]
      temp_dict[tuple(atom)] = c
    min_value = min(temp_dict.values())
    self.E = [key for key, value in temp_dict.items() if value == min_value]
    print("E:",self.E)
    print("E:",self.E[0])
    #Step 9
    self.R = [t[0] for t in self.T if tuple(t[1]) == self.E[0]]
    print("R:",self.R)
    #Step 10-11
    dnf = []
    for clause in self.R:
      l2 = []
      for atom in clause:
        l2.append([atom])
      dnf.append(l2)
    self.H = boolpy(dnf)
    print("H:",self.H)
    #Step 12
    print(self.implies(K_r,self.query,assumption=self.H))

  def find_Q(self, worlds):
    Q=[]
    for x in worlds:
      l2 = []
      for y in x:
        if abs(y) in list(self.f_IC.language):l2.append(y)
      if l2 not in Q:
        Q.append(l2)
    return Q

  def find_S(self, Q):
    S=[]
    Q_new = []
    new_list = Q
    n = max([element for row in Q for element in row])
    for i in range(n):
      Q_new.extend(generate_nested_lists(new_list, i))
      new_list = Q_new
      print(f"Q({i}):",Q_new)
      for q in Q_new:
        solver = Glucose4()
        for clause in self.K_IC.elements:
          solver.add_clause(clause)
        if solver.solve(assumptions = q):
          if q not in S:
            S.append(q)
            continue
        # solver.delete() 
      if len(S)!=0: return S
    # return S 
  
  #NEED TO CHECK MORE EFFICIENT WAY TO FIND THE MODELS NEEDED
  def find_T(self,worlds,S):
    T=[]
    # W = [[atom for atom in world if atom in s] for world in worlds for s in S]
    W = []
    for s in S:
      for w in worlds:
        l = [atom for atom in w if atom in s or -atom in s]
        if l not in W:
          W.append(l)
    min = inf
    for s in S:
      for w in W:
        if w == s:
          return [(w,[0])]
        if len(set(w).difference(s)) == min and (w, [abs(x) for x in list(set(w).difference(s))]) not in T:
          T.append((w, [abs(x) for x in list(set(w).difference(s))]))
          min = len(set(w).difference(s))
        elif len(set(w).difference(s)) < min and (w, [abs(x) for x in list(set(w).difference(s))]) not in T:
          T = [(w, [abs(x) for x in list(set(w).difference(s))])]
          min = len(set(w).difference(s))
    return T

if __name__ == "__main__":
  start_time = time.time()
  # with ProcessPoolExecutor() as executor:
  BeliefRevision().query_answering()
  end_time = time.time()
  execution_time = end_time - start_time
  print("Execution time:", execution_time, "seconds")
  process = psutil.Process()
  memory_usage = process.memory_info().rss / 1024 / 1024 # in megabytes
  print("Memory usage:", memory_usage, "MB")