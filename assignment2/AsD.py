import  heapq
import destroy as destroy
from timeit import default_timer as timer

def run(path):
    # array of all cars that thier length is 2
    smallcars = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}

    def astarblocking():
        #using A* to calculate the optimal path to win
        #if theres no solution return None if there solution return the node that contains all the needed data
        #admisable hueristic
        while len(pqueue):
            # pop the node with lowest cost estimate by value =depth of node + min distance from car x to the exit + number of steps needed to clean the road for car x
            node = heapq.heappop(pqueue)
            # expand to all posible children (boards after 1 move)
            for move in node.get_movesX():
                child = node.moveforX(move[0], move[1],move[2])
                # making sure were not going over a visited state
                if child.get_hash() not in visited:
                    # add state to visited list and to the priority queue
                    visited[child.get_hash()] = [node.vehicles, move]
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
    f = open("destroy_output.txt", "w+")
    problems = open(path, "r")
    #reading one line (1 puzzle)
    for line in problems:
        root = destroy.load_file(line)
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
                    if visited[node][1][2] != 0:
                        moves.append(['delete', visited[node][1][2]])
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
            #reversing moves because we start adding moves in reverse order so we reverse it back in the end
            moves.reverse()
            numpuzzle += 1
            f.write("\npuzzle #%d" % (numpuzzle))
            f.write("\nmoves: ")
            for move in moves:
                f.write(" %s%s, " % ((move[0]),(move[1])))
            f.write("\nExplored %d states in %f seconds" % (len(visited), (end - start)))
            f.write("\nSolved in %d moves" % (len(moves)))
        # start visualisation if wanted
    f.close()
