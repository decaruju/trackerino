from ..db import DB
import datetime


def test_constructor(tmpdir):
    db_file = tmpdir.join("temp.db")
    entries_table_name = "ENTRIES"
    activities_table_name = "ACTIVITIES"
    db = DB(filename=db_file, entries_table_name=entries_table_name, activities_table_name=activities_table_name)
    assert db.entries_table_name == entries_table_name
    assert db.activities_table_name == activities_table_name

def test_create_tables(tmpdir):
    db_file = tmpdir.join("temp.db")
    entries_table_name = "ENTRIES"
    activities_table_name = "ACTIVITIES"
    db = DB(filename=db_file, entries_table_name=entries_table_name, activities_table_name=activities_table_name)

    with db.connection as csr:
        value = list(csr.execute("SELECT * FROM sqlite_master WHERE type='table';"))
    assert len(value) == 0

    db.create_tables()

    with db.connection as csr:
        value = list(csr.execute("SELECT name FROM sqlite_master WHERE type='table';"))

    assert (entries_table_name, ) in value
    assert (activities_table_name, ) in value
    assert len(value) == 3 # a sequence is created and counted as a table

def test_activities(tmpdir):
    db_file = tmpdir.join("temp.db")
    entries_table_name = "ENTRIES"
    activities_table_name = "ACTIVITIES"
    db = DB(filename=db_file, entries_table_name=entries_table_name, activities_table_name=activities_table_name)
    db.create_tables()

    assert len(db.list_activities()) == 0
    activity_name = "TEST"
    db.add_activity(activity_name)
    assert len(db.list_activities()) == 1
    assert db.list_activities()[0][1] == activity_name
    assert db.activity_id(activity_name) == 1
    new_name = "NEW_NAME"
    db.edit_activity(activity_name, new_name)
    assert db.list_activities()[0][1] == new_name
    db.edit_activity(1, activity_name)
    assert db.list_activities()[0][1] == activity_name

def test_entries(tmpdir):
    db_file = tmpdir.join("temp.db")
    entries_table_name = "ENTRIES"
    activities_table_name = "ACTIVITIES"
    db = DB(filename=db_file, entries_table_name=entries_table_name, activities_table_name=activities_table_name)
    db.create_tables()
    activity_name = "TEST_ACTIVITY"
    db.add_activity(activity_name)

    assert len(db.entries()) == 0
    db.add_entry(1)
    db.add_entry(activity_name)
    assert len(db.entries()) == 2
    assert len(db.day_entries()) == 2
    assert len(db.week_entries()) == 2
    assert len(db.activity_entries(1)) == 2
    assert len(db.activity_entries(activity_name)) == 2
    assert db.show_entry(1)[1] == activity_name
    assert db.last_entry()[1] == activity_name
    new_date_time = (datetime.datetime.today() + datetime.timedelta(weeks=-1)).strftime('%Y-%m-%d %H:%M:%S')
    print(new_date_time)
    db.edit_entry(1, new_date_time)
    assert len(db.day_entries()) == 1
    assert len(db.day_entries(7)) == 1
    assert len(db.week_entries()) == 1
    assert len(db.week_entries(1)) == 1
