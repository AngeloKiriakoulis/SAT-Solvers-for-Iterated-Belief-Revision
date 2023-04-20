class BeliefSet:
    def __init__(self):
        self.beliefs = []

    def __repr__(self):
        return f"BeliefSet({self.beliefs})"
    
    def __str__(self):
        return f"{self.beliefs}"
    
    def add_belief(self, belief):
        self.beliefs.append(belief)
    
    def remove_belief(self, belief):
        self.beliefs.remove(belief)

    def load(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                chars = line.split()
                belief = list(map(int, chars))
                self.add_belief(belief)
        f.close()    
        
class Evidences:
    def __init__(self):
        self.evidences = []
    
    def __repr__(self):
        return f"Evidences: ({self.evidences})"
    
    def __str__(self):
        return f"{self.evidences}"
    
    def add_evidence(self, evidence):
        self.evidences.append(evidence)
    
    def remove_evidence(self, evidence):
        self.evidences.remove(evidence)

    def load(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                chars = line.split()
                evidence = list(map(int, chars))
                self.add_evidence(evidence)
        f.close()  

belief_set = BeliefSet()
belief_set.load("KB.txt")
# belief_set.add_belief('p')
# belief_set.add_belief('q')
print(belief_set) 

