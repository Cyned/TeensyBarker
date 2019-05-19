import psycopg2
import sys

import pandas as pd

from configparser import ConfigParser
from psycopg2 import ProgrammingError as DBResultsError
from typing import Sequence, Tuple

from databases.base import BasePostgres
from utilities import db_insert, db_select, db_search
from utils import transform_df_to_places, transform_df_to_working_time, delete_existed, decode_working_time
from config import (
    DB_FILE_NAME, DB_SECTION, DB_PLACES_TABLE, DB_PLACES_COLUMNS,
    DB_WORKING_TIME_TABLE, DB_WORKING_TIME_COLUMNS, DB_PLACES_ID_COLUMN,
)
from app import collect_logger as logger


class BDPlaces(BasePostgres):
    """
    Class to get and push data into the database
    """

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

    def test(self):
        """ Just test the connection with the database"""
        try:
            db_select(self.conn.cursor, DB_PLACES_TABLE, [DB_PLACES_COLUMNS['website']])
            db_select(self.conn.cursor, DB_WORKING_TIME_TABLE, [DB_WORKING_TIME_COLUMNS['days']])
            logger.info('test is successful')
        except Exception:
            logger.exception('Test failed. Something wrong with databases.')

    def add(self, data: pd.DataFrame):
        """
        Add records to the database
        :param data: pandas.DataFrame to insert into table
        """

        df = delete_existed(data=data, columns=('reference',), results=self.get_place(columns='place_id'))
        if df.empty:
            logger.info('There are no new places.')
            return
        data_places = transform_df_to_places(data=df, columns_dict=DB_PLACES_COLUMNS)
        if not data_places:
            logger.info(f'No records were written into {DB_WORKING_TIME_TABLE}.')
            return
        # insert data to Places table
        try:
            result = db_insert(
                cursor    = self.conn.cursor,
                table     = DB_PLACES_TABLE,
                columns   = DB_PLACES_COLUMNS.values(),
                values    = data_places,
                returning = (DB_PLACES_COLUMNS['place_id'], DB_PLACES_ID_COLUMN),
            )
            logger.info(f'{DB_PLACES_TABLE} records were written.')
        except Exception:
            logger.exception(f'Error was caught while writen new records to {DB_PLACES_TABLE} database.')
            result = None
        # insert data to WorkingTime table
        try:
            if result:
                data_times = transform_df_to_working_time(
                    data=df, place_ids=result, columns_dict=DB_WORKING_TIME_COLUMNS,
                )
                db_insert(
                    cursor  = self.conn.cursor,
                    table   = DB_WORKING_TIME_TABLE,
                    columns = DB_WORKING_TIME_COLUMNS.values(),
                    values  = data_times,
                )
                logger.info(f'{DB_WORKING_TIME_TABLE} records were written')
            else:
                logger.info(f'No records were written into {DB_PLACES_TABLE}.')
        except Exception:
            logger.exception(f'Error was caught while writen new records to {DB_WORKING_TIME_TABLE} database.')

    def get_place(self, columns: Sequence[str]) -> Tuple[Tuple]:
        """
        Get columns from Places in database.
        :return: tuple of results
        """
        return self.get(table=DB_PLACES_TABLE, columns=columns)

    def get_working_time(self, place_ids: Sequence[int]) -> dict:
        """
        Get working time of current place_id
        :param place_ids: list of id of places
        :return: data
        """
        if type(place_ids) is not tuple and type(place_ids) is not list:
            place_ids = (place_ids,)
        dict_ = dict()
        for place_id in place_ids:
            results = db_search(
                cursor     = self.conn.cursor,
                table      = DB_WORKING_TIME_TABLE,
                columns    = DB_WORKING_TIME_COLUMNS.values(),
                conditions = {DB_WORKING_TIME_COLUMNS['place_id']: place_id},
                operator   = 'or',
            )
            dict_.update(decode_working_time(results))
        return dict_

    def get(self, table: str, columns: Sequence[str]) -> Tuple[Tuple]:
        """
        Get columns from table in database.
        :return: data for the database
        """
        if type(columns) is not tuple and type(columns) is not list:
            columns = [columns]
        results = db_select(
            cursor   = self.conn.cursor,
            table    = table,
            columns = [DB_PLACES_COLUMNS[column] for column in columns],
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
            return super(BDPlaces, self).__getattribute__(item)
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
