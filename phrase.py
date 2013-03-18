from formula import *

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

  def __init__(self, cost=0):
    self._cost = cost

  def __contains__(self, item):
    if isinstance(item, Formula):
      return item in self._formulaset
    elif isinstance(item, str):
      if self._left is not None:
        if item in self._left:
          return true
      if self._right is not None:
        if item in self._right:
          return true
      return false

  def isComplex(self):
    return self._type==0

  def cost(self):
    return self._cost

  def span(self):
    return self._span

  def updateSpan(self):
    self._span = 0
    if self._left is not None:
      self._span += self._left.span()
    if self._right is not None:
      self._span += self._right.span()

  def updateFormulaSet(self):
    fs = FormulaSet()
    if self._left is not None:
      l = self._left.formulaset()
      if self._leftAmap is not None:
        fs.append(l.applyArgumentMap(self._leftAmap))
      else:
        fs.append(l)
    if self._right is not None:
      r = self._right.formulaset()
      if self._rightAmap is not None:
        fs.append(r.applyArgumentMap(self._rightAmap))
      else:
        fs.append(r)
    self._formulaset = fs

  def addLeft(self, left, amap=None):
    self._left = left
    self._leftAmap = amap
    self.updateSpan()
    self.updateFormulaSet()

  def changeLeft(self,left, amap=None):
    phrase = PhraseNode(self.cost()+left.cost()+COST_SUBSTITUTION)
    if amap is None:
      amap = self._leftAmap
    phrase.addLeft(left, amap)
    phrase.addRight(self.right(),self._rightAmap)

  def changeLeftArgumentMap(self, amap):
    phrase = PhraseNode(self.cost()+COST_AMAP)
    phrase.addLeft(self.left(), amap)
    phrase.addRight(self.right(),self.rightArgumentMap())
    return phrase
  
  def changeRight(self, right, amap=None):
    phrase = PhraseNode(self.cost()+right.cost()+COST_SUBSTITUTION)
    if amap is None:
      amap = self._rightAmap
    phrase.addLeft(self.left(),self._leftAmap)
    phrase.addRight(right, amap)
  
  def changeRightArgumentMap(self, amap):
    phrase = PhraseNode(self.cost()+COST_AMAP)
    phrase.addLeft(self.left(), self.leftArgumentMap())
    phrase.addRight(self.right(),amap)
    return phrase

  def minimalChange(self, meaning, left, right):

    pass
  
  def left(self):
    return self._left
  
  def leftArgumentMap(self):
    return self._leftAmap
  
  def addRight(self, right, amap=None):
    self._right = right
    self._rightAmap = amap
    self.updateSpan()
    self.updateFormulaSet()
  
  def right(self):
    return self._right

  def rightArgumentMap(self):
    return self._rightAmap
  
  def formulaset(self):
    return self._formulaset

  def __str__(self):
    return "(%s %s %s)" % (self.formulaset(), self.left(),
                           self.right())

  def __repr__(self):
    return self.__str__()
  
class ExemplarNode(PhraseNode):
  _type = 1

  _string = None
  
  def __init__(self, formulaset, cost=0):
    PhraseNode.__init__(self, cost)
    self._formulaset = formulaset
  
  def __contains__(self, item):
    if isinstance(item, Formula):
      return item in self._formulaset
    elif isinstance(item, str):
      return item == self._string

  def addString(self, string):
    self._string = string

  def string(self):
    return self._string

  def __str__(self):
    return "(%s '%s')" % (self.formulaset(), self.string())

  def __repr__(self):
    return self.__str__()
