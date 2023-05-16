from pysat.formula import CNF

class Set():
    def __init__(self, filename):
      self.elements = []
      self.language = set()
      self.load(filename)
      self.find_language()

    def __add__(self, other):
      if isinstance(other, Set):
        return self.elements + other.elements, self.language.intersection(other.language)
      else:
        raise TypeError("Unsupported operand type. Please provide another Set object.")
      
    def __str__(self):
      try:
        return f"{self.elements.clauses}"
      except AttributeError:
        return f"{self.elements}"

    def add(self, element):
      self.elements.append(element)

    def remove(self, element):
      self.elements.remove(element)

    def load(self, filename):
      with open(filename, 'r+') as fp:
        self.elements = CNF(from_fp=fp).clauses
        fp.seek(0)
      fp.close()

    def find_language(self):
      try:
        for clause in self.elements.clauses:
          for literal in clause:
            atom = abs(literal)
            self.language.add(atom)
      except AttributeError:
        try:
          for clause in self.elements:
            for literal in clause:
              atom = abs(literal)
              self.language.add(atom)
        except TypeError:
          for sentence in self.elements:
            for clause in sentence:
              for literal in clause:
                atom = abs(literal)
                self.language.add(atom)