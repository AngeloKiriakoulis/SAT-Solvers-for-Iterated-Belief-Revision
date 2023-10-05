def replace_larger_elements(K, A, B, W):
  # Step 1: Create sets of absolute values of elements in K and A
  kb_variables = set(abs(i) for clause in K for i in clause)
  ni_variables = set(abs(i) for clause in A for i in clause)

  # Step 2: Find available variables by subtracting ni_variables from kb_variables
  available_variables = kb_variables - ni_variables

  # Step 3: Sort the sets to prepare for replacement
  ni_list = sorted(list(ni_variables))
  available_list = sorted(list(available_variables))
  replace_dict = {} # Dictionary to store replacements

  # Step 4: Iterate through ni_list and replace variables with available ones
  for i in ni_list:
    try:
      m = min(available_list)
      if m < i:
        replace_dict[i] = m
        available_list.remove(m)
        available_list.insert(0, i)
    except:
      return K, A, B, W

  # Step 5: Replace variables in the input lists (K, A, B) using replace_dict
  for rep in replace_dict.items():
    for clause_list in [K, A, B]:
      for clause in clause_list:
        for idx, element in enumerate(clause):
          if rep[0] == element:
            clause[idx] = rep[1]
          elif -rep[0] == element:
            clause[idx] = -rep[1]
          elif rep[1] == element:
            clause[idx] = rep[0]
          elif -rep[1] == element:
            clause[idx] = -rep[0]
            
    # Step 6: Update the dictionary W with the variable replacements
    try:
      temp = W[rep[0]]
      W[rep[0]] = W[rep[1]]
      W[rep[1]] = temp
    except KeyError:
      raise Exception("New Info Variables larger than the Knowledge Base")

  print("Replacements: ", replace_dict)
  # Step 7: Return the modified input lists and dictionary
  return K, A, B, W
