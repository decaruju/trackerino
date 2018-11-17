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
        print('trackerino time tracker')
        print('---------------------------------')
        print()
        print('Expected one option of [(a)ctivities, (e)ntries, (c)hange, (r)eport, (s)tatus]')
        print('To add an activity, use "trk a <name-of-activity>"')
        print('To add an entry, use "trk e <name-or-id-of-activity>"')

    def status(self):
        last_entry = self.db.last_entry()
        print(f'Last entry is {last_entry}')
        date_time = datetime.datetime.fromisoformat(last_entry[2])
        print(f'You started working on it {timeago.format(date_time, datetime.datetime.now())}')

    def report(self):
        if len(sys.argv) == 2:
            print('Defaulting to reporting today')
            entries = self.db.day_entries()
        elif len(sys.argv) == 3:
            if sys.argv[2] in ('w', 'week', ):
                entries = self.db.week_entries()
            elif sys.argv[2] in ('d', 'day', ):
                entries = self.db.day_entries()

        if len(entries) == 0:
            print('You have no entries for this period')
            return
        day = datetime.datetime.fromisoformat(entries[0][2].split()[0])

        print(f'Your first entry is at {str(entries[0][2]).split()[1]}')
        entries.insert(0, (0, 'nothing', day.isoformat()))
        entries.append((0, 'nothing', datetime.datetime.now().isoformat()))

        time_spent = defaultdict(datetime.timedelta)
        for entry1, entry2 in zip(entries[:-1], entries[1:]):
            time_spent[entry1[1]] += (datetime.datetime.fromisoformat(entry2[2]) - datetime.datetime.fromisoformat(entry1[2]))
        for activity, duration in time_spent.items():
            if activity == 'nothing':
                continue
            print(f'You spent {str(duration).split(".")[0]} on {activity}')
            
            

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
        elif sys.argv[2] in ('e', 'edit', ):
            if len(sys.argv) <= 4:
                print("To edit a task, add its ID and the new datetime")
            else:
                self.db.edit_entry(sys.argv[3],  sys.argv[4])

        else:
            print('e options expects one of [d (day), w (week)]')

    def activities(self):
        if len(sys.argv) == 2:
            print(self.db.list_activities())
        else:
            self.db.add_activity(sys.argv[2])
