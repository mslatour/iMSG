from itertools import product

class Formula:
    _predicate = None

    def __init__(self, predicate):
        self._predicate = predicate

    def predicate(self):
        return self._predicate

    def primitive(self):
        return Formula(self.predicate())

    def __eq__(self, other):
        return other.predicate() == self.predicate()

    def __lt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return NotImplemented

    def __ge__(self, other):
        return NotImplemented

    def __hash__(self):
        return hash(self.predicate())

    def __str__(self):
        return "(%s)" % (self.predicate(), )
    
    def __repr__(self):
        return self.__str__()

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

    def apply_argument_map(self, amap):
        return RelationFormula(self.predicate(), amap.map(self.arg1()), \
                amap.map(self.arg2()))

    def __str__(self):
        return "(%s %d %d)" % (self.predicate(), self.arg1(), self.arg2())

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return isinstance(other, RelationFormula) and \
                other.predicate() == self.predicate() and \
                other.arg1() == self.arg1() and \
                other.arg2() == self.arg2()
    
    def __hash__(self):
        return hash((self.predicate(), self.arg1(), self.arg2()))

class PropertyFormula(Formula):
    _arg1 = 1

    def __init__(self, predicate, arg1=1):
        Formula.__init__(self, predicate)
        self._arg1 = arg1

    def arg1(self):
        return self._arg1

    def apply_argument_map(self, amap):
        return PropertyFormula(self.predicate(), amap.map(self.arg1()))
    
    def __str__(self):
        return "(%s %d)" % (self.predicate(), self.arg1())

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return isinstance(other, PropertyFormula) and \
                other.predicate() == self.predicate() and \
                other.arg1() == self.arg1()

    def __hash__(self):
        return hash((self.predicate(), self.arg1()))

class FormulaSet:
    _formulas = []

    def __init__(self, formulas=[]):
        self._formulas=[]
        for f in formulas:
            self.append(f)

    def __add__(self, other):
        if isinstance(other, FormulaSet):
            return FormulaSet(self._formulas.__add__(other.formulas()))
        elif isinstance(other, list):
            return FormulaSet(self._formulas.__add__(other))
        else:
            return NotImplemented

    def __hash__(self):
        return hash(tuple(self._formulas))

    def __eq__(self, other):
        if not isinstance(other, FormulaSet):
            return False

        return len(set(self)&set(other)) == len(other)
    
    def __lt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return NotImplemented

    def __ge__(self, other):
        return NotImplemented

    def __getitem__(self, key):
        if isinstance(key, slice):
            return FormulaSet(self._formulas[key])
        else:
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

    def append(self, item):
        if isinstance(item, FormulaSet):
            for f in item:
                self.append(f)
        else:
            self._formulas.append(item)

    def primitive(self):
        fs = FormulaSet()
        for f in self:
            fs.append(f.primitive())
        return fs

    def formulas(self):
        return self._formulas

    def apply_argument_map(self, amap):
        formulaset = FormulaSet()
        for formula in self.formulas():
            formulaset.append(formula.apply_argument_map(amap))
        return formulaset

    def __str__(self):
        return str(self.formulas())

    def __repr__(self):
        return self.__str__()

class ArgumentMap:
    """
    :param amap - Argument map dictionary
    :const MAX_CARDINALITY - Maximum argument number
    """
    MAX_CARDINALITY = 2

    def __init__(self, amap={}):
        self.amap = {1:1, 2:2}
        for arg in amap:
            self.amap[arg] = amap[arg]

    def __eq__(self, item):
        return self.amap == item.amap

    def __hash__(self):
        return hash(tuple(zip(self.amap.keys(), self.amap.values())))

    def map(self, arg):
        return self.amap[arg]

    def __str__(self):
        return "ArgumentMap(%s)" % (str(self.amap), )

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def generate_amap_set(n):
        return product(*[[ArgumentMap(dict(zip(args, x))) \
            for x in product(args, repeat=ArgumentMap.MAX_CARDINALITY)] \
                for args in [range(1, ArgumentMap.MAX_CARDINALITY+1)]*n])

    @staticmethod
    def find_mapping(a, b):
        amap = {}
        for f_a in a:
            if f_a.primitive() in b.primitive():
                f_b = b[b.primitive().index(f_a)]
                if isinstance(f_b, RelationFormula):
                    amap[f_a.arg1()] = f_b.arg1()
                    amap[f_a.arg2()] = f_b.arg2()
                elif isinstance(f_b, PropertyFormula):
                    amap[f_a.arg1()] = f_b.arg1()

        return ArgumentMap(amap) if len(amap)>0 else None
