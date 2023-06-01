from sympy.logic.boolalg import to_cnf
from sympy.abc import *

"""The convert_to_cnf function takes a nested list v representing a logical expression in disjunctive
form. The function then constructs a string expr to represent the logical expression in a string format
that SymPy can evaluate and convert to CNF."""
def convert_to_cnf(v):
  expr = ""
  for set in v:

    #The code iterates over each "set" in v, which corresponds to the outermost parentheses in the expression. It appends a "(" to expr to open the set.
    expr+="("
    for clause in set:

      #Next, the code iterates over each "clause" within a set, which corresponds to the inner parentheses within each set. If the clause contains more than one literal, it appends an additional "(" to expr to open the clause.
      if len(clause)>1:
        expr+="("
      for p in clause:
        if p>0:

          #If the literal is positive (p > 0),it appends the corresponding variable character (chr(abs(p)+64)) to expr.
          expr+=chr(abs(p)+64)
        else:

          #If the literal is negative, it appends the negation symbol (~) followed by the corresponding variable character to expr.
          expr+= "~" +chr(abs(p)+64)
        expr+="|"

      #After each literal, the code appends a "|" to separate the literals within a clause. It removes the trailing "|" using expr = expr[:-1].
      expr = expr[:-1]
      if len(clause)>1:
        expr+=")"
      expr+="&"

    #After each clause, the code appends an "&" to separate the clauses within a set. It removes the trailing "&" using expr = expr[:-1].
    expr = expr[:-1]    
    expr+=")|"

  #Finally, the code appends a ")" to close the set. It removes the trailing "|" and prints the CNF representation of the logical expression using to_cnf(eval(expr), True).
  expr = expr[:-1]

  #The eval function in Python is used to evaluate and execute dynamically created code represented as a string.
  return to_cnf(eval(expr))
      
convert_to_cnf([[[1,2],[-3]],[[2]]])
