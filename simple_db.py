import sys

LEGAL_COMMANDS = ['BEGIN', 'ROLLBACK', 'COMMIT', 'SET', 'UNSET', 'GET']


class SimpleDatabase(object):
    def __init__(self):
        self.database = {}
        self.changelog = []

    def get(self, key):
        if key in self.database:
            print(self.database['key'])
        else:
            print('NULL')

    def set(self, key, val):
        self.database[key] = val

    def unset(self, key):
        del self.database[key]

    def begin(self):
        self.changelog.insert(0, self.database)

    def rollback(self):
        self.database = self.changelog[0]
        self.changelog.pop()

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
