README FOR v1.0 of the belief revision app

Completed:
- Classes that represent the sets of the Knowledge Base(KB), New Info and Querries and can read from files.
- General Algorithm that was developed by Peppas et al. (2023). Functionality is established. Efiiciency is not

Problems:
- Works with large KBs but only for 1/2 new info variables. This is due to bad practices on some algorithms:
    - CNF converters. I am using a CNF converter from the boolpy module that takes to much time for large formulas.
    - Worlds searching: for higher variables i am creating too many worlds for my br algorithms to parse(findT and self.W)
  
