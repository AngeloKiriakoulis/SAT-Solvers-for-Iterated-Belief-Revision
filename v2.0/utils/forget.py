import itertools
import logging
from typing import List, Optional, Tuple

from utils.tseitin import Tseitin
from pysat.solvers import Glucose4

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def forget(V, P, new_info):
  """
    ### "Forgets" the values of 'P' in a CNF formula 'V', by generating all combinations of True and False values for the variables in P.For each combination, it iterates over V and replaces the values based on the condition.

    #### Args:
        V (list): The original list of CNF clauses represented as sublists.
        P (list): The condition list representing the variables to forget.

    #### Returns:
        list: A CNF formula representing the result of forgeting values in V based on the combinations of True and False values in P.

    #### Description:
        This function replaces the values in V based on the condition list P. It generates all combinations of True and False values for the variables in P using binary representation. For each combination, it iterates over V and replaces the values based on the condition.

        If a value in the sublist (clause) matches a value in P, it assigns the corresponding combination value. If the value in the sublist is negative, it flips the combination value.

        The function then checks for clauses (represented as CNF clauses in V) with only one True occurrence and removes them, as the CNF clauses are also True. If a clause is entirely False, the function continues to the next combination since the entire CNF result would be False. Finally, it removes any False occurrences from the remaining clauses.

        Finally, the method appends non-conflicting clauses (clauses not present in conflicting_clauses) to the resulting formula.

    """
  
  # Generate all combinations of True and False values for the P list. We only keep those that satisfy the New Information SAT problem.
  # combinations = []
  # for combination in list(itertools.product([False, True], repeat=len(P))):
  #   combo_list = [P[index] for index, value in enumerate(combination) if value]
  #   if solve_SAT(new_info,find_worlds=False,assumptions=combo_list)[0]:
  #     combinations.append(combination)


  combinations = list(itertools.product([False,True], repeat=len(P)))
  conflicting_clauses = []
  non_conflicting_clauses = []

  # Identify conflicting and non-conflicting clauses
  for sublist in V.tolist():
    for item in P:
      if item in sublist or -item in sublist:
        conflicting_clauses.append(sublist)
        if sublist in non_conflicting_clauses:
          non_conflicting_clauses.remove(sublist)
        break
    else:
      if sublist not in non_conflicting_clauses:
        non_conflicting_clauses.append(sublist)

  # Filter V to only include conflicting clauses
  V = [i for i in V.tolist() if i in conflicting_clauses]
  result_lists = []
  for combination in combinations:
    result_list = []
    for clause in V:
      clause_result = []
      for i in range(len(clause)):
        # Check if the clause value is present in the P list or its negation
        if abs(clause[i]) in P:
          value_index = P.index(abs(clause[i]))
          value = combination[value_index]
          # Handle negative values in the clause
          if clause[i] < 0:
            value = not value
          clause_result.append(value)
        else:
          clause_result.append(clause[i])
        # Check if the clause has only one True occurrence
      if any(clause_result) and clause_result.count(True) == 0:
        # print("CR(TRUE):", clause_result)
        result_list.append(clause_result)

        # Check if the entire clause is False, so we can continue to the next combination
      if all(value is False for value in clause_result):
        break
          

    # Check if any False occurrence should be removed from the result list
    result_list = [[value for value in clause if value is not False] for clause in result_list]
    if any(result_list) and result_list not in result_lists and solve_SAT(result_list)[0]:  # Only add non-empty and new result lists
        result_lists.append(result_list)
    else:
        continue

  max_element = max([element for row in V for element in row])
  cnf = Tseitin(result_lists,max_element).transformation
  
  # Append non-conflicting clauses to the resultingCNF formula
  for clause in non_conflicting_clauses:
      cnf.append(clause)

  return cnf

def solve_SAT(cnf , find_worlds = False, assumptions = []) -> Tuple[bool, Optional[List[int]]]:
    worlds = []
    solver = Glucose4()
    for clause in cnf:
      try:
        solver.add_clause(clause)
      except RuntimeError:
        solver.add_clause([clause])
    flag = solver.solve(assumptions)
    if find_worlds == True:
      for model in solver.enum_models():
        worlds.append(model)
    solver.delete()
    return flag, worlds