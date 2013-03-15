'''
By:
Michael Cabot (6047262), Richard Rozeboom (6173292)

Creates a parse forest for a sentence given a corpus. The parse forest
is represented by a dictionary that maps a span [i,j) to a dictionary
mapping parents to their left and right child. Each parent represents
a partial derivation of the sentence. The probability of these parents
are kept in a separate dictionary mapping a node in a span to its
probability.
'''

import re
from phrase import *
from formula import *

MERGE_COST = 1 # TODO this should be located somewhere else

def makeForest(string, meaning, grammar):
  """TODO write new docstring
  Creates parse forest: all possible (sub)trees with probabilities
  for a sentence given a grammar.
  Arguments:
  string    - contains words separated by single whitespace
  grammar   - dictionary mapping rhs to [(P(rule_1), lhs_1), ..., (P(rule_n), lhs_n)]
  Return:
  parseForest - dictionary mapping span [i,j) to dictionary mapping parent to (left-child, right-child, k)
  costs     - dictionary mapping (node, i, j) to P(node)"""
  string = string.strip() # remove whitespace+\n @ start and end   
  words = string.split(' ')
  # initialize
  parseForest, costs = initialize_forest(words, grammar)

  # expand
  for span in xrange(2, len(words)+1): # loop over spans
    for i in xrange(len(words)-span+1): # loop over sub-spans [i-k), [k-j)
      j = i+span
      for k in xrange(i+1, j): # k splits span [i,j)
        left = parseForest.get((i,k), {})
        right= parseForest.get((k,j), {})
        for x in left: # loop over nodes with span [i-k)
          for y in right: # loop over nodes with span [k-j)
            complex_phrases = get_complex_phrases(grammar, costs, x, y, 
                                words[i:j], meaning)
            for phrase in complex_phrases: # expand trees
              currentCost = phrase.cost
              if currentCost > costs.get((phrase, i, j), float('-inf')):
                costs[(phrase, i, j)] = currentCost
                parseForest.setdefault((i,j), {})[phrase] = (x, y, k)

  return parseForest, costs

def initialize_forest(words, grammar):
  parseForest = {} # condenses all possible parse tree
  costs = {} # holds probability of each entry in 'parseForest'
  for i in xrange(len(words)): # set terminals in triangle table
    word = words[i]
    span1_formulas = (f for f in grammar.get(word,[]) if f.span==1)
    for formulaset in span1_formulas: 
      # entry at (i,i+1) is dictionary with key=formula and value=(leftChild, rightChild, k)
      exemplar = ExemplarNode(formulaset, COST_NEW)
      parseForest.setdefault((i,i+1), {})[exemplar] = (word, None, i+1) 
      costs[(exemplar, i, i+1)] = exemplar.cost # set cost of node

  return parseForest, costs

def get_complex_phrases(grammar, costs, x, y, words, meaning):
  full_matches = []
  left_matches = []
  right_matches = []
  span = len(words)
  for phrase in complex_phrases[:]:
    if phrase.span!=span or \
       (phrase.left()!=x and phrase.right()!=y):
      complex_phrases.remove(phrase)
      continue

    if phrase.left()==x and phrase.right()==y:
      full_matches.append(phrase)
    elif phrase.left()==x and phrase.right()!=y:
      left_matches.append(phrase)
    else:
      right_matches.append(phrase)

  # if no phrase is found, then create a new one
  x_in_meaning = x
  y_in_meaning = y
  for formula in meaning:
    if x==formula:
      x_in_meaning = formula
    if y==formula:
      y_in_meaning = formula

  if len(complex_phrases)==0:    
    cost = costs[x] + costs[y] + COST_MERGE
    phrase = PhraseNode(cost, span)
    x_map = ArgumentMap.find_mapping(x, x_in_meaning)
    y_map = ArgumentMap.find_mapping(y, y_in_meaning)
    phrase.addLeft(x_in_meaning, x_map)
    phrase.addRight(y_in_meaning, y_map)
    return [phrase]

  return complex_phrases
