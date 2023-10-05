from math import inf
import time
from utils.gen import generate_nested_lists
import numpy as np
import psutil
import xlsxwriter

from utils.tseitin import Tseitin
from utils.set import Set
from utils.boolpy import boolpy
from utils.forget import forget
from utils.negation import negate
from utils.replace_largest import replace_larger_elements
from pysat.solvers import Glucose4

from typing import Optional,Tuple,List
import logging
import os
import random

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class BeliefRevision:
  """This class represents an algorithm designed to perform belief revision in a knowledge base.
  Belief revision is the process of updating or modifying a set of beliefs (knowledge base) based
  on new information or evidence."""

  def __init__(self, filename):
    #The initial set of beliefs or knowledge base.

    # # Huge KB Example
    # self.beliefs = Set(filename=filename)
    # for i in range(1,100):
    #   KB_file = f"RTI_k3_n100_m429/RTI_k3_n100_m429_{i}.cnf"
    #   self.beliefs += Set(filename=KB_file)
    # K = self.beliefs.elements.tolist()

    # Typical Example
    # K = [[3, 5], [1, -2, 4, -5], [-3, 5], [3, 2], [-5, -2], [-4,-2]]
    # print("KB:",K)
    # A = [[-5,-3]]
    # print("NI:",A)
    # B = [[1],[-5]]
    # print("Q:",B)
    
    # User Input
    try:
      here = os.path.dirname(os.path.abspath(__file__))
      KB_input = input("\nProvide the initial Knowledge Base: ")
      KB_file = os.path.join(here, KB_input)
      if os.path.exists(KB_file):
        self.beliefs = Set(filename=KB_file)
        K = self.beliefs.elements.tolist()
      else:
        self.beliefs = Set(elements=eval(KB_input))
        K = self.beliefs.elements

      NI_input = input("Provide the New Information:")
      NI_file = os.path.join(here, NI_input)
      if os.path.exists(NI_file):
        self.info = Set(filename=NI_file)
        A = self.info.elements.tolist()
      else:
        self.info = Set(elements=eval(NI_input))
        A = self.info.elements

      Q_input = input("Provide the Query:")
      Q_file = os.path.join(here, Q_input)
      if os.path.exists(Q_file):
        self.query = Set(filename=Q_file)
        B = self.info.elements.tolist()
      else:
        self.query = Set(elements=eval(Q_input))
        B = self.query.elements
    except FileNotFoundError: 
      print("Rerun the program with non-empty values")
      raise SystemExit(0)

    W_input = input("Provide the Belief Weights Dictionary:")
    self.weights =eval(W_input)

    self.max_element = max([element for row in K for element in row])
    
    # Generate a dictionary with random values
    self.weights = {i: random.randint(1, 5) for i in range(1,self.max_element+1)}
    print("\n")
    K,A,B,self.weights = replace_larger_elements(K,A,B,self.weights)
    self.beliefs = Set(elements = K)
    self.info = Set(elements = A)
    self.query = Set(elements = B)
    # print("Weights:", self.weights)
    try: 
      self.K_IC = self.beliefs + self.integrityConstraints
      self.f_IC = self.info + self.integrityConstraints
    except AttributeError: 
      self.K_IC = Set(elements = K)
      self.f_IC = Set(elements = A)
    


  def solve_SAT(self, cnf , find_worlds = False) -> Tuple[bool, Optional[List[int]]]:
    worlds = [] # Initialize an empty list to store possible worlds
    solver = Glucose4() # Create a Glucose4 solver instance

    # Loop through the clauses in 'cnf' and add them to the solver
    for clause in cnf:
      try:
        solver.add_clause(clause)
      except RuntimeError:
        # If a RuntimeError occurs when adding a clause, add a single-element list
        solver.add_clause([clause])

    flag = solver.solve()
    # If 'find_worlds' is True, enumerate all satisfying models and store them in 'worlds'
    if find_worlds == True:
      for model in solver.enum_models():
          worlds.append(model)
    solver.delete() # Clean up and delete the solver instance

    # Return the result of the solver (flag) and the list of satisfying worlds
    return flag, worlds


  def implies(self, source, query, assumption = []):
    assumptions = []
    try:
      for multiple_assumption in assumption:
        if self.solve_SAT(multiple_assumption)[0]:
          assumptions.append(multiple_assumption)
    except TypeError:
      assumptions = assumption
    
    neg = negate(query.elements) # Negate the elements in the 'query' and store them in 'neg'
    
    """Numpy treats anything that is a list or tuple as a special item that you want to convert into an array at the outer level. To append an element to an object array without having the fact that it is a list in your way, you have to first create an array or element that is empty."""
    c = np.empty(1, dtype=object) 

    # Loop through the elements in 'neg' and append them to 'source.elements'
    for i in range(len(neg)):
        c[0] = neg[i]
        source.elements = np.append(source.elements, c)
    # Return the result of solving a SAT problem, to check if the implication is true.
    c = np.empty(1, dtype=object) 

    # Loop through the elements in 'neg' and append them to 'source.elements'
    for assumption in assumptions:
      try:
        for literal in assumption:
          c[0] = [literal]
          source.elements = np.append(source.elements, c)
          if self.solve_SAT(source.elements.tolist(),find_worlds=False)[0]: return False
        return True
      except TypeError:
        c[0] = [assumption]
        source.elements = np.append(source.elements, c)
    return not self.solve_SAT(source.elements.tolist(),find_worlds=False)[0]

    
  def query_answering(self):
    start_time = time.time()
    #Step 1
    K_IC_flag = self.solve_SAT(self.K_IC.elements)
    if not K_IC_flag: return self.implies(self.info, self.query)
    #Step 1.5
    K_r = Set(elements = forget(self.K_IC.elements,list(self.f_IC.language),max_element = self.max_element))
    #Step 2
    if len(self.f_IC.language.intersection(self.query.language)) == 0: 
      print(self.implies(K_r,self.query))
      return
    #Step 3
    f_IC_flag, f_IC_worlds = self.solve_SAT(self.f_IC.elements, find_worlds=True)
    if not f_IC_flag: return "New Information contains inconsistencies"
    #Steps 4-5
    self.Q = self.find_Q(f_IC_worlds)
    self.S = self.find_S(self.Q)
    print("S:",(self.S))
    if self.S is None:
      print("New info variables have no worlds that satisfy the Knowledge Base")
      end_time = time.time()
      execution_time = end_time - start_time
      print("Execution time:", execution_time, "seconds")
      return
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
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    return execution_time

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
      if len(S)!=0: return S

  def find_T(self,worlds,S):
    if S is None:
      print("NO")
      return
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
  workbook = xlsxwriter.Workbook('version2.xlsx')
  worksheet = workbook.add_worksheet()
  first_time = time.time()
  for i in range(1,100):
    KB_file = f"RTI_k3_n100_m429/RTI_k3_n100_m429_{i}.cnf"
    exec_time = BeliefRevision(KB_file).query_answering()
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024 # in megabytes
    print("Memory usage:", memory_usage, "MB")
    worksheet.write(f'A{i}', exec_time)
    worksheet.write(f'B{i}', memory_usage)
  end_time = time.time()
  print(end_time-first_time)
  workbook.close()
    