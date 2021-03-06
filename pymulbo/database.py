import sqlite3
from glob import glob
import config
import uuid
import os
import pandas as pd


def get_db_con():
    path_to_db = config.dirs['db']
    con = sqlite3.connect(path_to_db)
    return con


def sql_exec(sql_cmd, con=None):
    if con is None:
        con = get_db_con()
    cursorObj = con.cursor()
    cursorObj.execute(sql_cmd)
    con.commit()


# def refresh_collections_table():
# %%
# Create table paths with all paths in library
print("Create paths table")
sql_table_paths = """
DROP TABLE IF EXISTS paths;"""
sql_exec(sql_table_paths)
sql_table_paths = """
CREATE TABLE paths(
    path_id INTEGER PRIMARY KEY AUTOINCREMENT,
    path text);"""
sql_exec(sql_table_paths)
print("get collections glob")
path_records = glob(config.dirs['collection'] + '**/**/*.*')
path_records = [(p,) for p in path_records]
print("insert each path in collections glob to paths table")
conn = get_db_con()
c = conn.cursor()
c.executemany('INSERT INTO paths(path) VALUES (?)', path_records)



sql_cmd = "SELECT * FROM paths"
df_paths = pd.read_sql(sql_cmd, con=conn, index_col="path_id")

df_tmp = df_paths.apply(lambda x: x.path, axis=1)
path_to_collection_file = df_tmp.values[0]
path_to_collection_file
# %%
filename, extension = os.path.splitext(path_to_collection_file)
id = uuid.uuid5(uuid.NAMESPACE_OID, path_to_collection_file).hex
def generate_id_for_collection_file(path_to_collection_file):

# fname_import = config.dirs['originals'] + id + extension
# %%
conn.commit()
conn.close()


# %%
refresh_collections_table()
conn = get_db_con()
sql_cmd = "SELECT * FROM paths"
pd.read_sql(sql_cmd, con=conn, index_col="path_id")

# %%
failpaths = []
for filepath in collection:
    filename, extension = os.path.splitext(filepath)
    # id = uuid.uuid5(uuid.NAMESPACE_OID, filepath).hex
    # fname_import = config.dirs['originals'] + id + extension
    # print(fname_import)
