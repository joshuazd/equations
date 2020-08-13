import random


class Resource(object):

    """Docstring for Resource. """

    def __init__(self, values):
        """TODO: to be defined1.

        :values: TODO

        """
        self._values = values

    def roll(self):
        """TODO: Docstring for roll.

        :f: TODO
        :returns: TODO

        """
        return random.choice(self._values)


class GreenResource(Resource):

    """Docstring for GreenResource. """

    def __init__(self):
        """TODO: to be defined1. """
        Resource.__init__(self, [4, 5, 6, '*', '^', '-'])


class BlackResource(Resource):

    """Docstring for BlackResource. """

    def __init__(self):
        """TODO: to be defined1. """
        Resource.__init__(self, [7, 8, 9, '+', '/', '√'])


class BlueResource(Resource):

    """Docstring for BlueResource. """

    def __init__(self):
        """TODO: to be defined1. """
        Resource.__init__(self, [0, 1, 2, '+', '-', '/'])


class RedResource(Resource):

    """Docstring for RedResource. """

    def __init__(self):
        """TODO: to be defined1. """
        Resource.__init__(self, [1, 2, 3, '+', '-', '*'])


class Game(object):

    """Docstring for Game. """

    def __init__(self):
        """TODO: to be defined1. """
        self._resources = [BlackResource()] * 5 + \
            [GreenResource()] * 5 + \
            [BlueResource()] * 5 + \
            [RedResource()] * 5

    def roll(self):
        """TODO: Docstring for roll.
        :returns: TODO

        """
        self._rolls = [r.roll() for r in self._resources]
        return self._rolls
