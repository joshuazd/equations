class Infix(object):
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)
    def __pow__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(x, other))
    def __rpow__(self, other):
        return self.function(other)
    def __mul__(self, other):
        return self.function(other)
    def __rmul__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))



root = Infix(lambda x,y: y**(1.0/x))
