import BiDi
import re_learning
import AsD
import As1b
import sys,os
from timeit import default_timer as timer

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print ("No FILE")
        sys.exit()

    # check if file exists
    elif not os.path.isfile(sys.argv[1]):
        print ("File can't be loaded")
        sys.exit()
    path=sys.argv[1]

    heuristic=sys.argv[2]
    #set a number x : 0<x<1 to make it hard for zero heuristic else set x very very large number
    if heuristic=='learning':
        alltimes = timer()
        re_learning.run(path)
    elif heuristic =='destroy':
        alltimes = timer()
        AsD.run(path)
    elif heuristic =='oneblock':
        alltimes = timer()
        As1b.run(path)
    elif heuristic =='bidirectional':
        path2 = sys.argv[3]
        alltimes = timer()
        BiDi.run(path,path2)
    enda=timer()
    timea=enda-alltimes
    print (timea)