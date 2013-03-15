class Formula:
  _predicate = None

  def __init__(self, predicate):
    self._predicate = predicate

  def predicate(self):
    return self._predicate

  def __eq__(self, other):
    return other.predicate() == self.predicate()

  def __lt__(self, other):
    return NotImplemented

  def __le__(self, other):
    return NotImplemented

  def __ne__(self, other):
    return other.predicate() != self.predicate()

  def __gt__(self, other):
    return NotImplemented

  def __ge__(self, other):
    return NotImplemented

  def __hash__(self):
    return int("".join([str(ord(c)) for c in self.predicate()]))

class RelationFormula(Formula):
  _arg1 = 1
  _arg2 = 2

  def __init__(self, predicate, arg1=1, arg2=2):
    Formula.__init__(self, predicate)
    self._arg1 = arg1
    self._arg2 = arg2

  def arg1(self):
    return self._arg1

  def arg2(self):
    return self._arg2

  def applyArgumentMap(self, amap):
    return RelationFormula(self.predicate(), amap.map(self.arg1()),\
        amap.map(self.arg2()))

  def __str__(self):
    return "(%s %d %d)" % (self.predicate(), self.arg1(), self.arg2())

class PropertyFormula(Formula):
  _arg1 = 1
  def __init__(self, predicate, arg1=1):
    Formula.__init__(self, predicate)
    self._arg1 = arg1

  def arg1(self):
    return self._arg1

  def applyArgumentMap(self, amap):
    return PropertyFormula(self.predicate(), amap.map(self.arg1()))
  
  def __str__(self):
    return "(%s %d)" % (self.predicate(), self.arg1())

class FormulaSet:
  _formulas = []

  def __init__(self, formulas=[]):
    self._formulas=[]
    for f in formulas:
      self.append(f)

  def append(self, formulaOrFormulaSet):
    if isinstance(formulaOrFormulaSet,FormulaSet):
      for f in formulaOrFormulaSet.formulas():
        self.append(f)
    else:
      self._formulas.append(formulaOrFormulaSet)

  def formulas(self):
    return self._formulas

  def applyArgumentMap(self, amap):
    formulaset = FormulaSet()
    for formula in self.formulas():
      formulaset.append(formula.applyArgumentMap(amap))
    return formulaset

  def __str__(self):
    s = ""
    for formula in self.formulas():
      s += str(formula)
    return s

class ArgumentMap:
  _amap = {1:1,2:2}

  def __init__(self, amap={}):
    for arg in amap:
      self._amap[arg] = amap[arg]

  def map(self, arg):
    return self._amap[arg]

  @staticmethod
  def find_mapping(a, b):
    if a.predicate()!=b.predicate or\
       a.__class__.__name__!=b.__class__.__name__:
      return None
    if isinstance(a, RelationFormula):
      map[a.arg1()] = b.arg1()
      map[a.arg2()] = b.arg2()
      return ArgumentMap(map)
    elif isinstance(a, PropertyFormula):
      map[a.arg1()] = b.arg1()
      return ArgumentMap(map)

    return None
