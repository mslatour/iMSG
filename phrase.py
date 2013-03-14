class PhraseNode:
  _type = 0
  _left = None
  _leftAmap = None
  _right = None
  _rightAmap = None
  _formulaset = None
  _cost = 0

  def __init__(self, formulaset, cost=0):
    self._formulaset = formulaset
    self._cost = cost

  def isComplex(self):
    return self._type==0

  def cost(self):
    return self._cost

  def addLeft(self, left, amap=None):
    self._left = left
    self._leftAmap = amap
  
  def left(self):
    return self._left
  
  def addRight(self, right, amap=None):
    self._right = right
    self._rightAmap = amap
  
  def right(self):
    return self._right

  def formulaset(self):
    return self._formulaset
  
class ExemplarNode(PhraseNode):
  _type = 1

  def addString(self, string):
    self.addleft(string)

  def string(self):
    return self.left()
