# README FOR v2.0 of the belief revision app

Completed:
# v1.0
- Classes that represent the sets of the Knowledge Base(KB), New Info and Querries and can read from files.
- General Algorithm that was developed by Peppas et al. (2023). Functionality is established. Efiiciency is not.
# v2.0
- CNF converters, using Tseitin Encoding for the forget() results. Clauses grow linearly, instead of exponentially. 
- Numpy representation for the Knowledge Sets. Acceleration of parsing them.
Generally the programm got accelerated into solving the problems with big knowledge bases, a problem that could not be resolved in v1.0.  

Problems:
Works with large KBs but only for 1/2 new info variables. This is due to bad practices on some algorithms:
- Worlds searching: for higher variables i am creating too many worlds for my br algorithms to parse (findT and self.W in belief_revision.py)
  
