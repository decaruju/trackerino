import sqlite3
import os.path
import re


class DB:
    def __init__(self, filename="trackerino.sqlite3", entries_table_name="entries", activities_table_name="activities"):
        self.connection = sqlite3.connect(filename)
        self.entries_table_name = entries_table_name
        self.activities_table_name = activities_table_name

    def create_tables(self):
        with self.connection as csr:
            csr.execute(f'''CREATE TABLE IF NOT EXISTS {self.activities_table_name} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT
                            );''')
                            
            csr.execute(f'''CREATE TABLE IF NOT EXISTS {self.entries_table_name} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                activity INTEGER,
                                date_time TEXT,

                                FOREIGN KEY(activity) REFERENCES {self.activities_table_name}(id)
                            );''')
                                
    def edit_activity(self, activity, name):
        if type(activity) is str:
            activity = self.activity_id(activity)
        with self.connection as csr:
            csr.execute(f'''UPDATE {self.activities_table_name} SET
                            name = '{name}'
                            WHERE id = {activity};''')

    def add_activity(self, name):
        with self.connection as csr:
            csr.execute(f'''INSERT INTO {self.activities_table_name} (
                                name
                            ) VALUES (
                                '{name}'
                            );''')

    def list_activities(self):
        with self.connection as csr:
            activities = csr.execute(f'''SELECT * FROM {self.activities_table_name};''')
        return list(activities)

    def activity_id(self, activity_name):
        if re.match(r'\d+', activity_name):
            return int(activity_name)
        with self.connection as csr:
            value = csr.execute(f'''SELECT id FROM {self.activities_table_name}
                                    WHERE name = '{activity_name}';''')
        return list(value)[0][0]

    def add_entry(self, activity):
        if type(activity) is str:
            activity = self.activity_id(activity)
        with self.connection as csr:
            csr.execute(f'''INSERT INTO {self.entries_table_name} (
                                activity,
                                date_time
                            ) VALUES (
                                '{activity}',
                                datetime('now', 'localtime')
                            );''')

    def last_entry(self):
        return self.entries(limit="LIMIT 1")[0]

    def entries(self, condition='', limit=''):
        with self.connection as csr:
            value = csr.execute(f'''SELECT {self.entries_table_name}.id, act.name, date_time FROM {self.entries_table_name}
                                    INNER JOIN {self.activities_table_name} act ON act.id=activity
                                    {condition}
                                    ORDER BY {self.entries_table_name}.date_time DESC
                                    {limit}
                                    ;''')
        return list(value)

    def show_entry(self, id):
        return self.entries(f'WHERE {self.entries_table_name}.id = {id}')[0]

    def week_entries(self, change=0):
        return self.entries(f"WHERE strftime('%Y-%W', datetime(date_time, 'localtime')) = strftime('%Y-%W', datetime('now', '-{change*7} days', 'localtime'))")

    def day_entries(self, change=0):
        return self.entries(f"WHERE strftime('%Y-%j', datetime(date_time, 'localtime')) = strftime('%Y-%j', datetime('now', '-{change} days', 'localtime'))")

    def activity_entries(self, activity):
        if type(activity) is str:
            activity = self.activity_id(activity)
        return self.entries(f"WHERE activity={activity}")

    def edit_entry(self, id, date_time):
        with self.connection as csr:
            csr.execute(f'''UPDATE {self.entries_table_name}
                                    SET date_time = '{date_time}'
                                    WHERE id = {id};''')

