import sys
from collections import defaultdict
from db import DB
import datetime
import timeago


def usage():
    print('USAGE...')
    print('Defaulting to status')
    status()

def status():
    last_entry = db.last_entry()
    print(f'Last entry is {last_entry}')
    date_time = datetime.datetime.fromisoformat(last_entry[2])
    print(f'You started working on it {timeago.format(date_time, datetime.datetime.now())}')

def report():
    pass

def change():
    if len(sys.argv) == 2:
        print('Expected activity id or name, activities are:')
        activities()
        return
    try:
        last = db.last_entry()
        print(f'You worked on {last[1]} for {datetime.datetime.fromisoformat(last[2]) - datetime.datetime.now()}')
    except Exception as e:
        pass
    db.add_entry(sys.argv[2])
    print('Switched to activity', sys.argv[2])

def entries():
    if len(sys.argv) == 2:
        print('\n'.join(f'ID: {entry[0]}, Activity: {entry[1]}, Start: {entry[2]}' for entry in db.entries()))
    elif sys.argv[2] in ('w', 'week', ):
        print('\n'.join(f'ID: {entry[0]}, Activity: {entry[1]}, Start: {entry[2]}' for entry in db.week_entries()))
    elif sys.argv[2] in ('d', 'day', ):
        print('\n'.join(f'ID: {entry[0]}, Activity: {entry[1]}, Start: {entry[2]}' for entry in db.day_entries()))
    else:
        print('e options expects one of [d (day), w (week)]')

def activities():
    if len(sys.argv) == 2:
        print(db.list_activities())
    else:
        db.add_activity(sys.argv[2])

if __name__ == '__main__':
    fmap = defaultdict(lambda: usage)
    fmap['s'] = status
    fmap['status'] = status
    fmap['r'] = report
    fmap['report'] = report
    fmap['c'] = change
    fmap['change'] = change
    fmap['e'] = entries
    fmap['entries'] = entries
    fmap['a'] = activities
    fmap['activities'] = activities

    db = DB()
    db.create_tables()
    if len(sys.argv) == 1:
        usage()
    else:
        fmap[sys.argv[1]]()
