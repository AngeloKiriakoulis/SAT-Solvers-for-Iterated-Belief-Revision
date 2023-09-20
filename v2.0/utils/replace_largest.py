def replace_larger_elements(K, A, B, W):
  kb_variables = set(abs(i) for j in K for i in j)
  ni_variables = set(abs(i) for j in A for i in j)
  available_variables =  kb_variables.difference(ni_variables)
  ni_list = sorted(list(ni_variables))
  available_list = sorted(list(available_variables))
  replace_dict = {}
  for i in ni_list:
    m = min(available_list)
    if m < i:
      replace_dict[i] = m
      available_list.remove(m)
      available_list.insert(0,i)
  for rep in replace_dict.items():
    for idx, clause in enumerate(K):
      for idy, element in enumerate(clause):
        if rep[0] == element:
          K[idx][idy] = rep[1]
        if -rep[0] == element:
          K[idx][idy] = -rep[1]
        if rep[1] == element:
          K[idx][idy] = rep[0]
        if -rep[1] == element:
          K[idx][idy] = -rep[0]
    for idx, clause in enumerate(A):
      for idy, element in enumerate(clause):
        if rep[0] == element:
          A[idx][idy] = rep[1]
        if -rep[0] == element:
          A[idx][idy] = -rep[1]
        if rep[1] == element:
          A[idx][idy] = rep[0]
        if -rep[1] == element:
          A[idx][idy] = -rep[0]
    for idx, clause in enumerate(B):
      for idy, element in enumerate(clause):
        if rep[0] == element:
          B[idx][idy] = rep[1]
        if -rep[0] == element:
          B[idx][idy] = -rep[1]
        if rep[1] == element:
          B[idx][idy] = rep[0]
        if -rep[1] == element:
          B[idx][idy] = -rep[0]
    try:
      temp = W[rep[0]]
      W[rep[0]] = W[rep[1]]
      W[rep[1]] = temp
    except KeyError:
      raise Exception("New Info Variables larger than the Knowledge Base.")
  print("Replacements: ", replace_dict)
  return K,A,B,W


