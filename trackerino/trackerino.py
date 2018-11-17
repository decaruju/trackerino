import sys
from collections import defaultdict
from .db import DB
import datetime
import timeago

class app:
    def __init__(self):
        self.define_fmap()
        self.db = DB()
        self.db.create_tables()
        if len(sys.argv) == 1:
            self.usage()
        else:
            self.fmap[sys.argv[1]]()

    def define_fmap(self):
        self.fmap = defaultdict(lambda: usage)
        self.fmap['s'] = self.status
        self.fmap['status'] = self.status
        self.fmap['r'] = self.report
        self.fmap['report'] = self.report
        self.fmap['c'] = self.change
        self.fmap['change'] = self.change
        self.fmap['e'] = self.entries
        self.fmap['entries'] = self.entries
        self.fmap['a'] = self.activities
        self.fmap['activities'] = self.activities


    def usage(self):
        print('USAGE...')
        print('Defaulting to status')
        self.status()

    def status(self):
        last_entry = self.db.last_entry()
        print(f'Last entry is {last_entry}')
        date_time = datetime.datetime.fromisoformat(last_entry[2])
        print(f'You started working on it {timeago.format(date_time, datetime.datetime.now())}')

    def report(self):
        pass

    def change(self):
        if len(sys.argv) == 2:
            print('Expected activity id or name, activities are:')
            self.activities()
            return
        try:
            last = self.db.last_entry()
            print(f'You worked on {last[1]} for {datetime.datetime.now() - datetime.datetime.fromisoformat(last[2])}')
        except Exception as e:
            pass
        self.db.add_entry(sys.argv[2])
        print('Switched to activity', sys.argv[2])

    def entries(self):
        if len(sys.argv) == 2:
            print('\n'.join(f'ID: {entry[0]}, Activity: {entry[1]}, Start: {entry[2]}' for entry in self.db.entries()))
        elif sys.argv[2] in ('w', 'week', ):
            print('\n'.join(f'ID: {entry[0]}, Activity: {entry[1]}, Start: {entry[2]}' for entry in self.db.week_entries()))
        elif sys.argv[2] in ('d', 'day', ):
            print('\n'.join(f'ID: {entry[0]}, Activity: {entry[1]}, Start: {entry[2]}' for entry in self.db.day_entries()))
        else:
            print('e options expects one of [d (day), w (week)]')

    def activities(self):
        if len(sys.argv) == 2:
            print(self.db.list_activities())
        else:
            self.db.add_activity(sys.argv[2])
