import AsB
import AsZ
import sys,os
from timeit import default_timer as timer

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print "No FILE"
        sys.exit()

    # check if file exists
    elif not os.path.isfile(sys.argv[1]):
        print "File can't be loaded"
        sys.exit()
    path=sys.argv[1]
    heuristic=sys.argv[2]
    #set a number x : 0<x<1 to make it hard for zero heuristic else set x very very large number
    if heuristic=='blocking':
        alltimes = timer()
        AsB.run(path)
    elif heuristic =='zero':
        alltimes = timer()
        time = sys.argv[3]
        AsZ.run(path,time)
    enda=timer()
    timea=enda-alltimes
    print timea