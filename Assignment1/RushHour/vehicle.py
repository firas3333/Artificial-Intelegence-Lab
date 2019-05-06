smallcar = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
largecar = {'O', 'P', 'Q', 'R'}

#code explains itself we create an objec vehicle of clas vehicle while checking that the car is valid if not the are some raise errors
class Vehicle(object):

    def __init__(self, id, x, y, orientation):
        if id in smallcar:
            self.id = id
            self.length = 2
        elif id in largecar:
            self.id = id
            self.length = 3
        else:
            raise ValueError('Invalid id {0}'.format(id))

        if 0 <= x <= 5:
            self.x = x
        else:
            raise ValueError('Invalid x {0}'.format(x))

        if 0 <= y <= 5:
            self.y = y
        else:
            raise ValueError('Invalid y {0}'.format(y))

        if orientation == 'H':
            self.orientation = orientation
            x_end = self.x + (self.length - 1)
            y_end = self.y
        elif orientation == 'V':
            self.orientation = orientation
            x_end = self.x
            y_end = self.y + (self.length - 1)
        else:
            raise ValueError('Invalid orientation {0}'.format(orientation))
        if x_end > 5 or y_end > 5:
            raise ValueError('Invalid configuration')

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Vehicle({0}, {1}, {2}, {3})".format(self.id, self.x, self.y,
                                                    self.orientation)
