from math import inf
import time
import numpy as np
import psutil
from tseitin import Tseitin
from revision.boolpy import boolpy
# from revision.conv_test import reduce_array
from set import Set
from pysat.solvers import Glucose4
from revision.forget import forget
from revision.negation import negate
from typing import Optional,Tuple,List
import logging
import os
import random

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class BeliefRevision:
  """This class represents an algorithm designed to perform belief revision in a knowledge base.
  Belief revision is the process of updating or modifying a set of beliefs (knowledge base) based
  on new information or evidence."""

  def __init__(self):
    #The initial set of beliefs or knowledge base.

    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'RTI_k3_n100_m429_1.cnf')
    self.beliefs = Set(filename=filename)
    K = self.beliefs.elements

    # # #The new information or evidence to be incorporated into the knowledge base.
    # self.info = Set("sets/info.cnf")
    # # #The integrity constraints of a domain
    # self.integrityConstraints = Set("sets/ic.cnf")
    # # #The given query that need to be checked 
    # self.query = Set("sets/query.cnf")
    # logging.debug("initializing sets")
    K = [[1, 2], [3, -1, 4, -2], [-1, 2], [1, 5], [-2, -5], [-4,-5]]
    self.beliefs = Set(elements = K)  
    A =  [[-1,-2]] 
    self.info = Set(elements = A)
    B = [[-5],[1]]
    self.query = Set(elements = B)
    try: 
      self.K_IC = self.beliefs + self.integrityConstraints
      self.f_IC = self.info + self.integrityConstraints
    except AttributeError: 
      self.K_IC = Set(elements = K)
      self.f_IC = Set(elements = A)
    
    

    # Specify the number of pairs (100 in this case)
    num_pairs = 100

    # Generate a dictionary with random values
    # self.weights = {i: random.randint(0, 10) for i in range(num_pairs+1)}
    self.weights = {0: 0, 1: 2, 2: 1, 3: 1, 4: 2, 5: 3}


  def solve_SAT(self, cnf , find_worlds = False, assumptions = []) -> Tuple[bool, Optional[List[int]]]:
    worlds = [] # Initialize an empty list to store possible worlds
    solver = Glucose4() # Create a Glucose4 solver instance

    # Loop through the clauses in 'cnf' and add them to the solver
    for clause in cnf:
        try:
            solver.add_clause(clause)
        except RuntimeError:
            # If a RuntimeError occurs when adding a clause, add a single-element list
            solver.add_clause([clause])
    try:
      flag = solver.solve(assumptions) # Attempt to solve the SAT problem with the specified assumptions
    except TypeError: #More than 1 H results 
      for assumption in assumptions:
        flag = solver.solve(assumption)
        if flag:break

    # If 'find_worlds' is True, enumerate all satisfying models and store them in 'worlds'
    if find_worlds == True:
      for model in solver.enum_models():
          worlds.append(model)
      # print("WORLDS: ", worlds)

    solver.delete() # Clean up and delete the solver instance

    # Return the result of the solver (flag) and the list of satisfying worlds
    return flag, worlds


  def implies(self, source, query, assumption = []):
    #Need to check cases where query are sub-lists of the source 
    neg = negate(query.elements) # Negate the elements in the 'query' and store them in 'neg'

    """Numpy treats anything that is a list or tuple as a special item that you want to convert into an array at the outer level. To append an element to an object array without having the fact that it is a list in your way, you have to first create an array or element that is empty."""
    c = np.empty(1, dtype=object) 

    # Loop through the elements in 'neg' and append them to 'source.elements'
    for i in range(len(neg)):
        c[0] = neg[i]
        source.elements = np.append(source.elements, c)
    print(source.elements, assumption)
    # Return the result of solving a SAT problem, to check if the implication is true.
    return not self.solve_SAT(source.elements,find_worlds=True, assumptions=assumption)[0]

    
  def query_answering(self):
    #Step 1
    K_IC_flag = self.solve_SAT(self.K_IC.elements)
    if not K_IC_flag: return self.implies(self.info, self.query)
    #Step 1.5
    K_r = Set(elements = forget(self.K_IC.elements,list(self.f_IC.language),new_info=self.f_IC.elements.tolist()))
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
    print("S:",(self.S))
    #Step 6
    self.T = self.find_T(f_IC_worlds,self.S)
    print("T:",self.T)
    #Step 7
    self.W = [item[1] for item in self.T]
    print("W:",self.W)
    #Step 8
    temp_dict ={}
    for atom in self.W:
      c=0
      for item in atom:
        c+=self.weights[item]
      temp_dict[tuple(atom)] = c
    min_value = min(temp_dict.values())
    self.E = [key for key, value in temp_dict.items() if value == min_value]
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
    S = []
    i = 0
    while len(S)==0 and i<2*len(self.f_IC.language):
      Q_new = [sublist[:] for sublist in Q]  # Create a copy of the original nested list
      for sublist in Q_new:
          for j in range(i):
              sublist[j % len(sublist)] *= -1  # Modify the sublist by incrementing values
          if sublist not in Q:
            Q.append(sublist)
      print(f"Q({i}): {Q}")
      for q in Q:
        solver = Glucose4()
        for clause in self.K_IC.elements:
          solver.add_clause(clause)
        if solver.solve(assumptions = q):S.append(q)
      i += 1
    return S
  
  #NEED TO CHECK MORE EFFICIENT WAY TO FIND THE MODELS NEEDED
  def find_T(self,worlds,S):
    T=[]
    W = set()
    for w in worlds:
      for s in S:
        l = frozenset(atom for atom in w if atom in s or -atom in s)
        W.add(l)
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
  BeliefRevision().query_answering()
  end_time = time.time()
  execution_time = end_time - start_time
  print("Execution time:", execution_time, "seconds")
  process = psutil.Process()
  memory_usage = process.memory_info().rss / 1024 / 1024 # in megabytes
  print("Memory usage:", memory_usage, "MB")