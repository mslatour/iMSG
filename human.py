# getLastCosts
# data structuur (token storage)
# stringToPhrases
"""
Michael Cabot & Sander Latour
"""

class Human:
  _lexicon = {}

  def __init__(self):
    self.cost = 0

  def lexicon(self):
    return self._lexicon

  def add_to_lexicon(self, meaning, string):
    self._lexicon[meaning] = string

  def verbalize(self, meaning):
    if meaning in self._lexicon:
      return self._lexicon[meaning]
    try:
      s = ""
      for m in meaning:
        s += self.verbalize(m)
      return s
    except TypeError:
      return ""

  def get_last_cost(self):
    return self.cost
