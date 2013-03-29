from random import random, choice
from formula import *
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
    # No sample yet => exploration
    return choice(unseen_meaning)

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
        [(PropertyFormula, 1), (RelationFormula, 1, 2), (PropertyFormula, 2)],\
        [(PropertyFormula, 1), (RelationFormula, 2, 1), (PropertyFormula, 2)],\
        [(PropertyFormula, 1), (RelationFormula, 1, 1)] \
]

exploration_rate = 0.01
number_intentions = 10
number_iterations = 100

# dummy init parent
snake1 = FormulaSet([PropertyFormula('snake',1)])
bite12 = FormulaSet([RelationFormula('bite',1,2)])
pig1 = FormulaSet([PropertyFormula('pig',1)])
pig2 = FormulaSet([PropertyFormula('pig',2)])
lex1 = PCFGLexicalRule(snake1, ('fala'))
lex2 = PCFGLexicalRule(pig1, ('odu'))
lex2.cost = 10
lex3 = PCFGLexicalRule(bite12, ('kapa'))
parent = Parent(Grammar([lex1,lex2,lex3]))
# end dummy init parent

for iteration in range(number_iterations):
    print "[%d] Start iteration" % (iteration,)
    child = Child()
    
    for i in range(number_intentions):
        template = choice(templates)
        intention = FormulaSet()
        for placeholder in template:
            predicate = sample_lexicon(parent, placeholder[0], universal_meaning, 0.01)
            intention.append(placeholder[0](predicate, *placeholder[1:]))

        print "[%d] Communicate %d: %s" % (iteration, i, intention,)
        parent.communicate(intention, child)
    # Grow up
    parent = child.grow_up()
    print "[%d] Child grown up" % (iteration,)
