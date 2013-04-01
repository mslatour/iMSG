from formula import FormulaSet, ArgumentMap

COST_AMAP = 0.05
COST_MERGE = 1.5
COST_SUBSTITUTION = 0.1
COST_NEW = 1.0
REINFORCEMENT_RATE = 0.1
DISCOURAGING_RATE = 0.1

class PCFGRule:
    """
    :param lhs - Left-hand-side of the rule (formulaset)
    :param rhs - Right-hand-side of the rule (tuple of formulasets)
    :param cost - Cost of using this rule
    :param amap - Argument mappings used to go from RHS to LHS
    """
    def __init__(self, rhs, cost, amap=None):
        self.rhs = rhs
        self.amap = amap if amap != None else tuple([ArgumentMap()]*len(rhs))
        self.lhs = FormulaSet([x.apply_argument_map(self.amap[i]) \
                for i, x in enumerate(rhs)])
        self.cost = cost

    def __eq__(self, item):
        return (self.lhs == item.lhs and self.rhs == item.rhs)

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def __str__(self):
        return "%s --> %s [%f]" % (self.lhs, self.rhs, self.cost)

    def __repr__(self):
        return str(self)

    def reinforce(self):
        self.cost *= (1-REINFORCEMENT_RATE)

    def discourage(self):
        self.cost += DISCOURAGING_RATE

    def expand(self, rhs, costs):
        rule = self
        if len(self.rhs) != len(rhs):
            return []

        # Make the primitives fit
        for i in range(len(rhs)):
            if self.rhs[i].primitive() != rhs[i].primitive():
                # Copy current rhs into a list
                new_rhs = list(rule.rhs)
                # Alter the rhs element
                new_rhs[i] = rhs[i]
                # Create a new PCFG rule
                rule = PCFGRule(tuple(new_rhs), \
                        rule.cost+COST_SUBSTITUTION+costs[i], self.amap)

        # Create set of possible argument mappings
        amapset = ArgumentMap.generate_amap_set(len(rhs))

        # Placeholder for possible PCFG rules
        pcfgs = []

        # Generate all argument variations
        for amap in amapset:
            cost = rule.cost + (0 if amap == self.amap else COST_AMAP)
            pcfgs.append(PCFGRule(rhs, cost, amap))

        return pcfgs

class PCFGLexicalRule(PCFGRule):
    """
    :param lhs - Left-hand-side of the rule (formulaset)
    :param rhs - Right-hand-side of the rule (tuple of one string)
    :param cost - Cost of using this rule
    """

    def __init__(self, lhs, rhs, cost=COST_NEW):
        self.lhs = lhs
        self.rhs = rhs
        self.cost = cost

    def expand(self, rhs, costs):
        return [self]

class Grammar:
    _rules = []

    def __init__(self, rules=[]):
        self._rules = rules

    def rules(self):
        return self._rules
        
    def expanded_grammar(self, rhs, rhs_costs):
        best_rules = []
        best_cost = float('inf')
        max_sub_cost = len(rhs) * COST_SUBSTITUTION + \
                       sum(i for i in rhs_costs)
        for rule in self.rules():
            if len(rule.rhs) != len(rhs):
                continue

            if rule.cost + max_sub_cost < best_cost:
                best_rules = [rule]
                best_cost = rule.cost
            elif rule.cost <= best_cost + max_sub_cost:
                best_rules.append(rule)
                if rule.cost < best_cost:
                    best_cost = rule.cost
        
        expanded_rules = {}
        for rule in best_rules:
            temp_rules = rule.expand(rhs, rhs_costs)
            for temp in temp_rules:
                if temp.cost < expanded_rules.get(temp, float('inf')):
                    expanded_rules[temp] = temp.cost

        rule_gen = self.create_rule_generator(rhs, rhs_costs)
        for rule in rule_gen:
            if rule.cost < expanded_rules.get(rule, float('inf')):
                expanded_rules[rule] = rule.cost

        return Grammar(expanded_rules.keys())

    def create_rule_generator(self, rhs, costs):
        amapset = ArgumentMap.generate_amap_set(len(rhs))
        return (PCFGRule(rhs, sum(costs)+COST_MERGE, amap) for amap in amapset)

    def rhs_mapping(self):
        mapping = {}
        for rule in self.rules():
            mapping.setdefault(rule.rhs, []).append((rule.lhs, rule.cost))

        return mapping

    def lhs_mapping(self):
        mapping = {}
        for rule in self.rules():
            mapping.setdefault(rule.lhs, []).append((rule.rhs, rule.cost))

        return mapping

    def __add__(self, other):
        if isinstance(other, Grammar):
            return Grammar(self.rules() + other.rules())
        else:
            return NotImplemented

    def __eq__(self, other):
        return set(self.rules()) == set(other.rules())

    def __lt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return NotImplemented

    def __ge__(self, other):
        return NotImplemented

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Grammar(self.rules()[key])
        else:
            return self.rules()[key]
  
    def __setitem__(self, key, value):
        self._rules[key] = value

    def __iter__(self):
        return self._rules.__iter__()
  
    def __reversed__(self):
        return self._rules.__reversed__()

    def __contains__(self, item):
        return self._rules.__contains__(item)

    def __len__(self):
        return len(self._rules)

    def index(self, item):
        return self._rules.index(item)

    def append(self, item):
        self._rules.append(item)

    def extend(self, item):
        self._rules.extend(item)

    def __str__(self):
        return "Grammar%s" % self.rules()

    def __repr__(self):
        return str(self)
