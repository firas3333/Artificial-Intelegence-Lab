from vehicle import Vehicle

# goal vihcle (4,2) means its out
# 2 arrays to set the length of a vehicle
GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')
smallcars = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
largecars = {'O', 'P', 'Q', 'R'}


# class RushHour has all the moethods and functionts we need to implement A* for solving RushHour (node)
class RushHour(object):
    # constructor to initiate vehicles, board, move, depth of the state , and its value (heuristic)
    def __init__(self, vehicles, board=None, moved=None, depth=0, value=None,destroy=0):
        """Create a new Rush Hour board.

        Arguments:
            vehicles: a set of Vehicle objects.
        """
        self.board = board
        self.vehicles = tuple(vehicles)
        self.moved = moved
        self.depth = depth
        self.value = value
        self.destroyed=destroy

    # overload of equal
    def __eq__(self, other):
        return self.vehicles == other.vehicles

    # overload notequal
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    # comparing board depending on value
    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        s = '-' * 8 + '\n'
        for line in self.get_board():
            s += '|{0}|\n'.format(''.join(line))
        s += '-' * 8 + '\n'
        return s

    # using the the array of vehicles (self.vehicles) we creat and return the of the board where in right now
    def get_board(self):
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                for i in range(vehicle.length):
                    board[y][x + i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    board[y + i][x] = vehicle.id
        return board

    # true if we found solution
    def solved(self):
        return GOAL_VEHICLE in self.vehicles

    def get_hash(self):
        return self.vehicles

    # our goal vehicle is (X,4,2,H) so if we have X.x==4 we win :D
    def win(self):
        for v in self.vehicles:
            if v.id == 'X':
                if v.x == 4:
                    return True
                else:
                    return False






    def get_movesX(self):
        board = self.get_board()
        moves = []
        for index, v in enumerate(self.vehicles):
            # red car
            if v.id == 'X':
                # move right *go crazy!!!!!*
                if v.x + v.length - 1 < 5 and board[v.y][v.x + v.length] == ' ':
                    moves.append([index, 1, 0])
                elif v.x + v.length - 1 < 5 and board[v.y][v.x + v.length] != ' ':
                    self.destroyed += 1
                    badcarid = (board[v.y][v.x + v.length])
                    moves.append([index, 1, badcarid])
        return moves


    def moveforX(self, index, move, badcarid):
        board = self.get_board()

        node = RushHour(list(self.vehicles), list(board), (index, move), self.depth + 1)

        # get the vehicle that needs to be moved
        vehicle = node.vehicles[index]
        if move > 0:
            node.board[vehicle.y][vehicle.x] = ' '
            node.board[vehicle.y][vehicle.x + vehicle.length] = vehicle.id
        node.vehicles = list(node.vehicles)
        # depends on car orientation we move
        if badcarid == 0:
            a = 0
        else:
            i = 0
            for car in node.vehicles:
                if car.id == badcarid:
                    node.vehicles[i] = Vehicle(car.id, 0, 0, car.orientation, 1)
                i += 1

        node.vehicles[index] = Vehicle(node.vehicles[index].id, vehicle.x + move, vehicle.y, vehicle.orientation)
        node.vehicles = tuple(node.vehicles)
        # calculate the cost estimate
        node.value = node.get_cost_estimateX()

        return node


    def get_cost_estimateX(self):
        return self.depth + self.get_min_distance() + self.destroyed


    def get_min_distance(self):
            for v in self.vehicles:
                if v.id == 'X':
                    return 5 - (v.x + v.length - 1)
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
            finalvehicles.append(Vehicle(id, x, y, orientation))
        #create instance of class rushhour that has all the vehicles in it
        return RushHour(set(finalvehicles))
