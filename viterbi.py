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

def parse(words, meaning, str_to_phr, for_to_phr):
  parse_forest, _ = make_forest(words, meaning,
                    str_to_phr, for_to_phr)
  return list(parse_forest[(0,len(words))])[0]

def make_forest(words, meaning, str_to_phr, for_to_phr):
  # initialize
  parse_forest, costs = initialize_forest(words, meaning, str_to_phr)

  # expand
  for span in xrange(2, len(words)+1): # loop over spans
    for i in xrange(len(words)-span+1): # loop over sub-spans [i-k), [k-j)
      j = i+span
      for k in xrange(i+1, j): # k splits span [i,j)
        left = parse_forest.get((i,k), {})
        right= parse_forest.get((k,j), {})
        for x in left: # loop over nodes with span [i-k)
          for y in right: # loop over nodes with span [k-j)
            complex_phrases = get_complex_phrases(for_to_phr, costs, x, y, 
                                j-i, meaning)
            for phrase in complex_phrases: # expand trees
              current_cost = phrase.cost()
              if current_cost > costs.get((phrase, i, j), float('-inf')):
                costs[(phrase, i, j)] = current_cost
                parse_forest.setdefault((i,j), {})[phrase] = (x, y, k)

  return parse_forest, costs

def initialize_forest(words, meaning, str_to_phr):
  parse_forest = {} # condenses all possible parse tree
  costs = {} # holds cost of each entry in 'parse_forest'
  for i, word in enumerate(words): # set terminals in triangle table
    exemplars = (f for f in str_to_phr.get(word,set([])) if f.span()==1)
    for exemplar in exemplars: 
      parse_forest.setdefault((i,i+1), {})[exemplar] = (word, None, i+1) 
      costs[(exemplar, i, i+1)] = exemplar.cost() # set cost of node

  # if new word, create exemplar node  
  if len(parse_forest)==0 and len(words)==1:
    exemplar = ExemplarNode(meaning)
    exemplar.add_string(words[0])
    parse_forest.setdefault((0,1), {})[exemplar] = (words[0], None, i+1)
    costs[(exemplar, i, i+1)] = exemplar.cost()

  return parse_forest, costs

def get_complex_phrases(for_to_phr, costs, x, y, span, meaning, top=False):
  x_phrases = set([])
  for formula in x.meaning():
    pred = formula.predicate()
    temp_phrases = [phrase for phrase in for_to_phr.get(pred,set([]))
                    if phrase.span()==span]
    x_phrases |= set(temp_phrases)

  y_phrases = set([])
  for formula in y.meaning():
    pred = formula.predicate()
    temp_phrases = [phrase for phrase in for_to_phr.get(pred,set([]))
                    if phrase.span()==span]
    y_phrases |= set(temp_phrases)

  potential_phrases = x_phrases | y_phrases
  complex_phrases = []
  for phrase in potential_phrases:
    temp_phrase = phrase.minimal_change(meaning, x, y)
    if temp_phrase:
      complex_phrases.append(temp_phrase)

  print 'x: %s' % x
  print 'y: %s' % y
  print 'meaning: %s' % meaning
  complex_phrases.append(PhraseNode.merge(x, y, meaning))

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

  snake_e.add_string('snake')
  bit_e.add_string('bit')
  pig_e.add_string('pig')
  
  str_to_phr = {'snake': [snake_e],
                'bit': [bit_e],
                'pig': [pig_e]}

  for_to_phr = {}
  for obs in observations:
    words = obs[0]
    meaning = obs[1]
    print 'words: %s' % (words,)
    print 'meaning: %s' % meaning
    parse_forest, costs = make_forest(words, meaning,\
                         str_to_phr, for_to_phr)
    parse = list(parse_forest[(0,len(words))])[0]
    print 'parse: %s' % parse
    print 'costs: %s' % parse.cost()
    print ''
    parse.draw()

