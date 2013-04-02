from random import random, choice, seed
from formula import RelationFormula, PropertyFormula, FormulaSet
from datetime import datetime
from pcfg import PCFGLexicalRule
from human import Child, Parent

OPT_SAMPLE_MEANING = True

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

    RelationFormula('ate',1,2), \
    RelationFormula('bit',1,2), \
    RelationFormula('chased',1,2), \
    RelationFormula('insulted',1,2), \
    RelationFormula('kissed',1,2), \
    RelationFormula('liked',1,2), \
    RelationFormula('noticed',1,2), \
    RelationFormula('praised',1,2), \
    RelationFormula('punched',1,2), \
    RelationFormula('shoved',1,2), \
    RelationFormula('slapped',1,2), \
    RelationFormula('tickled',1,2) \
]

TEMPLATES = [\
#        [(PropertyFormula, 1), (RelationFormula, 1, 2), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
#        [(PropertyFormula, 1), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
#        [(PropertyFormula, 1), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
#        [(PropertyFormula, 1), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
#        [(PropertyFormula, 1), (RelationFormula, 2, 1), (PropertyFormula, 2)],\
#        [(PropertyFormula, 1), (RelationFormula, 1, 2)], \
        [(PropertyFormula, 1), (RelationFormula, 2, 1)] \
]

INTENTIONS = []

class World:

    def __init__(self, exploration_rate, seed_value = None):
        self.exploration_rate = exploration_rate
        seed(seed_value)

    def sample_lexicon(self, human, formula_class, 
                       exploration_rate = None):
        if exploration_rate == None:
            exploration_rate = self.exploration_rate

        thresh = random()
        
        relevant_lexicon = [ rule for rule in human.grammar if \
                isinstance(rule, PCFGLexicalRule) and \
                isinstance(rule.lhs[0], formula_class)]

        # Normalized sum
        norm_sum = float(sum([1/float(rule.cost) for rule in relevant_lexicon]))

        unseen_meaning = [f.predicate() for f in UNIVERSAL_MEANING \
                if isinstance(f, formula_class)]

        # Cumulative probability density
        cum_prob = 0

        relevant_lexicon = []
        # Sample from relevant_lexicon
        for rule in relevant_lexicon:
            if rule.lhs[0].predicate() in unseen_meaning:
                unseen_meaning.remove(rule.lhs[0].predicate())
            cum_prob += (1-exploration_rate)/(float(rule.cost)*norm_sum)
            if cum_prob >= thresh:
                return rule.lhs[0].predicate()
        if len(unseen_meaning) > 0:
            # No sample yet => explore unseen meanings
            return choice(unseen_meaning)
        else:
            # or if every meaning is explored, 
            # sample again without exploration
            self.exploration_rate = 0
            return self.sample_lexicon(human, formula_class, 0)

    def iterated_learning(self, number_intentions, number_iterations):
        parent_costs = []
        child_costs = []
        parent_sizes = []
        child_sizes = []
        accuracies = []
        # Init first (random) parent
        parent = Parent()
        for iteration in xrange(number_iterations):
            print "[%s] Start iteration %d" % \
                  (datetime.today().time(), iteration)

            parent_c = child_c = temp_acc = 0

            child = Child() # create new child
            
            for _ in xrange(number_intentions):
                if OPT_SAMPLE_MEANING:
                    template = choice(TEMPLATES)
                    intention = FormulaSet()
                    for placeholder in template:
                        predicate = self.sample_lexicon(parent, placeholder[0])
                        intention.append(placeholder[0](predicate,
                                                        *placeholder[1:]))
                else:
                    intention = choice(INTENTIONS)

                parent.communicate(intention, child)
                print "[COST:%d] parent: %f child: %f" % (iteration, parent.cost, child.cost)
                print child.grammar

                parent_c += parent.cost
                child_c += child.cost
                parent_rules = parent.used_rules
                child_rules = child.used_rules
                common_rules = len(set(parent_rules) & set(child_rules))
                temp_acc += 0.5 * (common_rules / len(parent_rules) + 
                              common_rules / len(child_rules))

            parent_costs.append(parent_c / number_intentions)
            child_costs.append(child_c / number_intentions)
            parent_sizes.append(len(parent.grammar))
            child_sizes.append(len(child.grammar))
            accuracies.append(temp_acc / number_intentions)

            print "[%s] Child fully educated, grammar size: %d" % \
                    (datetime.today().time(), len(child.grammar))
            # Grow up
            parent = child.grow_up()

            print "[%s] Child grown up, end of iteration %d" % \
                    (datetime.today().time(), iteration)
        print 'parent costs: \n%s' % parent_costs
        print 'child costs: \n%s' % child_costs
        print 'parent grammar sizes: \n%s' % parent_sizes
        print 'child grammar sizes: \n%s' % child_sizes
        grammar_diff = [parent_sizes[i]-child_sizes[i]
                             for i in xrange(number_iterations)]
        print 'grammar diff: \n%s' % grammar_diff
        print 'Accuracies: \n%s' % accuracies

if __name__ == '__main__':
    WORLD = World(1, 1)
    WORLD.iterated_learning(10, 30)
