from vehicle import Vehicle
GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')
CAR_IDS = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
TRUCK_IDS = {'O', 'P', 'Q', 'R'}

class RushHour(object):

    def __init__(self, vehicles,board=None):
        self.vehicles = vehicles
        self.board=board

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        string = '-' * 8 + '\n'
        for line in self.get_board():
            string += '|{0}|\n'.format(''.join(line))
        string += '-' * 8 + '\n'
        return string

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

    def solved(self):
        return GOAL_VEHICLE in self.vehicles
#computing all posible move in the current state were in
    def moves(self):
        board = self.get_board()
        for v in self.vehicles:
            if v.orientation == 'H':
                if v.x - 1 >= 0 and board[v.y][v.x - 1] == ' ':
                    new_v = Vehicle(v.id, v.x - 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)
                if v.x + v.length <= 5 and board[v.y][v.x + v.length] == ' ':
                    new_v = Vehicle(v.id, v.x + 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)
            else:
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y - 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)
                if v.y + v.length <= 5 and board[v.y + v.length][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y + 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles)


def load_file(line):
    visitedLOAD = []
    vehicles = []
    finalvehicles=[]
    board = [[' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ']]
    counter = 0
    for i in range(0, 6):
        for j in range(0, 6):
            carid = line[counter]

            if carid == '.':
                board[i][j] = ' '
            else:
                board[i][j] = line[counter]
            if carid not in visitedLOAD and carid != '.':
                if carid in CAR_IDS:
                    short = 2
                    vehicles.append([carid, int(i), int(j), int(short)])
                else:
                    long = 3
                    vehicles.append([carid, int(i), int(j), int(long)])

                visitedLOAD.append(carid)

            counter += 1
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

        finalvehicles.append(Vehicle(id, x, y, orientation))
    return RushHour(set(finalvehicles),board)


