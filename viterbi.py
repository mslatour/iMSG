'''
By:
Michael Cabot (6047262), Richard Rozeboom (6173292)

Creates the most probable derivation of a sentence.
'''

import nltk.tree
import sys
import logging
import traceback
import getopt
import ast
import time
import CYK
import extractPCFG


def mostProbableTree(string, grammar):
    """Creates a parse forest an creates most probable
    parse tree.
    Arguments:
    string      - contains words separated by single whitespace
    grammar     - dictionary mapping rhs to [(P(rule_1), lhs_1), ..., (P(rule_n), lhs_n)]
    Return:
    nltk.Tree() -  most probable parse tree"""
    parseForest, probs = CYK.makeForest(string, grammar)
    j = len(string.split())
    if not (0,j) in parseForest:
        return None
    bestTree = viterbi(parseForest, probs, 0, j)
    unbinarizeAndReunarize(bestTree)
    return bestTree
    
def unbinarizeAndReunarize(tree):
    """Unbinarize and re-unarize a parse tree. Replace child
    that contains @ with its children. Extend node <A>%%%%%<B>
    by <A> --> <B>.
    Arguments:
    tree    - nltk parse tree"""
    i = 0
    while i < len(tree):
        child = tree[i]
        if not isinstance(child, str): 
            if "@" in child.node: # unbinarize
                tree.pop(i)
                tree[i:i] = list(child)
                i -= 1
            elif "%%%%%" in child.node: # re-unarize
                split = child.node.split("%%%%%")
                child.node = split[0]
                grandChildren = removeChildren(child)
                newChild = nltk.Tree(split[1], grandChildren)
                child.append(newChild)
                
            unbinarizeAndReunarize(child)
        i += 1

def removeChildren(tree):
    """Remove the children from parse tree
    Arguments:
    tree - nltk parse tree
    Return:
    list with children of tree"""
    children = []
    while len(tree)>0:
        children.append(tree.pop(0))
    return children
            
def viterbi(parseForest, probs, i, j, node='TOP', repeat=False):
    """Finds the most probable parse tree.
    Arguments:
    parseForest - dictionary that maps span [i,j) to grammar rules
    probs       - dictionary that maps entries in 'parseForest' to their probability
    i           - left index of span (inclusive)
    j           - right index of span (exclusive)
    node        - current node to be explored
    repeat      - keeps track of X->X rules
    Return:
    nltk.Tree() - most probable parse tree"""
    children = parseForest[(i,j)].get(node, None) # children=(leftChild, rightChild, k)
    if not children or repeat:
        return node
    repeat = children[0]==node and not children[1] #X->X only allowed once
    leftChild = viterbi(parseForest, probs, i, children[2], children[0], repeat)
    if children[1]: # if binary rule
        rightChild = viterbi(parseForest, probs, children[2], j, children[1], repeat)
        return nltk.Tree(node, [leftChild, rightChild])
    else: # if unary rule
        return nltk.Tree(node, [leftChild])


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:g:s:p:")
    except getopt.GetoptError as e:
        print e
        sys.exit(2) # command line error
        
    corpusFileName, grammarFileName = None, None
    testFileName, parsesFileName = None, None
    for opt, arg in opts:
        if opt == "-c": # tree corpus
            corpusFileName = arg
        elif opt == "-g": # tree grammar
            grammarFileName = arg
        elif opt == "-s": # test sentences
            testFileName = arg
        elif opt == "-p": # most probable trees for test sentences
            parsesFileName = arg
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
        if not parsesFileName:
            parsesFileName = "parses_"+testFileName
        
        if extractPCFG.fileExists(parsesFileName): # check if going to overwrite file
            print "Your are about to overwrite %s\n" \
            "y\t\t- To overwrite the file.\n" \
            "<new name>\t- To change the name." %parsesFileName
            input = raw_input()
            if input!='y':
                parsesFileName = input
        
        parsesFile = open(parsesFileName, 'w') 
        logging.basicConfig(filename='debug.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
        testFile = open(testFileName, 'r')
        print 'Start parsing at: %s' %time.asctime()
        start = time.clock() # start timing parsing time
        for line in testFile: # read from file
            try:
                bestTree = mostProbableTree(line, grammar)
                if bestTree:
                    parsesFile.write(bestTree.pprint(margin=100000000000000000000)+"\n") # large margin to counter pretty print
                else:
                    logging.warning("Could not parse: %s" %line)
                    parsesFile.write("(TOP Warning: could not parse.)\n")
            except Exception, e:
                print "Could not parse: %s" %line
                print traceback.format_exc()
                logging.exception("Could not parse: %s" %line)
                parsesFile.write("(TOP Error: see 'debug.log')\n")
                
        parsesFile.close()
        print 'Parsing duration: %f seconds' %(time.clock()-start)
        print 'End parsing at: %s' %time.asctime()
    else:
        print "Enter a sentence. Type 'q' to quit."
        line = raw_input("Sentence: ")
        while line!='q': # read from stdin
            bestTree = mostProbableTree(line, grammar)
            if bestTree:
                print bestTree
                bestTree.draw()
            else:
                print "Warning: could not parse"
            line = raw_input("Sentence: ")