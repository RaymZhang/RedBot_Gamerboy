from random import randrange

class die(object):

    def __init__(self):
        self.value = None
        self.roll()

    def roll(self):
        self.value = randrange(1, 7)
