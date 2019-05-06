
import random
class Move(object):
    # constructor to initiate vehicles, board, move, depth of the state , and its value (heuristic)
    def __init__(self,car, direction):
        """Create a new Rush Hour board.

        Arguments:
            vehicles: a set of Vehicle objects.
        """
        self.car = car
        self.direction = direction
        self.w = random.randint(1,500)
    # overload of equal
    def __eq__(self, other):
        return self.w == other.w and self.car==other.car and self.direction==other.direction

    # overload notequal
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    # comparing board depending on value
    def __lt__(self, other):
        return self.w < other.w

    def get_w(self):
        return self.w
    def inc_w(self):
        return self.w+1
    def dec_w(self):
        return self.w-1
    def getid(self):
        return self.car
    def getdir(self):
        return self.direction
def loadallmoves(path):
    moves = open(path, "r")
    allpossiblemove=dict()
    movess=[]
    movesclass=[]
    for line in moves:
        id,dir=line.split(',')
        movess.append([int(id),int(dir)])
    for m in movess:
        move=Move(m[0],m[1])
        w=move.get_w()
        allpossiblemove[tuple(m)]=w
        movesclass.append(move)
    return allpossiblemove,movesclass
def loadoptsol(path):
    optsol=open(path,"r")
    puzlsoptsol=dict()
    i=0
    for line in optsol:
        puzlsoptsol[i]=line
        i+=1
    return puzlsoptsol
#
# if __name__ == '__main__':
#     pathformoves="possiblemoves"
#     pathforopt="optimalsolution"
#     allpossiblemove, movesclass = loadallmoves(pathformoves)
#     print(allpossiblemove[tuple([1,-1])])