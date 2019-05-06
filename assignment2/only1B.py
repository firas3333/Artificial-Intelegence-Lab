from vehicle import Vehicle

# goal vihcle (4,2) means its out
# 2 arrays to set the length of a vehicle
GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')
smallcars = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
largecars = {'O', 'P', 'Q', 'R'}


# class RushHour has all the moethods and functionts we need to implement A* for solving RushHour (node)
class RushHour(object):
    # constructor to initiate vehicles, board, move, depth of the state , and its value (heuristic)
    def __init__(self, vehicles, board=None, moved=None, depth=0, value=None):
        """Create a new Rush Hour board.

        Arguments:
            vehicles: a set of Vehicle objects.
        """
        self.board = board
        self.vehicles = tuple(vehicles)
        self.moved = moved
        self.depth = depth
        self.value = value


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

    # getting all the possible moves in this format [index,move]
    def get_moves(self):

        board = self.get_board()
        moves = []
        for index, v in enumerate(self.vehicles):
            # horizontally orientated vehicle
            if v.orientation == 'H':
                # left test
                if v.x != 0 and board[v.y][v.x - 1] == ' ':
                    moves.append([index, -1])
                # right test
                if v.x + v.length - 1 < 5 and board[v.y][v.x + v.length] == ' ':
                    moves.append([index, 1])
            # vertically orientated vehicle
            else:
                # up test
                if v.y != 0 and board[v.y - 1][v.x] == ' ':
                    moves.append([index, -1])
                # down test
                if v.y + v.length - 1 < 5 and board[v.y + v.length][v.x] == ' ':
                    moves.append([index, 1])
        return moves

    def move(self, index, move):
        board = self.get_board()

        node = RushHour(list(self.vehicles), list(board), (index, move), self.depth + 1)

        # get the vehicle that needs to be moved
        vehicle = node.vehicles[index]
        # move horizontal vehicle
        if vehicle.orientation == 'H':
            # generate new row for board
            node.board[vehicle.y] = list(node.board[vehicle.y])
            # right
            if move > 0:
                node.board[vehicle.y][vehicle.x] = ' '
                node.board[vehicle.y][vehicle.x + vehicle.length] = vehicle.id

            # left
            else:
                node.board[vehicle.y][vehicle.x - 1] = vehicle.id
                node.board[vehicle.y][vehicle.x + vehicle.length - 1] = ' '

        # move vertical vehicle
        else:
            # down
            if move > 0:

                # new rows for board
                node.board[vehicle.y] = list(node.board[vehicle.y])
                node.board[vehicle.y + vehicle.length] = list(node.board[vehicle.y + vehicle.length])

                node.board[vehicle.y][vehicle.x] = ' '
                node.board[vehicle.y + vehicle.length][vehicle.x] = vehicle.id
            # up
            else:

                #  rows for board
                node.board[vehicle.y - 1] = list(node.board[vehicle.y - 1])
                node.board[vehicle.y + vehicle.length - 1] = list(node.board[vehicle.y + vehicle.length - 1])

                node.board[vehicle.y - 1][vehicle.x] = vehicle.id
                node.board[vehicle.y + vehicle.length - 1][vehicle.x] = ' '

        # update self.vehicles
        node.vehicles = list(node.vehicles)

        # depends on car orientation we move
        if node.vehicles[index].orientation == 'H':

            node.vehicles[index] = Vehicle(node.vehicles[index].id, vehicle.x + move, vehicle.y, vehicle.orientation)

        elif node.vehicles[index].orientation == 'V':

            node.vehicles[index] = Vehicle(node.vehicles[index].id, vehicle.x, vehicle.y + move, vehicle.orientation)

        node.vehicles = tuple(node.vehicles)

        # calculate the cost estimate
        node.value = node.get_cost_estimate()

        return node
    def get_cost_estimate(self):
        return self.depth + self.get_min_distance() + self.get_additional_steps()

    def get_min_distance(self):
        for v in self.vehicles:
            if v.id == 'X':
                return 5 - (v.x + v.length - 1)

    def get_additional_steps(self):
        steps = 0
        c = 0
        for v in self.vehicles:
            if v.id == 'X':
                c += 1
                origin = v.x + v.length - 1

        # check for vehicles in the direct path car x
        for i in range(1, self.get_min_distance() + 1):
            # get the i places from the car x
            index = self.board[origin + i][2]
            if index != ' ':
                # get the directly blocking vehicle
                counter = 0
                for i in self.vehicles:
                    if i.id == index:
                        vehicle = self.vehicles[counter]
                    counter += 1
                # center large car  in path of car x
                if vehicle.y < 2 < vehicle.y + vehicle.length - 1:
                    steps += 2
                # blocked no center
                else:
                    steps += 1
        return steps

    # checking if the block around me is blocked
    def is_blocked(self, index):
        if index == ' ':
            return False
            counter = 0
            for i in self.vehicles:
                if i.id == index:
                    vehicle = self.vehicles[counter]
                counter += 1
            # horizontally orientated vehicle
            if vehicle.orientation == 'H':
                if vehicle.x == 0 and self.board[vehicle.y][vehicle.x - 1]:
                    return True
                elif vehicle.x + vehicle.length - 1 == 5 and self.board[vehicle.x][vehicle.y - 1]:
                    return True
                elif self.board[vehicle.x][vehicle.y - 1] and self.board[vehicle.x][vehicle.x + vehicle.length - 1]:
                    return True

            # vertically orientated vehicle
            else:
                if vehicle.y == 0 and self.board[vehicle.y + vehicle.length - 1][vehicle.x]:
                    return True
                elif vehicle.y + vehicle.length - 1 == 5 and self.board[vehicle.y - 1][vehicle.x]:
                    return True
                elif self.board[vehicle.x - 1][vehicle.y] and self.board[vehicle.y + vehicle.length - 1][vehicle.y]:
                    return True
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