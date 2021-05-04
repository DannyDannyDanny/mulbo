"""Define mpath, read files in mpath, write file index to database."""
import sqlite3
try:
    import config
except ImportError:
    from foldersage import config
path_to_db = config.dirs['db_foldersage']


def get_db_con():
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(path_to_db)
    return conn


def sql_exec(sql_cmd, con=None):
    if con is None:
        con = get_db_con()
    cursorObj = con.cursor()
    cursorObj.execute(sql_cmd)
    con.commit()


def index_file(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO files(path) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO audio(name,file_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid
