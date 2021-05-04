"""Define mpath, read files in mpath, write file index to database."""
import sqlite3
try:
    import config
except ImportError:
    from foldersage import config
from pathlib import Path
try:
    from foldersage.foldersage import get_db_con, sql_exec, index_file
except ImportError:
    from foldersage import get_db_con, sql_exec, index_file
path_to_db = config.dirs['db_foldersage']
Path(path_to_db).unlink()
sqlite3.connect(path_to_db)
# %%

sql_files_create = """
CREATE TABLE IF NOT EXISTS files (
    id integer PRIMARY KEY,
    path text NOT NULL
);"""
sql_audio_create = """
CREATE TABLE IF NOT EXISTS audio (
    id integer PRIMARY KEY,
    name text NOT NULL,
    file_id integer NOT NULL,
    FOREIGN KEY (file_id) REFERENCES files (id)
);"""

print('connecting')
con = get_db_con()
print('dropping')
sql_exec("DROP TABLE IF EXISTS files")
sql_exec("DROP TABLE IF EXISTS audio")
print('creating files table')
sql_exec(sql_files_create)
print('creating file test')

mpath = config.dirs['library']
mpath = Path(mpath)
print('mpath:', mpath, 'exists', mpath.exists())
tree = mpath.glob('**/*')
print('fetching tree for mpath')
for filepath in tree:
    if filepath.is_file():
        filepath = str(filepath)
        filepath = (filepath,)
        project_id = index_file(con, filepath)
        print(f'added {filepath}')
    else:
        print(f'skipped {filepath}')
con.close()
