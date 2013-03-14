'''
By:
Michael Cabot (6047262), Richard Rozeboom (6173292)

Creates a parse forest for a sentence given a corpus. The parse forest
is represented by a dictionary that maps a span [i,j) to a dictionary
mapping parents to their left and right child. Each parent represents
a partial derivation of the sentence. The probability of these parents
are kept in a separate dictionary mapping a node in a span to its
probability.
'''

import sys
import getopt
import ast
import extractPCFG

def makeForest(string, grammar):
    """Creates parse forest: all possible (sub)trees with probabilities
    for a sentence given a grammar. Unknown words will be replaced by 
    'XXXUNKNOWNXXX'.
    Arguments:
    string      - contains words separated by single whitespace
    grammar     - dictionary mapping rhs to [(P(rule_1), lhs_1), ..., (P(rule_n), lhs_n)]
    Return:
    parseForest - dictionary mapping span [i,j) to dictionary mapping parent to (left-child, right-child, k)
    probs       - dictionary mapping (node, i, j) to P(node)"""
    string = string.strip() # remove whitespace+\n @ start and end 
    parseForest = {} # condenses all possible parse tree
    probs = {} # holds probability of each entry in 'parseForest'
    words = string.split(' ')
    # initialize 
    for i in xrange(len(words)): # set terminals in triangle table
        word = words[i]
        for lhs in grammar.get(word, grammar.get('XXXUNKNOWNXXX', [])): 
            # entry at (i,i+1) is dictionary with key=lhs[1]=parent and value=(leftChild, rightChild, k)
            parseForest.setdefault((i,i+1), {})[lhs[1]] = (word, None, i+1) 
            probs[(lhs[1], i, i+1)] = lhs[0] # set probability of node
            extendUnary(lhs[1], grammar, parseForest, probs, i, i+1) # extend with unary rules            
            
    # expand
    for span in xrange(2, len(words)+1): # loop over spans
        for i in xrange(len(words)-span+1): # loop over sub-spans [i-k), [k-j)
            j = i+span
            for k in xrange(i+1, j): # k splits span [i,j)
                left = parseForest.get((i,k), {})
                right= parseForest.get((k,j), {})
                for x in left: # loop over nodes with span [i-k)
                    for y in right: # loop over nodes with span [k-j)
                        rhs = '~'.join([x, y])
                        for lhs in grammar.get(rhs, []): # expand trees
                            currentProb = lhs[0]*probs[(x,i,k)]*probs[(y,k,j)]
                            if currentProb > probs.get((lhs[1], i, j), -1):
                                probs[(lhs[1], i, j)] = currentProb
                                parseForest.setdefault((i,j), {})[lhs[1]] = (x, y, k)
                                #extendUnary(lhs[1], grammar, parseForest, probs, i, j) # extend with unary rules                               
    
    for node in dict(parseForest.get((0,len(words)), {})): # extend nodes with span [0,n) with unary rules
        extendUnary(node, grammar, parseForest, probs, 0, len(words))
    return parseForest, probs
                    
def extendUnary(node, grammar, parseForest, probs, i, j):
    """Finds entries that extend a tree with unary rules.
    Arguments:
    node        - current node to be extended with unary rules
    grammar     - dictionary mapping rhs to lhs
    parseForest - dictionary mapping span [i,j) to entries
    probs       - dictionary mapping (node, i, j) to P(node)
    i           - left index of span (inclusive)
    j           - right index of span (exclusive)"""
    for lhs in grammar.get(node, []):
        if lhs[1]==node: # prevent X->X
            continue
        currentProb = lhs[0] * probs[(node, i, j)]
        if currentProb > probs.get((lhs[1], i, j), -1):
            probs[(lhs[1], i, j)] = currentProb
            parseForest[(i,j)][lhs[1]] = (node, None, j)
            extendUnary(lhs[1], grammar, parseForest, probs, i, j)
                    
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:g:s:")
    except getopt.GetoptError as e:
        print e
        sys.exit(2) # command line error
        
    corpusFileName, grammarFileName = None, None
    testFileName = None
    for opt, arg in opts:
        if opt == "-c": # tree corpus
            corpusFileName = arg
        elif opt == "-g": # tree grammar
            grammarFileName = arg
        elif opt == "-s": # test sentences
            testFileName = arg
    # read/create grammar
    if not corpusFileName and not grammarFileName: # no tree corpus or grammar given
        print "Use '-c <file>' to give a tree corpus or '-g <file>' to give a grammar."
        sys.exit(2)
    elif corpusFileName: 
        if not extractPCFG.fileExists(corpusFileName):
            print "The tree corpus '%s' does not exist." %corpusFileName
            sys.exit(2)
        grammar = extractPCFG.createGrammar(corpusFileName) # create grammar from corpus
        if not grammarFileName: 
            grammarFileName = 'grammar_' + corpusFileName
            print "The grammar file is saved as: %s" %grammarFileName
        extractPCFG.saveToFile(grammar, grammarFileName) # save grammar
    elif grammarFileName:
        if not extractPCFG.fileExists(grammarFileName):
            print "The grammar '%s' does not exist." %grammarFileName
            sys.exit(2)
        try: # read grammar
            grammarFile = open(grammarFileName, 'r')
            grammar = ast.literal_eval(grammarFile.next().strip()) # read grammar from file
        except (SyntaxError, ValueError):
            print "The file %s does not contain a grammar." %grammarFileName
            sys.exit(2)    
    # read sentences
    if testFileName:
        if not extractPCFG.fileExists(testFileName):
            print "The file '%s' does not exist." %testFileName
            sys.exit(2)
        testFile = open(testFileName, 'r')
        for line in testFile: # read from file
            line = line.strip()
            print line
            parseForest, _ = makeForest(line.strip(), grammar)
            wordAmount = len(line.split(' '))
            nodes = parseForest.get((0, wordAmount), {})
            if 'TOP' in nodes:
                print 'TOP', nodes['TOP']
            else:
                print 'No parse'
    else:
        print "Enter a sentence. Type 'q' to quit."
        line = raw_input("Sentence: ")
        while line!='q': # read from stdin
            line = line.strip()
            parseForest, _ = makeForest(line, grammar)
            wordAmount = len(line.split(' '))
            nodes = parseForest.get((0, wordAmount), {})
            if 'TOP' in nodes:
                print 'TOP', nodes['TOP']
            else:
                print 'No parse'
                
            line = raw_input("Sentence: ")
    