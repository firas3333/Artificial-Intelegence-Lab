import  heapq
import reinforcmentL
from timeit import default_timer as timer
import learningUtils
def run(path):
    # array of all cars that thier length is 2
    smallcars = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
    #loading file (takes one line (one puzzle) per call)


    def astarblocking():
        #using A* to calculate the optimal path to win
        #if theres no solution return None if there solution return the node that contains all the needed data
        #admisable hueristic
        # training_inputs.append(np.array([None, root.vehicles, root.value]))
        # labels.append(1)
        a = 0

        while len(pqueue):
            # pop the node with lowest cost estimate by value =depth of node + min distance from car x to the exit + number of steps needed to clean the road for car x
            node = heapq.heappop(pqueue)
            # expand to all posible children (boards after 1 move)
            for move in node.get_moves():
                child = node.move(move[0], move[1],allpossiblemove)
                # making sure were not going over a visited state
                if child.get_hash() not in visited:
                    # add state to visited list and to the priority queue
                    visited[child.get_hash()] = [node.vehicles, move]
                    # print (allpossiblemove[tuple(move)])
                    if move in opte:
                        allpossiblemove[tuple(move)]=allpossiblemove[tuple(move)]-1
                    else:
                        allpossiblemove[tuple(move)]=allpossiblemove[tuple(move)]+1
                    heapq.heappush(pqueue, child)
                #move[0]=index of the car we moved in self.vehicles(cars)
                #checking that this was the last move we need (after we get x to the correct place we dont need to do anything else
                if node.vehicles[move[0]].id=='X':
                    #checks if goal vehicle is in this state
                    if child.win():
                        #return the node that has the winning state
                        return child.get_hash()


    alltimes=timer()
    # load board from file
    path = path
    #puzzles counter
    numpuzzle=0
    #creating file for A star results
    f = open("reinforcment_learning.txt", "w+")
    problems = open(path, "r")
    pathformoves = "possiblemoves"
    pathforopt = "optimalsolution"
    optsols = learningUtils.loadoptsol(pathforopt)
    allpossiblemove, movesclass = learningUtils.loadallmoves(pathformoves)
    #reading one line (1 puzzle)
    iopt=0
    for line in problems:
        id=0
        cars = dict()
        visitedmove=[]
        root = reinforcmentL.load_file(line)
        opte=[]
        for car in root.vehicles:
            cars[car.id]=id
            id+=1
        optimalsolution=optsols[iopt]
        strings=optimalsolution.split(',')
        for i in range(len(strings)):
            if strings[i] not in visitedmove:
                visitedmove.append(strings[i])
                if strings[i][1]=='R' or strings[i][1]=='D':
                    direct=1
                else:
                    direct=-1
                opte.append([cars[strings[i][0]],direct])
        # initialize visited dictionary
        visited = dict()
        #taking list of object of class vehicles in this state (self.vehicles(vihcle(x,2,1,H),vehicle(b,3,4,V)....)
        visited[root.get_hash()] = None
        # initialize priority queue
        pqueue = list()
        #pushing the root state (the puzzle as we loaded it before any move)
        heapq.heappush(pqueue, root)
        # when we started solving a puzzle
        start = timer()
        # going to A* algorythm node= object which has the solution and any other needed params
        training_inputs = []
        labels =[]
        node = astarblocking()

        # when we finish solving the puzle
        end = timer()
        moves = []
        #if node==None it means algorythm couldnt find solution
        if node==None:
            f.write("\npuzzle #%d" % (numpuzzle))
            f.write("\n no possible solution ")
            f.write("\nExplored %d states in %f seconds "% (len(visited), (end - start)))
            print ("couldnt find solution for puzzle #%d"%(numpuzzle))
            numpuzzle+=1
        else:
            #moves are stored in this format [8,1],[6,-1][index,move] meaning index=index of the car in the vehicles array and 1/-1=R/L or U/D depinding on orientation
            #this loop takes all the moves stored in the node returned from astarblocking() and turns them into a format of [X,R],[O,L]
            while visited[node] is not None:
                if visited[node][0][visited[node][1][0]].orientation == 'H':
                    if visited[node][1][1] == 1:
                        moves.append([visited[node][0][visited[node][1][0]].id, 'R'])
                        node = visited[node][0]
                    elif visited[node][1][1] == -1:
                        moves.append([visited[node][0][visited[node][1][0]].id, 'L'])
                        node = visited[node][0]
                elif visited[node][0][visited[node][1][0]].orientation == 'V':
                    if visited[node][1][1] == 1:
                        moves.append([visited[node][0][visited[node][1][0]].id, 'D'])
                        node = visited[node][0]
                    elif visited[node][1][1] == -1:
                        moves.append([visited[node][0][visited[node][1][0]].id, 'U'])
                        node = visited[node][0]
                i=0

                for move in training_inputs:
                    if visited[node]!=None and move[0]!=None:
                            if move[0][0]==visited[node][1][0] and  move[0][1]==visited[node][1][1]:
                                if move[1]==node:
                                    labels[i]=1
                    i+=1
            # movesss=[]
            # for m in training_inputs:
            #     movesss.append(np.array(m[0]))
            # perceptron.train(movesss, labels)
            # inputs = np.array([4, 1])
            # print(perceptron.predict(inputs))
            # print(len(training_inputs))
            # ppn = pleaseeee.perceptron(eta=0.1, n_iter=10)
            # ppn.fit(training_inputs, labels)
            # print( ppn.predict([[3,2],None,4]))

            #reversing moves because we start adding moves in reverse order so we reverse it back in the end
            moves.reverse()
            numpuzzle += 1
            f.write("\npuzzle #%d" % (numpuzzle))
            f.write("\nmoves: ")
            for move in moves:
                f.write(" %s%s, " % ((move[0]),(move[1])))
            f.write("\nExplored %d states in %f seconds" % (len(visited), (end - start)))
            f.write("\nSolved in %d moves" % (len(moves)))
            iopt+=1
        # start visualisation if wanted
    f.close()

