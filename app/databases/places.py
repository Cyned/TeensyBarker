import pandas as pd

from typing import Sequence, Tuple, Optional, List, Any

from databases.base import BasePostgres
from collect_places.utils import (
    transform_df_to_places, transform_df_to_working_time, delete_existed, decode_working_time,
)
from config import (
    DB_PLACES_TABLE, DB_PLACES_COLUMNS,
    DB_WORKING_TIME_TABLE, DB_WORKING_TIME_COLUMNS, DB_PLACES_ID_COLUMN,
    DB_MENUS_TABLE, DB_MENUS_COLUMNS, DB_MENUS_ID_COLUMN,
)
from app import basic_logger as logger


class DBPlaces(BasePostgres):
    """ Class to get and push data into the Places database """

    def __init__(self):
        """ Connect to the PostgresSQL database server """
        super(DBPlaces, self).__init__()

    def add_places(self, data: pd.DataFrame):
        """
        Add records `data` to the database
        :param data: pandas.DataFrame to insert into table
        """
        df = delete_existed(
            data=data, columns=('reference',), results=tuple(zip(*self.get_places(columns='place_id'))),
        )
        if df.empty:
            logger.info('There are no new places.')
            return
        # insert data to Places table
        places = transform_df_to_places(data=df, columns_dict=DB_PLACES_COLUMNS)
        try:
            result = self.insert(
                table     = DB_PLACES_TABLE,
                columns   = places.columns,
                values    = places.values,
                returning = (DB_PLACES_COLUMNS['place_id'], DB_PLACES_ID_COLUMN),
            )
            logger.info(f'{DB_PLACES_TABLE} records were written.')
        except Exception as e:
            logger.error(f'Error was caught while writen new records to {DB_PLACES_TABLE} database.')
            logger.exception(e)
            return
        # insert data to WorkingTime table
        data_times = transform_df_to_working_time(
            data=df, place_ids=result, columns_dict=DB_WORKING_TIME_COLUMNS,
        )
        try:
            self.insert(
                table     = DB_WORKING_TIME_TABLE,
                columns   = data_times.columns,
                values    = data_times.values,
                returning = (DB_PLACES_COLUMNS['place_id'], DB_PLACES_ID_COLUMN),
            )
            logger.info(f'{DB_WORKING_TIME_TABLE} records were written')
        except Exception as e:
            logger.error(f'Error was caught while writen new records to {DB_WORKING_TIME_TABLE} database.')
            logger.exception(e)

    def get_places(self, columns: Sequence[str]) -> Tuple[Tuple]:
        """
        Get columns from `Places` table` in database.
        :return: tuple of results
        """
        if type(columns) is not tuple and type(columns) is not list:
            columns = [columns]
        results = self.select(table=DB_PLACES_TABLE, columns=[
                DB_PLACES_COLUMNS[column] if DB_PLACES_COLUMNS.get(column) else column for column in columns
        ])
        return results

    def get_place_from_name(self, place_name: str) -> Optional[str]:
        """
        Get place id from from the database
        :param place_name: name of the place to search
        :return: ids of the place
        """
        results = self.search(
            table      = DB_PLACES_TABLE,
            columns    = [DB_PLACES_ID_COLUMN],
            conditions = {DB_PLACES_COLUMNS['name']: place_name},
        )
        if results:
            return results[0][0]
        return None

    def get_working_time(self, place_ids: Sequence[int]) -> dict:
        """
        Get working time of current place_id
        :param place_ids: list of indices of places
        :return: data about the working time
        """
        if not isinstance(place_ids, Sequence):
            place_ids = (place_ids,)
        dict_ = dict()
        for place_id in place_ids:
            results = self.search(
                table      = DB_WORKING_TIME_TABLE,
                columns    = list(DB_WORKING_TIME_COLUMNS.values()),
                conditions = {DB_WORKING_TIME_COLUMNS['place_id']: place_id},
                operator   = 'or',
            )
            dict_.update(decode_working_time(results))
        return dict_

    def get_menu_from_file_name(self, file_name: str) -> Tuple:
        """
        Get menu from the database
        :param file_name: name of the file to search in the data base
        :return: ids of the menus
        """
        results = self.search(
            table      = DB_MENUS_TABLE,
            columns    = [DB_MENUS_ID_COLUMN],
            conditions = {DB_MENUS_COLUMNS['file_name']: file_name},
        )
        return results

    def get_menus_from_place_id(self, place_id: str) -> Tuple[Any]:
        """
        Get menus fro the database
        :param place_id: id of the place
        :return: name of the menu file
        """
        results = self.search(
            table      = DB_MENUS_TABLE,
            columns    = [DB_MENUS_COLUMNS['file_name']],
            conditions = {DB_MENUS_COLUMNS['place_id']: place_id},
        )
        return list(zip(*results))[0]

    def add_menu(self, data: dict):
        """
        Add menu into the database
        :param data: data about the menu
        """
        self.execute(
            'INSERT INTO {table} ({columns}) VALUES ({values})'.format(
            table   = f'"{DB_MENUS_TABLE}"',
            columns = ', '.join([
                f'"{DB_MENUS_COLUMNS[column]}"' if DB_MENUS_COLUMNS.get(column) else f'"{column}"' for column in data.keys()
            ]),
            values  = ', '.join([
                f"'{value}'" if value else 'current_timestamp' for value in data.values()
            ]),
        ))

    def update_menu_date(self, menu_id: int):
        """
        Update DateMenuUpdated of the menu
        :param menu_id: id of the menu date to update
        """
        self.execute(
            'UPDATE {table} SET {column_date} = current_timestamp where {column_id} = {value}'.format(
                table       = f'"{DB_MENUS_TABLE}"',
                column_date = f'"{DB_MENUS_COLUMNS["date"]}"',
                column_id   = f'"{DB_MENUS_ID_COLUMN}"',
                value       = menu_id,
            )
        )
