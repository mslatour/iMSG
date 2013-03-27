from formula import *

COST_AMAP = 1
COST_MERGE = 2
COST_SUBSTITUTION = 3
COST_NEW = 4

class PCFGRule:
    """
    :param lhs - Left-hand-side of the rule (formulaset)
    :param rhs - Right-hand-side of the rule (tuple of formulasets)
    :param cost - Cost of using this rule
    :param amap - Argument mappings used to go from RHS to LHS
    """
    def __init__(self, rhs, cost, amap=None):
        self.rhs = rhs
        self.amap = amap if amap is not None else ArgumentMap()
        self.lhs = FormulaSet([x.apply_argument_map(self.amap) for x in rhs])
        self.cost = cost

    def __eq__(self, item):
        return (self.rhs == item.rhs and self.amap == item.amap)

    def __hash__(self):
        return hash((self.rhs,self.amap))

    def expand(self, rhs, costs):
        rule = self
        if len(self.rhs) != len(rhs):
            return []

        # Make the primitives fit
        for i in range(len(rhs)):
            if self.rhs[i].primitive() != rhs[i].primitive():
                # Copy current rhs into a list
                new_rhs = list(self.rhs)
                # Alter the rhs element
                new_rhs[i] = rhs[i]
                # Create a new PCFG rule
                rule = PCFGRule(tuple(new_rhs),\
                        rule.cost+COST_SUBSTITUTION+costs[i], self.amap)

        # Create set of possible argument mappings
        amapset = ArgumentMap.generate_amap_set(len(rhs))

        # Placeholder for possible PCFG rules
        pcfgs = []

        # Generate all argument variations
        for amap in amapset:
            cost = rule.cost + (0 if amap == self.amap else COST_AMAP)
            pcfgs.append(PCFGRule(rhs,cost,amap))

        return pcfgs
