from pcfg import PCFGLexicalRule, Grammar
from random import sample, randint
from datetime import datetime
import string
import viterbi


class Child:

    def __init__(self, grammar = None):
        if grammar == None:
            self.grammar = Grammar()
        else:
            self.grammar = grammar

        self.cost = 0
        self.used_rules = []
        
    def observe(self, (words, meaning)):
        parse_forest, costs = viterbi.make_forest(words, meaning, self.grammar)
        correct_parse_cost = None
        span = (0, len(words))
        for top in parse_forest[span]: # find parse that matches the meaning
            if top == meaning:
                correct_parse_cost = costs[(top,)+span]
                self.cost = correct_parse_cost
                reinforced_rules = self.reinforce(parse_forest, costs, 
                                                  top, span)
                self.used_rules = reinforced_rules
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
        return Parent(self.grammar)


class Parent:

    def __init__(self, grammar = None):
        if grammar == None:
            self.grammar = Grammar()
        else:
            self.grammar = grammar

        self.cost = 0
        self.used_rules = []
    
    def make_up_word(self):
        return "".join(sample(string.letters, randint(4, 8)))

    def communicate(self, meaning, child):
        # create words that correspond to meaning
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

        # find parse that matches the meaning
        parse_forest, costs = viterbi.make_forest(words, meaning, self.grammar)
        span = (0, len(words))
        for top in parse_forest[span]:
            if top == meaning:
                self.cost = costs[(top,)+span]
                rules = viterbi.get_rules(parse_forest, costs, top, span)
                self.used_rules = rules
                break

        print "[%s] Communicate (%s,%s)" % \
                (datetime.today().time(), words, meaning)
        child.observe((words, meaning))
