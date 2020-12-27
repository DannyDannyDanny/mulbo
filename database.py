import sqlite3
import config

path_to_db = config.dirs['db']
conn = sqlite3.connect(path_to_db)

sql_table = """
CREATE TABLE
messages(
    id integer PRIMARY KEY,
    name text,
    salary real,
    department text,
    position text,
    hireDate text)"""


def sql_exec(con=conn):
    cursorObj = con.cursor()
    cursorObj.execute(sql_table)
    con.commit()


sql_table()
