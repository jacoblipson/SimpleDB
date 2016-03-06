import sys
from copy import copy

LEGAL_COMMANDS = [
    'BEGIN', 'ROLLBACK', 'COMMIT', 'SET', 'UNSET', 'GET', 'NUMEQUALTO'
]


class SimpleDatabase(object):
    def __init__(self):
        self.database = {}
        self.valscount = {}
        self.changelog = []

    def decrement_valcount(self, key):
        if key in self.database:
            self.valscount[self.database[key]] -= 1

    def increment_valcount(self, val):
        if val in self.valscount:
            self.valscount[val] += 1
        else:
            self.valscount[val] = 1

    def get(self, key):
        if key in self.database:
            print(self.database[key])
        else:
            print('NULL')

    def set(self, key, val):
        self.decrement_valcount(key)
        self.database[key] = val
        self.increment_valcount(val)

    def unset(self, key):
        self.decrement_valcount(key)
        del self.database[key]

    def numequalto(self, val):
        print(self.valscount[val]) \
            if val in self.valscount else print(0)

    def begin(self):
        self.changelog.insert(0, (copy(self.database), copy(self.valscount)))

    def rollback(self):
        if len(self.changelog) > 0:
            self.database, self.valscount = self.changelog[0]
            self.changelog.pop(0)
        else:
            print('NO TRANSACTION')

    def commit(self):
        self.changelog = []


database = SimpleDatabase()
line = sys.stdin.readline().strip()
while line != 'END':
    command_args = line.split(' ')
    if command_args[0] in LEGAL_COMMANDS:
        method = getattr(SimpleDatabase, command_args[0].lower())
        method(database, *command_args[1:])
    else:
        print("I'm sorry, I don't know command {0}.".format(command_args[0]))
    line = sys.stdin.readline().strip()
