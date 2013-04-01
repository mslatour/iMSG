from pcfg import PCFGLexicalRule, Grammar
from formula import FormulaSet
from random import sample, randint, seed
from datetime import datetime
import string
import viterbi

class Human:
    """
    :param grammar
    """
    def __init__(self, grammar = None, seed_value = None):
        self.grammar = grammar if grammar is not None else Grammar()
        self.seed_value = seed_value
        seed(seed_value)
        self.cost = 0

    def set_seed(self, seed_value):
        self.seed_value = seed_value
        seed(seed_value)

    def get_last_cost(self):
        return self.cost


class Child(Human):

    def __init__(self, grammar = None, seed_value = None):
        Human.__init__(self, grammar, seed_value)
        
    def observe(self, (words, meaning)):
        parse_forest, costs = viterbi.make_forest(words, meaning, self.grammar)
        correct_parse_cost = None
        span = (0, len(words))
        for top in parse_forest[span]: # find parse that matches the meaning
            if top == meaning:
                correct_parse_cost = costs[(top,)+span]
                reinforced_rules = self.reinforce(parse_forest, costs, 
                                                  top, span)
                break

        for rule in reinforced_rules: # add reinforced rules to grammar
            if not rule in self.grammar:
                self.grammar.append(rule)

        for top in parse_forest[span]: # discourage rule in bad parses
            if top == meaning:
                continue

            if costs[(top,)+span] < correct_parse_cost:
                self.discourage(parse_forest, costs, top, span)

    def reinforce(self, parse_forest, costs, top, span):
        rules = viterbi.get_rules(parse_forest, costs, top, span)
        for rule in rules:
            rule.reinforce()

        return rules

    def discourage(self, parse_forest, costs, top, span):
        rules = viterbi.get_rules(parse_forest, costs, top, span)
        for rule in rules:
            rule.discourage()

        return rules

    def grow_up(self):
        return Parent(self.grammar, self.seed_value+1)


class Parent(Human):

    def __init__(self, grammar = None, seed_value = None):
        Human.__init__(self, grammar, seed_value)
    
    def make_up_word(self):
        return "".join(sample(string.letters, randint(4, 8)))

    def communicate(self, meaning, child):
        words = []
        lhs_mapping = self.grammar.lhs_mapping()
        for i in xrange(len(meaning)):
            sub_meaning = meaning[i:i+1]
            if sub_meaning in lhs_mapping:
                left_child, _ = lhs_mapping[sub_meaning][0]
                word = left_child[0]
            else:
                word = self.make_up_word()
                self.grammar.append(\
                        PCFGLexicalRule(sub_meaning, (word,)))

            words.append(word)

        print "[%s] Communicate (%s,%s)" % \
                (datetime.today().time(), words, meaning)
        child.observe((words, meaning))
