class Human:
    """
    :param grammar
    """
    def __init__(self, grammar = None):
        self.grammar = grammar is grammar is not None else Grammar()

    def get_last_cost(self):
        return self.cost


class Child(Human):

    def observe(self, (words, meaning)):
        pass
            
    def reinforce_and_discourage(self, words, meaning):
        parse_forest, costs = viterbi.make_forest(words, meaning, self.grammar)
        correct_parse_cost = None
        span = (0,len(words))
        for top in parseForest[span]:
            if top==meaning:
                correct_parse_cost = costs[(top,)+span]
                self.reinforce(parse_forest, costs, top, span)
                break

        for top in parseForest[span]:
            if top==meaning:
                continue

            if costs[(top,)+span] < correct_parse_cost:
                self.discourage(parse_forest, costs, top, span)

    def reinforce(self, parse_forest, costs, top, span):
        rules = get_rules(parse_forest, costs, top, span)
        for rule in rules:
            rule.reinforce()

    def discourage(self, parse_forest, costs, top, span):
        rules = get_rules(parse_forest, costs, top, span)
        for rule in rules:
            rule.discourage()

    def grow_up(self):
        return Parent(self.grammar)

class Parent(Human):

    def communicate(self, meaning, child):

        pass
