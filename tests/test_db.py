from ..db import DB
import datetime
import pytest


entries_table_name = "ENTRIES"
activities_table_name = "ACTIVITIES"
activity_name = "TEST ACTIVITY"

@pytest.fixture
def db_without_tables(tmpdir):
    db_file = tmpdir.join("temp.db")
    return DB(filename=db_file, entries_table_name=entries_table_name, activities_table_name=activities_table_name)

@pytest.fixture
def db_without_activities(db_without_tables):
    db_without_tables.create_tables()
    return db_without_tables

@pytest.fixture
def db_without_entries(db_without_activities):
    db_without_activities.add_activity(activity_name)
    return db_without_activities

@pytest.fixture
def db(db_without_entries):
    db_without_entries.add_entry(activity_name)
    db_without_entries.add_entry(activity_name)
    db_without_entries.add_entry(activity_name)
    new_date_time = (datetime.datetime.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
    db_without_entries.edit_entry(2, new_date_time)
    new_date_time = (datetime.datetime.today() + datetime.timedelta(weeks=-1)).strftime('%Y-%m-%d %H:%M:%S')
    db_without_entries.edit_entry(1, new_date_time)
    return db_without_entries

def test_constructor_connects_to_db(tmpdir):
    db_file = tmpdir.join("temp.db")
    DB(filename=db_file, entries_table_name=entries_table_name, activities_table_name=activities_table_name)

def test_constructor_assigns_given_table_names(db):
    assert db.entries_table_name == entries_table_name
    assert db.activities_table_name == activities_table_name

def test_no_tables_exists_on_construction(db_without_tables):
    with db_without_tables.connection as csr:
        value = list(csr.execute("SELECT * FROM sqlite_master WHERE type='table';"))
    assert len(value) == 0

def test_tables_are_created(db):
    with db.connection as csr:
        value = list(csr.execute("SELECT * FROM sqlite_master WHERE type='table';"))
    assert len(value) == 3 # a sequence is created and counted as a table

def test_tables_have_correct_name(db):
    with db.connection as csr:
        value = list(csr.execute("SELECT name FROM sqlite_master WHERE type='table';"))

    assert (entries_table_name, ) in value
    assert (activities_table_name, ) in value

def test_activities_table_is_empty_on_construction(db_without_activities):
    assert len(db_without_activities.list_activities()) == 0

def test_add_activity_create_table(db_without_activities):
    activity_name = "TEST"
    db_without_activities.add_activity(activity_name)
    assert len(db_without_activities.list_activities()) == 1

def test_add_activity_assign_correct_name(db):
    assert db.list_activities()[0][1] == activity_name

def test_activity_id_fetches_correct_id(db):
    assert db.activity_id(activity_name) == 1

def test_edit_activity_by_name_changes_name(db):
    new_name = "NEW_NAME"
    db.edit_activity(activity_name, new_name)
    assert db.list_activities()[0][1] == new_name

def test_edit_activity_by_id_changes_name(db):
    new_name = "NEW_NAME"
    db.edit_activity(1, new_name)
    assert db.list_activities()[0][1] == new_name

def test_no_entries_on_construction(db_without_entries):
    assert len(db_without_entries.entries()) == 0

def test_add_entry_with_name_adds_an_entry(db_without_entries):
    db_without_entries.add_entry(activity_name)
    assert len(db_without_entries.entries()) == 1

def test_add_entry_with_id_adds_an_entry(db_without_entries):
    db_without_entries.add_entry(1)
    assert len(db_without_entries.entries()) == 1

def test_last_entry_returns_last_entry(db):
    assert db.last_entry()[0] == 3

def test_show_entry_returns_correct_entry(db):
    assert db.show_entry(2)[0] == 2

def test_edit_entry_edits_the_entry(db):
    new_date_time = (datetime.datetime.today() + datetime.timedelta(weeks=-1)).strftime('%Y-%m-%d %H:%M:%S')
    db.edit_entry(1, new_date_time)
    assert db.show_entry(1)[2] == new_date_time

def test_day_entries_returns_entries_of_the_day(db):
    assert len(db.day_entries()) == 1

def test_week_entries_returns_entries_of_the_week(db):
    assert len(db.week_entries()) == 2

def test_activity_entries_by_id_returns_the_entries(db):
    assert len(db.activity_entries(1)) == 3

def test_activity_entries_by_name_returns_the_entries(db):
    assert len(db.activity_entries(activity_name)) == 3