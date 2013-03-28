
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
  