"""
Michael Cabot & Sander Latour
"""
from human import Human
from phrase import *
import viterbi
import copy

class Child(Human):

  def __init__(self):
    Human.__init__(self)
  
  def observe(self, (words, meaning)):
    phrase = viterbi.parse(words, meaning,
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
      
  def reinforce_and_discourage(self, words, meaning, lexicon, grammar):
    parse_forest, costs = viterbi.make_forest(words, meaning,
                          lexicon, grammar)
    correct_parse_cost = None
    span = (0,len(words))
    for top in parseForest[span]:
      if top==meaning:
        correct_parse_cost = costs[(top,)+span]
        self.reinforce(parse_forest, lexicon, grammar, top)
        break

    for top in parseForest[span]:
      if top==meaning:
        continue

      if costs[(top,)+span] < correct_parse_cost:
        self.discourage(parse_forest, lexicon, grammar, top)

  def reinforce(self, parse_forest, lexicon, grammar, top, span):
    rules = get_rules(parse_forest, top, span)
    for rule in rules:
     rule.reinforce()

  def discourage(self, parse_forest, lexicon, grammar, top, span):
    rules = get_rules(parse_forest, top, span)
    for rule in rules:
      rule.discourage()

  def grow_up(self):
    pass

if __name__=='__main__':
  import observations
  child = Child()
  observations = observations.observations
  for obs in observations:
    child.observe(obs)