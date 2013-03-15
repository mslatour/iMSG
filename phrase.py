COST_AMAP = 1
COST_MERGE = 2
COST_SUBSTITUTION = 3
COST_NEW = 4

class PhraseNode:
  _type = 0
  _left = None
  _leftAmap = None
  _right = None
  _rightAmap = None
  _formulaset = None
  _cost = 0
  _span = 1

  def __init__(self, cost=0, span=1):
    self._cost = cost
    self._span = span

  def isComplex(self):
    return self._type==0

  def cost(self):
    return self._cost

  def span(self):
    return self._span

  def createFormulaSet(self):
    fs = FormulaSet()
    if self._left is not None:
      if self._leftAmap is not None:
        fs.addFormula(self._left.applyArgumentMap(self._leftAmap))
      else:
        fs.addFormula(self._left)
    if self._right is not None:
      if self._rightAmap is not None:
        fs.addFormula(self._right.applyArgumentMap(self._rightAmap))
      else:
        fs.addFormula(self._right)
    return fs

  def addLeft(self, left, amap=None):
    self._left = left
    self._leftAmap = amap
    self.createFormulaSet()
  
  def left(self):
    return self._left
  
  def addRight(self, right, amap=None):
    self._right = right
    self._rightAmap = amap
    self.createFormulaSet()
  
  def right(self):
    return self._right

  def formulaset(self):
    return self._formulaset
  
class ExemplarNode(PhraseNode):
  _type = 1
  
  def __init__(self, formulaset, cost=0):
    PhraseNode.__init__(cost, 1)
    self._formulaset = formulaset

  def addString(self, string):
    self.addleft(string)

  def string(self):
    return self.left()
