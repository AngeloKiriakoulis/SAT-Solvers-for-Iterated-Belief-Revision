import os
from pysat.formula import CNF
import numpy as np
# The Set class encapsulates functionalities for managing and manipulating unique sets of integers. It ensures uniqueness of elements within the set and stores them in a compact NumPy array. The class enables set combination and comparison, supports addition and removal of elements, loading CNF clauses from files, and identifying the unique absolute values present in the set. It serves as a versatile toolkit for working with constraint-based problems and CNF representations.
class Set():
  # Constructor to initialize the class
  def __init__(self, filename=None, elements = []):
    
    # Store unique elements as a NumPy array of type int16
    self.elements = np.array(elements, dtype=object)
    
    try:
      # Attempt to load CNF clauses from a file (if provided)
      self.load(filename)
    except:
      pass
    
    # Find the language (set of unique absolute values) in the elements
    self.language = self.find_language()

  # Overload the "+" operator for combining Set objects
  def __add__(self, other):
    if isinstance(other, Set):
      # Concatenate the elements of self and other
      return np.append(self.elements, other.elements, axis=0)
      # Alternatively, create and return a new Set with concatenated elements
      # return Set(elements=self.elements + other.elements)
    else:
      raise TypeError("Unsupported operand type. Please provide another Set object.")

  # Overload the "==" operator for comparing Set objects
  def __eq__(self,other):
    if isinstance(other, Set):
      return self.elements == other.elements
    return False

  # Overload the "__str__" method to provide a string representation of the object
  def __str__(self):
    try:
      # Attempt to retrieve CNF clauses if available, otherwise use raw elements
      return f"{self.elements.clauses}"
    except AttributeError:
      return f"{self.elements}"
    
  def add(self, element):
    self.elements = np.append(self.elements, element,axis=0)

  def remove(self, element):
    # Find indices of elements to remove
    indices_to_remove = np.where(self.elements == element)[0]
    
    if indices_to_remove.size > 0:
      # Remove elements at specified indices
      self.elements = np.delete(self.elements, indices_to_remove,axis=0)

  # Load CNF clauses from a file
  def load(self, filename):
    with open(filename, 'r+') as fp:
      # Load CNF clauses and store them as NumPy array
      self.elements = np.array(CNF(from_fp=fp).clauses)
      fp.seek(0)
    fp.close()

  # Find the language (set of unique absolute values) in the elements
  def find_language(self):
    language = set()
    for i in self.elements:
      for j in i:
        language.add(abs(j))  
    return language
     