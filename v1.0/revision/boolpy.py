import boolean


def boolpy(expression):
  algebra = boolean.BooleanAlgebra()
  l = {str(i): i for i in range(100)}
  TRUE, FALSE, NOT, AND, OR, symbol = algebra.definition()
  l=[]
  for cnf in expression:
    l1=[]
    for clause in cnf:
      if len(cnf) == 1 and len(clause) == 1:
        l1.append(algebra.symbols(clause[0])[0])
      elif len(cnf) == 1:
        l1.append(OR(*algebra.symbols(*clause)))
      elif len(clause) == 1:
        l1.append(algebra.symbols(clause[0])[0])
      else:
        l1.append(OR(*algebra.symbols(*clause)))
    if len(l1) == 1:
      l.append(l1[0])
    elif len(l1) > 1:
      l.append(AND(*l1))
    else:pass
  if len(l) == 1:
    expr = l[0]
  else:
    expr = OR(*l)
  cnf = []
  # print("SIMPLE:",expr.simplify())
  cnf_expr = algebra.cnf(expr).simplify()
  if type(expr) == AND:
    for arg in expr.args:
      cnf.append(int(str(arg)))
  else:
    for clause in cnf_expr.args:
      l1=[]
      for arg in list(clause.symbols):
        l1.append(int(str(arg)))
      cnf.append(l1)




  #SO QUICK UP UNTIL HERE, need to find a good way to convert back from the symbols to lists.
  
  return cnf

