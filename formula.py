import phrase

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

  def __repr__(self):
    return self.__str__()

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

  def __repr__(self):
    return self.__str__()

class FormulaSet:
  _formulas = []

  def __init__(self, formulas=[]):
    self._formulas=[]
    for f in formulas:
      self.append(f)

  def __getitem__(self,key):
    return self._formulas[key]
  
  def __setitem__(self, key, value):
    self._formulas[key] = value

  def __iter__(self):
    return self._formulas.__iter__()
  
  def __reversed__(self):
    return self._formulas.__reversed__()

  def __contains__(self, item):
    return self._formulas.__contains__(item)

  def __len__(self):
    return len(self._formulas)

  def index(self, item):
    return self._formulas.index(item)

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
    return str(self.formulas())

  def __repr__(self):
    return self.__str__()

class ArgumentMap:
  _amap = {1:1,2:2}

  def __init__(self, amap={}):
    self._amap = amap

  def map(self, arg):
    return self._amap[arg]

  def __str__(self):
    return str(self._amap)

  def __repr__(self):
    return self.__str__()

  @staticmethod
  def findMapping(a, b):
    if isinstance(a, phrase.PhraseNode):
      a = a.formulaset()
    if isinstance(b, phrase.PhraseNode):
      b = b.formulaset()
    map = {}
    for f_a in a:
      if f_a in b:
        f_b = b[b.index(f_a)]
        if isinstance(f_b, RelationFormula):
          map[f_a.arg1()] = f_b.arg1()
          map[f_a.arg2()] = f_b.arg2()
        elif isinstance(f_b, PropertyFormula):
          map[f_a.arg1()] = f_b.arg1()

    return ArgumentMap(map) if len(map)>0 else None
