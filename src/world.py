from random import random, choice, seed
from formula import RelationFormula, PropertyFormula, FormulaSet
from datetime import datetime
from pcfg import PCFGLexicalRule
from human import Child, Parent


UNIVERSAL_MEANING = [\
    PropertyFormula('cat',1), \
    PropertyFormula('fox',1), \
    PropertyFormula('goat',1), \
    PropertyFormula('horse',1), \
    PropertyFormula('lizard',1), \
    PropertyFormula('monkey',1), \
    PropertyFormula('moose',1), \
    PropertyFormula('mouse',1), \
    PropertyFormula('pig',1), \
    PropertyFormula('rat',1), \
    PropertyFormula('snake',1), \
    PropertyFormula('squirrel',1), \

    RelationFormula('bite',1,2), \
    RelationFormula('chased',1,2), \
    RelationFormula('insulted',1,2), \
    RelationFormula('kissed',1,2), \
    RelationFormula('liked',1,2), \
    RelationFormula('noticed',1,2), \
    RelationFormula('praised',1,2), \
    RelationFormula('shoved',1,2), \
    RelationFormula('slapped',1,2), \
    RelationFormula('tickled',1,2) \
]

TEMPLATES = [\
        [(PropertyFormula, 1), (RelationFormula, 1, 2), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
        [(PropertyFormula, 1), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
        [(PropertyFormula, 1), (RelationFormula, 2, 1), (PropertyFormula, 2)],\
        [(PropertyFormula, 1), (RelationFormula, 1, 2)], \
        [(PropertyFormula, 1), (RelationFormula, 2, 1)] \
]


class World:

    def __init__(self, exploration_rate, seed_value = None):
        self.exploration_rate = exploration_rate
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
        parent_costs = []
        child_costs = []
        child_grammar_sizes = []
        accuracies = []
        # Init first (random) parent
        parent = Parent()
        for iteration in xrange(number_iterations):
            print "[%s] Start iteration %d" % \
                  (datetime.today().time(), iteration)

            child = Child()
            
            temp_parent_cost = 0
            temp_child_cost = 0
            temp_child_grammar_size = 0
            temp_acc = 0
            for _ in xrange(number_intentions):
                template = choice(TEMPLATES)
                intention = FormulaSet()
                for placeholder in template:
                    predicate = self.sample_lexicon(parent, placeholder[0])
                    intention.append(placeholder[0](predicate,
                                                    *placeholder[1:]))

                parent.communicate(intention, child)

                temp_parent_cost += parent.cost
                temp_child_cost += child.cost
                temp_child_grammar_size += len(child.grammar)
                parent_rules = parent.used_rules
                child_rules = child.used_rules
                common_rules = len(set(parent_rules) & set(child_rules))
                temp_acc += 0.5 * (common_rules / len(parent_rules) + 
                                   common_rules / len(child_rules))

            parent_costs.append(temp_parent_cost / number_intentions)
            child_costs.append(temp_child_cost / number_intentions)
            child_grammar_sizes.append(temp_child_grammar_size / number_intentions)
            accuracies.append(temp_acc / number_intentions)

        print "[%s] Child fully educated, grammar size: %d" % \
                (datetime.today().time(), len(child.grammar))
        # Grow up
        parent = child.grow_up()
        print "[%s] Child grown up, end of iteration %d" % \
                (datetime.today().time(), iteration)
        print 'parent costs: \n%s' % parent_costs
        print 'child costs: \n%s' % child_costs
        print 'child grammar sizes: \n%s' % child_grammar_sizes
        print 'Accuracies: \n%s' % accuracies

if __name__ == '__main__':
    WORLD = World(0.2, 1)
    WORLD.iterated_learning(10, 100)
