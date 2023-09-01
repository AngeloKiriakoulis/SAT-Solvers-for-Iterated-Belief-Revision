from typing import List
import numpy as np
from pysat.formula import CNF

from revision.boolpy import boolpy
# from revision.converter import *

def negate(formula) -> List:
  """
    # Encodes the negation of a given CNF formula using Tseitin encoding and specific list parsing.

    ### Args:
        formula (list): The CNF formula represented as a list of sublists, where each sublist represents a clause and contains positive or negative literals.

    ### Returns:
        list: The CNF formula representing the negation, encoded with the use of auxiliary Tseitin variables.

    ### Description:
        This method takes a CNF formula and applies Tseitin encoding to obtain its negation in CNF form. The negation is encoded using auxiliary Tseitin variables, which are introduced as negative numbers positioned at the end of each sublist, except when a negative number is actually a negated literal that needs to be included in the final result.

        The input 'formula' should be provided as a list of sublists, where each sublist represents a clause in the CNF formula. Each literal in a clause should be represented as a positive or negative integer.

        My method included inspecting the negation output for different inputs and analyzing the patterns to correctly identify auxiliary variables and negated literals. By observing the resulting CNF formula and the positions of the negative numbers, we conclude on which ones are auxiliary variables and which ones are negated literals to be included in the final result.

    Example:
        formula = [[1, 2], [2]]
        ### Output: [[-1, -3], [-2, -3], [1, 2, 3], [3, -2]]
    """
  print(formula.tolist())
  pos = CNF(from_clauses=formula.tolist())

  neg = pos.negate()
  print(neg.clauses)
  #Checking if all clauses in the formula are just literals, and if so, returns the negation clauses directly
  if all(len(sublist) == 1 for sublist in formula): 
    print("!!!:", np.array(neg.clauses))
    return np.array(neg.clauses)

  """This block of code initializes an empty dictionary 'clause_dict' to store the clauses based on their auxiliary variables. It iterates through the negated clauses except the last one 'neg.clauses[:-2]'. For each clause, it checks the last element 'key' to determine if it's a negative auxiliary variable. If it is, and the key is not already present in 'clause_dict', it adds a new key-value pair with the key as the negative auxiliary variable and the value as a list containing the clause without the auxiliary variable. If the key is already present, it appends the clause to the existing list. The else block is used to skip non-negative auxiliary variables."""

  clause_dict = {}
  for clause in neg.clauses[:-2]: 
    key = clause[-1]
    if key<0 and key not in clause_dict:
      clause_dict[key] = [clause[:-1]]
    elif key<0:
      clause_dict[key].append(clause[:-1])
    else:continue
  keys_list = [-x for x in list(clause_dict.keys())]
  print(keys_list)

  """This block of code compares 'keys_list' with the last clause of 'neg.clauses'. If they are not equal, it means that some negated literals are missing in 'clause_dict'. It then proceeds to fill in the missing negated literals. It initializes a variable i with the last key in 'clause_dict.keys()'. It creates a list add_atoms containing negated literals from the last clause that are not present in keys_list. It then iterates over each atom in add_atoms, decrements i by 1, and adds a new key-value pair to dictionary"""

  if keys_list != neg.clauses[-1]:
    i = list(clause_dict.keys())[-1]
    add_atoms = [x for x in neg.clauses[-1] if x not in keys_list]
    for atom in add_atoms:
      i-=1
      clause_dict[i] = [[atom]]

  print(clause_dict)
  print(list(clause_dict.values()))

  #NEEDS FIX
  negation = boolpy(list(clause_dict.values()))

  return negation
