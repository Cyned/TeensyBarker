import psycopg2
import sys

from configparser import ConfigParser
from psycopg2 import ProgrammingError as DBResultsError
from typing import Sequence, Tuple, Any

from databases.utilities import db_insert, db_select, db_search
from config import DB_FILE_NAME, DB_SECTION
from app import basic_logger as logger


class BaseDB(object):

    def __init__(self):
        self.conn = None

    def insert(self, **kwargs):
        raise NotImplementedError

    def select(self, *args, **kwargs):
        raise NotImplementedError

    def search(self, *args, **kwargs):
        raise NotImplementedError

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class BasePostgres(BaseDB):
    """ Basic class to manage postgres database """
    def __init__(self):
        """ Connect to the PostgresSQL database server """
        super(BasePostgres, self).__init__()

    def __enter__(self):
        try:
            # read connection parameters
            params = config()
            # connect to the PostgresSQL server
            logger.info('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.exception(error)
            sys.exit()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        logger.info('Database connection closed.')

    def insert(self, table: str, columns: Sequence[str], values, returning: Tuple[Any, str] = ()):
        """
        Insert data into the table and returning needful values
        :param table: name of the table
        :param columns: names of columns to insert to
        :param values: values to push into the database
        :param returning: name of columns to return
        :return:
        """
        results = db_insert(
            cursor    = self.conn.cursor,
            table     = table,
            columns   = columns,
            values    = values,
            returning = returning,
        )
        return results

    def search(self, table: str, columns: Sequence[str], conditions: dict, operator='and') -> Tuple[Tuple]:
        """
        Get columns from the table with conditions `where db_value == value`
        :param table: name of the table
        :param columns: columns to return
        :param conditions: dict of conditions
        :param operator: dict of conditions {column : value}
        :return: path of the file system
        """
        if type(columns) is not tuple and type(columns) is not list:
            columns = [columns]
        results = db_search(
            cursor     = self.conn.cursor,
            table      = table,
            columns    = columns,
            conditions = conditions,
            operator   = operator,
        )
        return results

    def select(self, table: str, columns: Sequence[str]) -> Tuple[Tuple]:
        """
        Get columns from table in database.
        :return: data for the database
        """
        if type(columns) is not tuple and type(columns) is not list:
            columns = [columns]
        results = db_select(
            cursor  = self.conn.cursor,
            table   = table,
            columns = columns,
        )
        return results

    def execute(self, query: str) -> Tuple[Tuple]:
        """
        Execute the PostgresSql query
        :param query: query to execute
        :return: request result
        """
        with self.conn.cursor() as cur:  # create a cursor
            cur.execute(query)
            try:
                results = cur.fetchall()
            except DBResultsError:
                results = ()
        return results

    def __getattribute__(self, item):
        try:
            return super(BasePostgres, self).__getattribute__(item)
        except TypeError:
            raise ConnectionError('Use context managers!')


def config(filename: str = DB_FILE_NAME, section: str = DB_SECTION) -> dict:
    """
    Get configs for the connection to the database
    :param filename: config_file [.ini] of the database to connect
    :param section: section of database
    :return: configuration dict
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgres sql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return db
