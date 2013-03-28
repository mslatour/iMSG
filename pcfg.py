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


class Grammar:
  _rules = []

  def __init__(self, rules=[]):
    self._rules = rules

  def rules(self):
    return self._rules

  def extended_grammar(self, rhs, rhs_costs):
    extended_rules = {}
    for rule in self.rules():
      temp_rules = rule.extend(rhs, rhs_costs)
      for temp in temp_rules:
        if temp.cost() < extended_rules.get(temp, float('inf')):
          extended_rules[temp] = temp.cost()

    new_rules = self.create_rules(rhs[0], rhs[1]) # TODO always cheaper to create new rule?
    for rule in new_rules:
      if rule.cost() < extended_rules.get(rule, float('inf')):
        extended_rules[rule] = rule.cost()

    return Grammar(extended_rules.keys())

  def create_rules(self, left, right):
    rules = []
    # TODO
    # get all argument mappings for left and right
    # apply all combinations to union of left and right
    # create rule and add to rules
    # cost of new rule = left.cost() + right.cost() + COST_MERGE
    return rules

  def inverse(self):
    inverse = {}
    for rule in self.rules():
      inverse.setdefault(rule.rhs(), []).append((rule.lhs(), rule.cost()))

    return inverse

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

  def __getitem__(self,key):
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
