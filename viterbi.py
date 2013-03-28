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
from PCFG import *

def get_rules(parse_forest, node, span, rules = []):
    i, j = span
    entry = parse_forest[span].get(node, None)
    if not entry: # return if reache leave
        return

    left_child, right_child, k = entry
    if right_child: # if binary rule
        current_rule = PCFGRule(node, (left_child,right_child))
        rules.append(current_rule)
        get_rules(parse_forest, left_child, (i,k), rules)
    else: # if unary rule
        current_rule = PCFGRule(node, (left_child,))
        rules.append(current_rule)
        get_rules(parse_forest, right_child, (k,j), rules)

    return rules

def make_forest(words, meaning, grammar):
    # initialize
    parse_forest, costs = initialize_forest(words, meaning, grammar.inverse())

    # expand
    for span in xrange(2, len(words)+1): # loop over spans
        for i in xrange(len(words)-span+1): # loop over sub-spans [i-k), [k-j)
            j = i+span
            for k in xrange(i+1, j): # k splits span [i,j)
                left = parse_forest.get((i,k), {})
                right= parse_forest.get((k,j), {})                
                for x in left: # loop over nodes with span [i-k)
                    for y in right: # loop over nodes with span [k-j)
                        rhs = (x,y)
                        rhs_costs = (costs[(x,i,k)], costs[(y,k,j)])
                        inv_grammar = grammar.extended_grammar(
                                                    rhs, rhs_costs).inverse()
                        for lhs, current_cost in inv_grammar[(x,y)]: # expand trees
                            if current_cost < costs.get((lhs, i, j), float('inf')):
                                costs[(lhs, i, j)] = current_cost
                                parse_forest.setdefault((i,j), {})[lhs] = (x,y,k)

    return parse_forest, costs

def initialize_forest(words, meaning, lexicon):
    parse_forest = {} # condenses all possible parse tree
    costs = {} # holds cost of each entry in 'parse_forest'
    for i, word in enumerate(words): # set terminals in triangle table
        if (word,) in lexicon:
            lhs_info = lexicon[(word,)]
        else:
            lhs_info = [(PCFGRule(meaning[i],(word,)), COST_NEW)]
        for lhs, current_cost in lhs_info:
            parse_forest.setdefault((i,i+1), {})[lhs] = (word, None, i+1)
            costs[(lhs, i, i+1)] = current_cost # set cost of node

    return parse_forest, costs

