
class Event:
    def __init__(self, id, name, rating_count):
        self.id = id
        self.name = name
        self.rating_count = rating_count


class Operator:
    def __init__(self, id, name, rating_count):
        self.id = id
        self.name = name
        self.rating_count = rating_count


class EvaluationSet:
    def __init__(self, event_id, event_name, ones, twos, threes, fours, fives):
        self.event_id = event_id
        self.event_name = event_name
        self.ones = ones
        self.twos = twos
        self.threes = threes
        self.fours = fours
        self.fives = fives
        self.rating_count = ones+twos+threes+fours+fives
        if self.rating_count > 0:
            self.average = round((ones*2 + twos*2 + threes*3 + fours*4 + fives*5) / self.rating_count, 1)
        else:
            self.average = 0
        self.evals = [ones, twos, threes, fours, fives]
