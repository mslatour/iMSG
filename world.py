from random import random, choice, seed
from formula import RelationFormula, PropertyFormula, FormulaSet
from datetime import datetime
from pcfg import PCFGLexicalRule
from human import Child, Parent


UNIVERSAL_MEANING = [\
    PropertyFormula('snake',1), \
    PropertyFormula('pig',1), \
    PropertyFormula('horse',1), \
    PropertyFormula('cat',1), \
    PropertyFormula('lizard',1), \
    RelationFormula('bite',1,2), \
    RelationFormula('insulted',1,2), \
    RelationFormula('tickled',1,2), \
    RelationFormula('noticed',1,2) \
]

TEMPLATES = [\
        [(PropertyFormula, 1), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
        [(PropertyFormula, 1), (RelationFormula, 2, 1), (PropertyFormula, 2)],\
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)], \
        [(PropertyFormula, 1), (RelationFormula, 1, 1)] \
]


class World:

    def __init__(self, exploration_rate, seed_value = None):
        self.exploration_rate = exploration_rate
        self.seed_value = seed_value
        seed(seed_value)

    def sample_lexicon(self, human, formula_class, 
                       exploration_rate = None):
        if not exploration_rate:
            exploration_rate = self.exploration_rate

        thresh = random()
        
        relevant_lexicon = [ rule for rule in human.grammar if \
                isinstance(rule, PCFGLexicalRule) and \
                isinstance(rule.lhs[0], formula_class)]

        # Normalized sum
        norm_sum = float(sum([1/float(rule.cost) for rule in relevant_lexicon]))
        norm_sum *= (1+exploration_rate)

        unseen_meaning = [f.predicate() for f in UNIVERSAL_MEANING \
                if isinstance(f, formula_class)]

        # Cumulative probability density
        cum_prob = 0

        # Sample from relevant_lexicon
        for rule in relevant_lexicon:
            if rule.lhs[0].predicate() in unseen_meaning:
                unseen_meaning.remove(rule.lhs[0].predicate())
            cum_prob += 1/(float(rule.cost)*norm_sum)
            if cum_prob >= thresh:
                return rule.lhs[0].predicate()
        if len(unseen_meaning) > 0:
            # No sample yet => explore unseen meanings
            return choice(unseen_meaning)
        else:
            # or if every meaning is explored, 
            # sample again without exploration
            return self.sample_lexicon(human, formula_class, 0)

    def iterated_learning(self, number_intentions, number_iterations): 
        # Init first (random) parent
        parent = Parent(seed_value = self.seed_value)
        for iteration in range(number_iterations):
            print "[%s] Start iteration %d" % \
                  (datetime.today().time(), iteration)
            child = Child(seed_value = self.seed_value)
            
            for _ in range(number_intentions):
                template = choice(TEMPLATES)
                intention = FormulaSet()
                for placeholder in template:
                    predicate = self.sample_lexicon(parent, placeholder[0])
                    intention.append(placeholder[0](predicate,
                                                    *placeholder[1:]))

                parent.communicate(intention, child)

            print "[%s] Child fully educated, grammar size: %d" % \
                    (datetime.today().time(), len(child.grammar))
            # Grow up
            parent = child.grow_up()
            print "[%s] Child grown up, end of iteration %d" % \
                    (datetime.today().time(), iteration)


if __name__ == '__main__':
    WORLD = World(0.2, 2)
    WORLD.iterated_learning(10, 25)
