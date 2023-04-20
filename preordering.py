import heapq

# Define the propositional atoms
atoms = [1, 2, 3, 4, 5]

# Define the weights or priorities for the atoms
weights = {1: 3, 2: 1, 3: 2, 4: 4, 5: 2}

# Create a priority queue for the atoms based on their weights
pq = [(weights[a], a) for a in atoms]
heapq.heapify(pq)

# Process the atoms in priority order
while pq:
    _, atom = heapq.heappop(pq)
    # Do something with the atom
    print(atom)
