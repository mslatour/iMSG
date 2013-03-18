from formula import *

observations = [\
  [('snake',),FormulaSet([PropertyFormula('snake',1)])], \
  [('pig',),FormulaSet([PropertyFormula('pig',1)])], \
  [('snake','bit','pig'),FormulaSet([PropertyFormula('snake',1),RelationFormula('bit',2,1),PropertyFormula('pig',1)])], \
  [('snake','bit','pig'),FormulaSet([PropertyFormula('snake',1),RelationFormula('bit',1,2),PropertyFormula('pig',2)])], \
]
