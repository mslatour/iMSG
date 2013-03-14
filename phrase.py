class PhraseNode:
  _type = 0
  _left = None
  _right = None
  _formulaset = None

  def __init__(self, formulaset):
    self._formulaset = formulaset

  def isComplex(self):
    return self._type==0

  def addLeft(self, left):
    self._left = left
  
  def left(self):
    return self._left
  
  def addRight(self, right):
    self._right = right
  
  def right(self):
    return self._right

  def formulaset(self):
    return self._formulaset
  
class ExemplarNode(Phrase):
  _type = 1

  def addString(self, string):
    self.addleft(string)

  def string(self):
    return self.left()
