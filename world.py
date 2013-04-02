from random import random, choice
from formula import *
from datetime import datetime
from pcfg import *
from human import *

def sample_lexicon(human, formula_class, universal_meaning, exploration_rate):
    thresh = random()
    
    relevant_lexicon = [ rule for rule in human.grammar if \
            isinstance(rule, PCFGLexicalRule) and \
            isinstance(rule.lhs[0], formula_class)]

    # Normalized constant
    Z = float(sum([1/float(rule.cost) for rule in relevant_lexicon]))
    Z *= (1+exploration_rate)

    unseen_meaning = [f.predicate() for f in universal_meaning \
            if isinstance(f, formula_class)]

    # Cumulative probability density
    p = 0

    # Sample from relevant_lexicon
    for rule in relevant_lexicon:
        if rule.lhs[0].predicate() in unseen_meaning:
            unseen_meaning.remove(rule.lhs[0].predicate())
        p += 1/(float(rule.cost)*Z)
        if p >= thresh:
            return rule.lhs[0].predicate()
    if len(unseen_meaning) > 0:
        # No sample yet => explore unseen meanings
        return choice(unseen_meaning)
    else:
        # or if every meaning is explored, sample again without no exploration
        return sample_lexicon(human, formula_class, universal_meaning, 0)

universal_meaning = [\
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

templates = [\
#        [(PropertyFormula, 1), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
#        [(PropertyFormula, 1), (RelationFormula, 2, 1), (PropertyFormula, 2)],\
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

exploration_rate = 0.2
number_intentions = 10
number_iterations = 100

# Init first (random) parent
parent = Parent()
for iteration in range(number_iterations):
    print "[%s] Start iteration %d" % (datetime.today().time(), iteration)
    child = Child()
    
    for i in range(number_intentions):
        template = choice(templates)
        intention = FormulaSet()
        for placeholder in template:
            predicate = sample_lexicon(parent, placeholder[0], \
                    universal_meaning, exploration_rate)
            intention.append(placeholder[0](predicate, *placeholder[1:]))
        parent.communicate(intention, child)
    cost = sum([rule.cost for rule in child.grammar])
    print "[%s] Child fully educated, grammar size: %d, grammar costs: %d" % \
            (datetime.today().time(), len(child.grammar), cost)
    # Grow up
    parent = child.grow_up()
    print "[%s] Child grown up, end of iteration %d" % \
            (datetime.today().time(), iteration)
