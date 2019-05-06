import  heapq
from timeit import default_timer as timer
import forblocking as forblocking
from timeit import default_timer as timer

def run(path):
    # array of all cars that thier length is 2
    smallcars = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
    #loading file (takes one line (one puzzle) per call)
    def load_file(line):
        #array to keep track of cars that weve already added to the array of vehicles
        visitedLOAD = []
        #array of the cars regular array
        vehicles = []
        #array for objects of class vehicle (also contains same cars)
        finalvehicles=[]
        #6x6 listof lists
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        counter = 0
        #loop to read the line charachter by charachter
        for i in range(0, 6):
            for j in range(0, 6):
                #name of the care
                carid = line[counter]
                #we decided its simpler to call empty block as white space rather than '.'
                if carid == '.':
                    board[i][j] = ' '
                else:
                    #filling the board with cars(were inserting charachter by character regardless of what it means )
                    board[i][j] = line[counter]
                #if its first time we se this car we must store it in vehicles as normal list
                # vehicles[i]=[carid, row,column,length]
                if carid not in visitedLOAD and carid != '.':
                    if carid in smallcars:
                        short = 2
                        vehicles.append([carid, int(i), int(j), int(short)])
                    else:
                        long = 3
                        vehicles.append([carid, int(i), int(j), int(long)])

                    visitedLOAD.append(carid)

                counter += 1
        #checking the board to detirmine car's orientation
        for car in vehicles:
            v, h = 'V', 'H'
            if car[1] + 1 > 5:
                if car[0] == board[car[1] - 1][car[2]]:
                    car.extend(v)
                else:
                    car.extend(h)
            elif car[1] - 1 < 0:
                if car[0] == board[car[1] + 1][car[2]]:
                    car.extend(v)
                else:
                    car.extend(h)
            elif car[0] == board[car[1] - 1][car[2]] or car[0] == board[car[1] + 1][car[2]]:
                car.extend(v)
            else:
                car.extend(h)

            id, x, y, orientation = car[0],car[2],car[1],car[4]
            #finalvehicles array of cars wich each car is represented as object from vehicle class vehicle(id,column,row,orientation)
            finalvehicles.append(forblocking.Vehicle(id, x, y, orientation))
        #create instance of class rushhour that has all the vehicles in it
        return forblocking.RushHour(set(finalvehicles))

    def astarblocking():
        #using A* to calculate the optimal path to win
        #if theres no solution return None if there solution return the node that contains all the needed data
        #admisable hueristic
        while len(pqueue):
            # pop the node with lowest cost estimate by value =depth of node + min distance from car x to the exit + number of steps needed to clean the road for car x
            node = heapq.heappop(pqueue)
            # expand to all posible children (boards after 1 move)
            for move in node.get_moves():
                child = node.move(move[0], move[1])
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
    f = open("Astar_output.txt", "w+")
    problems = open(path, "r")
    #reading one line (1 puzzle)
    for line in problems:
        root = load_file(line)
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
            print "couldnt find solution for puzzle #%d"%(numpuzzle)
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
