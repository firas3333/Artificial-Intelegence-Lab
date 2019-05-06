import  heapq
from timeit import default_timer as timer
import bidirectional as bidirectional
from timeit import default_timer as timer

def run(path,path2):
    # array of all cars that thier length is 2
    smallcars = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
    def astarblocking():
        #using A* to calculate the optimal path to win
        #if theres no solution return None if there solution return the node that contains all the needed data
        #admisable hueristic
        while len(pqueue)and len(pqueue2):
            # pop the node with lowest cost estimate by value =depth of node + min distance from car x to the exit + number of steps needed to clean the road for car x
            node = heapq.heappop(pqueue)

            node2 = heapq.heappop(pqueue2)

            counter = 0
            visitid=[]
            for car2 in node2.vehicles:
                count2 = 0
                for car1 in node.vehicles:
                    if car1.id == car2.id :
                        visitid.append(car1)
                        count2 += 1
                counter += 1
            node.vehicles = list(node.vehicles)
            node.vehicles = visitid
                        # (node2.vehicles[counter], node2.vehicles[count2]) = (node2.vehicles[count2], node2.vehicles[counter])
            node.vehicles = tuple(node.vehicles)

                        # tmp = child.get_hash()[counter]
                        # child.get_hash()[counter]=car2
                        # child.get_hash()[count2]=tmp


            # expand to all posible children (boards after 1 move)
            movees=zip(node.get_moves(),node2.get_moves())

            for move,move2 in movees:
                child = node.move(move[0], move[1])
                child2 = node2.move(move2[0], move2[1])
                # print(child.get_hash())
                # print(child2.get_hash())
                # print('---------------------------')
                # making sure were not going over a visited state
                if child.get_hash() not in visited:
                    # add state to visited list and to the priority queue
                    visited[child.get_hash()] = [node.vehicles, move]
                    heapq.heappush(pqueue, child)
                if child2.get_hash() not in visited2:
                    # add state to visited list and to the priority queue
                    visited2[child2.get_hash()] = [node2.vehicles, move2]
                    heapq.heappush(pqueue2, child2)
                # print(child.get_hash())
                # print(child2.get_hash())
                # print('---------------------------')

                if child.get_hash()in visited2:
            # if v == len(node.vehicles):
            #         print(v)
            #         print(len(node.vehicles))
            #         nodes=child.get_hash()
            #         nodes2=child2.get_hash()
                    child2.vehicles,move2=visited2[child.get_hash()]
                    child2 = child2.move(move2[0], move2[1])
                    return child.get_hash(),child2.get_hash()
                #move[0]=index of the car we moved in self.vehicles(cars)
                #checking that this was the last move we need (after we get x to the correct place we dont need to do anything else

    alltimes=timer()
    # load board from file
    path = path
    path2 = path2
    #puzzles counter
    numpuzzle=0
    #creating file for A star results
    f = open("bidirectionalOutP.txt", "w+")
    problems1 = open(path, "r")
    problems2 = open(path2, "r")
    problems=zip(problems1,problems2)
    #reading one line (1 puzzle)
    for line,line2 in problems:
        root = bidirectional.load_file(line)
        root2 = bidirectional.load_file(line2)
        # initialize visited dictionary
        visited = dict()
        visited2 = dict()
        #taking list of object of class vehicles in this state (self.vehicles(vihcle(x,2,1,H),vehicle(b,3,4,V)....)
        visited[root.get_hash()] = None
        visited2[root2.get_hash()] = None
        # initialize priority queue
        pqueue = list()
        pqueue2 = list()
        #pushing the root state (the puzzle as we loaded it before any move)
        heapq.heappush(pqueue, root)

        heapq.heappush(pqueue2, root2)
        # when we started solving a puzzle
        start = timer()
        # going to A* algorythm node= object which has the solution and any other needed params
        bothnodes = astarblocking()

        if bothnodes:
            node,node2=bothnodes

        else:
            node=bothnodes
            node2=None
        # when we finish solving the puzle
        end = timer()
        moves = []
        moves2 = []
        #if node==None it means algorythm couldnt find solution
        # if node==None and node2==None:

        if node==None:

            f.write("\npuzzle #%d" % (numpuzzle))
            f.write("\n no possible solution ")
            f.write("\nExplored %d states in %f seconds "% (len(visited), (end - start)))
            print ("couldnt find solution for puzzle #%d"%(numpuzzle))
            numpuzzle+=1

        else:

            #moves are stored in this format [8,1],[6,-1][index,move] meaning index=index of the car in the vehicles array and 1/-1=R/L or U/D depinding on orientation
            #this loop takes all the moves stored in the node returned from astarblocking() and turns them into a format of [X,R],[O,L]
            visited[root.get_hash()]=None

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

            while visited2[node2] is not None:
                if visited2[node2][0][visited2[node2][1][0]].orientation == 'H':
                    if visited2[node2][1][1] == 1:
                        moves2.append([visited2[node2][0][visited2[node2][1][0]].id, 'L'])
                        node2 = visited2[node2][0]
                    elif visited2[node2][1][1] == -1:
                        moves2.append([visited2[node2][0][visited2[node2][1][0]].id, 'R'])
                        node2 = visited2[node2][0]
                elif visited2[node2][0][visited2[node2][1][0]].orientation == 'V':
                    if visited2[node2][1][1] == 1:
                        moves2.append([visited2[node2][0][visited2[node2][1][0]].id, 'U'])
                        node2 = visited2[node2][0]
                    elif visited2[node2][1][1] == -1:
                        moves2.append([visited2[node2][0][visited2[node2][1][0]].id, 'D'])
                        node2 = visited2[node2][0]

            #reversing moves because we start adding moves in reverse order so we reverse it back in the end
            moves.reverse()
            numpuzzle += 1
            f.write("\npuzzle #%d" % (numpuzzle))
            f.write("\nmoves: ")
            for move in moves:
                f.write(" %s%s, " % ((move[0]),(move[1])))
            for move2 in moves2:
                f.write(" %s%s, " % ((move2[0]),(move2[1])))
            f.write("\nExplored %d states in %f seconds" % (len(visited), (end - start)))
            f.write("\nSolved in %d moves" % (len(moves)))
        # start visualisation if wanted
    f.close()
