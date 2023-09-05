# README FOR v2.0 of the belief revision app

Completed:
- Classes that represent the sets of the Knowledge Base(KB), New Info and Querries and can read from files.
- General Algorithm that was developed by Peppas et al. (2023). Functionality is established. Efiiciency is not

Implemented in v2.0:
- forget() results filtering: Instead of finding every combination for the variables of the new information, we keep only those that satisfy a SAT problem of the new information. 

We do not need to check the cases of forget(), where the new information is not satisfied. Thus we save computational time and space, without losing useful information in our problem.

Problems:
- Works with large KBs but only for 1/2 new info variables. This is due to bad practices on some algorithms:
- CNF converters. I am using a CNF converter from the boolpy module that takes to much time for large formulas.
- Worlds searching: for higher variables i am creating too many worlds for my br algorithms to parse (findT and self.W in belief_revision.py)
  
