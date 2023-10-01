def generate_nested_lists(Q, n):
    if n == 0:
        return Q
    new_lists = []
    for sublist in Q:
        for i in range(len(sublist)):
            new_sublist = sublist[:]
            new_sublist[i] *= -1
            if new_sublist not in Q:
              new_lists.append(new_sublist)
            else:
               break
    return new_lists