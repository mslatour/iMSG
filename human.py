from pcfg import *
import viterbi

class Human:
    """
    :param grammar
    """
    def __init__(self, grammar = None):
        self.grammar = grammar if grammar is not None else Grammar()
        self.cost = 0

    def get_last_cost(self):
        return self.cost


class Child(Human):

    def __init__(self, grammar = None):
        Human.__init__(self, grammar)
        
    def observe(self, (words, meaning)):
        parse_forest, costs = viterbi.make_forest(words, meaning, self.grammar)
        correct_parse_cost = None
        span = (0, len(words))
        for top in parse_forest[span]: # find parse that matches the meaning
            if top == meaning:
                correct_parse_cost = costs[(top,)+span]
                reinforced_rules = self.reinforce(parse_forest, costs, top, span)
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


class Parent(Human):
    def __init__(self, grammar = None):
        Human.__init__(self, grammar)

                
    def communicate(self, meaning, child):
        pass

