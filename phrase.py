from formula import *

COST_AMAP = 1
COST_MERGE = 2
COST_SUBSTITUTION = 3
COST_NEW = 4

class PhraseNode:
  _type = 0
  _left = None
  _left_amap = None
  _right = None
  _right_amap = None
  _meaning = None
  _cost = 0
  _span = 1

  @staticmethod
  def merge(left, right, meaning):
    left_map = ArgumentMap.find_mapping(left.meaning(), meaning)
    right_map = ArgumentMap.find_mapping(right.meaning(), meaning)
    cost = left.cost() + right.cost() + COST_MERGE
    pn = PhraseNode(cost)
    pn.add_left(left, left_map)
    pn.add_right(right, right_map)
    return pn

  def __init__(self, cost=0):
    self._cost = cost

  def __contains__(self, item):
    if isinstance(item, Formula):
      return item in self._meaning
    elif isinstance(item, str):
      if self._left is not None:
        if item in self._left:
          return true
      if self._right is not None:
        if item in self._right:
          return true
      return false

  def is_complex(self):
    return self._type==0

  def cost(self):
    return self._cost

  def span(self):
    return self._span

  def update_span(self):
    self._span = 0
    if self._left is not None:
      self._span += self._left.span()
    if self._right is not None:
      self._span += self._right.span()

  def update_formula_set(self):
    fs = FormulaSet()
    if self._left is not None:
      l = self._left.meaning()
      if self._left_amap is not None:
        fs.append(l.apply_argument_map(self._left_amap))
      else:
        fs.append(l)
    if self._right is not None:
      r = self._right.meaning()
      if self._right_amap is not None:
        fs.append(r.apply_argument_map(self._right_amap))
      else:
        fs.append(r)
    self._meaning = fs

  def add_left(self, left, amap=None):
    self._left = left
    self._left_amap = amap
    self.update_span()
    self.update_formula_set()

  def change_left(self,left, amap=None):
    phrase = PhraseNode(self.cost()+left.cost()+COST_SUBSTITUTION)
    if amap is None:
      amap = self._left_amap
    phrase.add_left(left, amap)
    phrase.add_right(self.right(),self._right_amap)

  def change_left_argument_map(self, amap):
    phrase = PhraseNode(self.cost()+COST_AMAP)
    phrase.add_left(self.left(), amap)
    phrase.add_right(self.right(),self.right_argument_map())
    return phrase
  
  def change_right(self, right, amap=None):
    phrase = PhraseNode(self.cost()+right.cost()+COST_SUBSTITUTION)
    if amap is None:
      amap = self._right_amap
    phrase.add_left(self.left(),self._left_amap)
    phrase.add_right(right, amap)
  
  def change_right_argument_map(self, amap):
    phrase = PhraseNode(self.cost()+COST_AMAP)
    phrase.add_left(self.left(), self.left_argument_map())
    phrase.add_right(self.right(),amap)
    return phrase

  def minimal_change(self, meaning, left, right):
    if self.meaning() == meaning:
      return self
    if self.left().meaning().primitive() != left.meaning().primitive():
      return self
    else:
      return None
  
  def left(self):
    return self._left
  
  def left_argument_map(self):
    return self._left_amap
  
  def add_right(self, right, amap=None):
    self._right = right
    self._right_amap = amap
    self.update_span()
    self.update_formula_set()
  
  def right(self):
    return self._right

  def right_argument_map(self):
    return self._right_amap
  
  def meaning(self):
    return self._meaning

  def leaves(self):
    left_leaves = self.left().leaves()
    right_leaves = self.right().leaves()
    return left_leaves + right_leaves

  def __str__(self):
    return "(%s [%s %s])" % (str(self.meaning()), str(self.left()),
                           str(self.right()))

  def __repr__(self):
    return self.__str__()

  def draw(self):
    try:
      from nltk import Tree
    except:
      print "This option requires the installation of nltk:"
      print "http://nltk.org/"
      return

    tree = self.get_tree()
    tree.draw()

  def get_tree(self):
    try:
      from nltk import Tree
    except:
      print "This option requires the installation of nltk:"
      print "http://nltk.org/"
      return

    return Tree(str(self.meaning()), 
           [self.left().get_tree(), self.right().get_tree()])
  
class ExemplarNode(PhraseNode):
  _type = 1

  _string = None
  
  def __init__(self, formulaset, cost=0):
    PhraseNode.__init__(self, cost)
    self._meaning = formulaset
  
  def __contains__(self, item):
    if isinstance(item, Formula):
      return item in self._meaning
    elif isinstance(item, str):
      return item == self._string

  def add_string(self, string):
    self._string = string

  def string(self):
    return self._string

  def leaves(self):
    return [self.string()]

  def __str__(self):
    return "(%s %s)" % (str(self.meaning()), self.string())

  def __repr__(self):
    return self.__str__()

  def get_tree(self):
    try:
      from nltk import Tree
    except:
      print "This option requires the installation of nltk:"
      print "http://nltk.org/"
      return

    return Tree(str(self.meaning()), [self.string()])
