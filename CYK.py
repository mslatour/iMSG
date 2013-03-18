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


def makeForest(words, meaning, str_to_phr, for_to_phr):
  # initialize
  parseForest, costs = initialize_forest(words, str_to_phr)

  # expand
  for span in xrange(2, len(words)+1): # loop over spans
    for i in xrange(len(words)-span+1): # loop over sub-spans [i-k), [k-j)
      j = i+span
      for k in xrange(i+1, j): # k splits span [i,j)
        left = parseForest.get((i,k), {})
        right= parseForest.get((k,j), {})
        for x in left: # loop over nodes with span [i-k)
          for y in right: # loop over nodes with span [k-j)
            complex_phrases = get_complex_phrases(for_to_phr, costs, x, y, 
                                j-i, meaning)
            for phrase in complex_phrases: # expand trees
              currentCost = phrase.cost()
              if currentCost > costs.get((phrase, i, j), float('-inf')):
                costs[(phrase, i, j)] = currentCost
                parseForest.setdefault((i,j), {})[phrase] = (x, y, k)

  return parseForest, costs

def initialize_forest(words, str_to_phr):
  parseForest = {} # condenses all possible parse tree
  costs = {} # holds cost of each entry in 'parseForest'
  for i, word in enumerate(words): # set terminals in triangle table
    exemplars = (f for f in str_to_phr.get(word,[]) if f.span()==1)
    for exemplar in exemplars: 
      parseForest.setdefault((i,i+1), {})[exemplar] = (word, None, i+1) 
      costs[(exemplar, i, i+1)] = exemplar.cost() # set cost of node

  return parseForest, costs

def get_complex_phrases(for_to_phr, costs, x, y, span, meaning, top=False):
  x_phrases = []
  for formula in x.formulaset():
    temp_phrases = [phrase for phrase in for_to_phr.get(formula,[])
                    if phrase.span()==span]
    x_phrases.extend(temp_phrases)

  y_phrases = []
  for formula in y.formulaset():
    temp_phrases = [phrase for phrase in for_to_phr.get(formula,[])
                    if phrase.span()==span]
    y_phrases.extend(temp_phrases)

  potential_phrases = set(x_phrases) | set(y_phrases)
  complex_phrases = []
  for phrase in potential_phrases:
    temp_phrase = phrase.minimalChange(meaning, x, y)
    if temp_phrase:
      complex_phrase.append(temp_phrase)

  complex_phrases.append(PhraseNode.mergeNodes(x, y, meaning))

  return complex_phrases

if __name__=='__main__':
  import observations
  observations = observations.observations
  
  snake_f = PropertyFormula('snake')
  bit_f = RelationFormula('bit')
  pig_f = PropertyFormula('pig')
  
  snake_fs = FormulaSet([snake_f])
  bit_fs = FormulaSet([bit_f])
  pig_fs = FormulaSet([pig_f])
  
  snake_e = ExemplarNode(snake_fs, 1)
  bit_e = ExemplarNode(bit_fs, 1)
  pig_e = ExemplarNode(pig_fs, 1)

  snake_e.addString('snake')
  bit_e.addString('bit')
  pig_e.addString('pig')
  
  str_to_phr = {'snake': [snake_e],
                'bit': [bit_e],
                'pig': [pig_e]}

  for_to_phr = {}
  for obs in observations:
    words = obs[0]
    meaning = obs[1]
    print 'words: %s' % (words,)
    print 'meaning: %s' % meaning
    parseForest, costs = makeForest(words, meaning,\
                         str_to_phr, for_to_phr)
    parse = list(parseForest[(0,len(words))])[0]
    print 'parse: %s' % parse
    print 'costs: %s' % parse.cost()
    print ''
    parse.draw()

