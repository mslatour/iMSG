"""
Michael Cabot & Sander Latour
"""
from human import Human
from viterbi import parse
from phrase import *
import copy

class Child(Human):

  def __init__(self):
    Human.__init__(self)
  
  def observe(self, (words, meaning)):
    phrase = parse(words, meaning,
             self.str_to_phr, self.for_to_phr)
    self.add_subphrases(phrase)
    #phrase.draw()

  def add_subphrases(self, phrase):
    self.add_phrase(phrase)
    if not isinstance(phrase, ExemplarNode):
      self.add_subphrases(phrase.left())
      self.add_subphrases(phrase.right())

  def add_phrase(self, phrase):
    phrase_copy = copy.deepcopy(phrase)
    for formula in phrase_copy.meaning():
      self.for_to_phr.setdefault(formula.predicate(), 
                                 set([])).add(phrase_copy)

    for word in phrase_copy.leaves():
      self.str_to_phr.setdefault(word, set([])).add(phrase_copy)

  def grow_up(self):
    pass

if __name__=='__main__':
  import observations
  child = Child()
  observations = observations.observations
  for obs in observations:
    child.observe(obs)