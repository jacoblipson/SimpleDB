import sys
from collections import defaultdict

LEGAL_COMMANDS = [
    'BEGIN', 'ROLLBACK', 'COMMIT', 'SET', 'UNSET', 'GET', 'NUMEQUALTO'
]


class SimpleDatabase(object):
    def __init__(self):
        self.database = {}
        self.valscount = defaultdict(int)
        self.db_history = []
        self.vals_history = []

    # persist change to database, log change unless overwritten
    def write_db(self, key, val=None, log=True):
        if len(self.db_history) > 0 and log:
            self.db_history[0][key] = self.database[key] \
                if key in self.database else None
        if val:
            self.database[key] = val
        else:
            del self.database[key]

    # update the count of each value in the DB, log change unless overwritten
    def update_valcount(self, val, count, log=True):
        if len(self.vals_history) > 0 and log:
            self.vals_history[0][val] = self.valscount[val]
        self.valscount[val] = count

    def get(self, key):
        if key in self.database:
            print(self.database[key])
        else:
            print('NULL')

    def set(self, key, val):
        if key in self.database:
            # decrement the count for the value we are replacing
            self.update_valcount(self.database[key],
                                 self.valscount[self.database[key]] - 1)
        self.write_db(key, val)
        self.update_valcount(val, self.valscount[val] + 1)

    def unset(self, key):
        self.update_valcount(self.database[key],
                             self.valscount[self.database[key]] - 1)
        self.write_db(key)

    def numequalto(self, val):
        print(self.valscount[val])

    # new dicts in history will capture changes in this transaction block
    def begin(self):
        self.db_history.insert(0, {})
        self.vals_history.insert(0, defaultdict(int))

    # iterate across changes to database and value counts and reset state
    def rollback(self):
        if len(self.db_history) > 0:
            db_changes = self.db_history.pop(0)
            for key in db_changes:
                self.write_db(key, db_changes[key], False)

            val_changes = self.vals_history.pop(0)
            for val in val_changes:
                self.update_valcount(val, val_changes[val], False)
        else:
            print('NO TRANSACTION')

    def commit(self):
        self.db_history = []
        self.vals_history = []

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
