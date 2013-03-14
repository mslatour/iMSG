"""
Michael Cabot & Sander Latour
"""
from human import Human

class Parent(Human):

    def __init__(self):
        Human.__init__(self)

    def communicate(self, meaning, child):
        pass