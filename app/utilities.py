from psycopg2 import ProgrammingError as DBResultsError
from typing import Sequence, Tuple
from app import collect_logger as logger


def db_insert(cursor, table: str, columns: Sequence[str], values, returning=()) -> Tuple[Tuple]:
    """
    Insert data into Postgres database
    :param cursor: cursor of Postgres database
    :param table: name of the table
    :param columns: names of columns
    :param values: values to insert
    :param returning: values to return after the insert
    :return: values defined in returning
    """
    returns = ''
    # returning construction
    if returning:
        returns = ' RETURNING {values}'.format(values=create_db_query(returning, type_='usual'))

    with cursor() as cur:  # create a cursor
        cur.execute(
            'INSERT INTO "{table}" ({db_columns}) VALUES {values}{returning};'.format(
                table=table,
                db_columns=create_db_query(columns, type_='usual'),
                values=create_db_query(values, type_='values'),
                returning=returns,
            ))
        try:
            results = cur.fetchall()
        except DBResultsError as e:
            logger.exception(e)
            results = ()
    return results


def db_select(cursor, table: str, columns: Sequence[str]) -> Tuple[Tuple]:
    """
    Select some data from Postgres database
    :param cursor: cursor of Postgres database
    :param table: name of the table
    :param columns: names of columns to select
    :return: list of results
    """

    with cursor() as cur:
        cur.execute(
            'SELECT {column} FROM "{table}";'.format(
                column = create_db_query(columns, type_='usual'),
                table  = table,
            )
        )
        results = cur.fetchall()
    return results


def db_search(cursor, table: str, columns: Sequence[str], conditions: dict, operator: str = 'and') -> Tuple[Tuple]:
    """
    Select some data from Postgres database using some conditions with AND
    :param cursor: cursor of Postgres database
    :param table: name of the table
    :param columns: names of columns to select
    :param conditions: conditions using to select data
    :param operator: AND or OR
    :return: requested data
    """
    with cursor() as cur:
        cur.execute(
            'SELECT {column} FROM "{table}" WHERE {conds};'.format(
                column = create_db_query(columns, type_='usual'),
                table  = table,
                conds  = create_conditions(conds=conditions, operator=operator),
            )
        )
        results = cur.fetchall()
    return results


def create_db_query(collection: Sequence, type_: str = 'usual') -> str:
    """
    Create right postgres request
    :param collection: collection to put into request
    :param type_: type of the request {'usual', 'values'}
    :return: collection`s query
    """
    types = {
        'usual':  '"{item}",',
        'values': "'{item}',",
    }
    txt = ''
    for item in collection:
        if type(item) is float:
            txt += '{item},'.format(item=item)
        elif type(item) is int:
            txt += '{item},'.format(item=item)
        elif type(item) is str:
            txt += types[type_].format(item=item)
        elif type(item) is bool:
            txt += '{item},'.format(item='TRUE' if item else 'FALSE')
        elif type(item) is tuple:
            txt += '({item}),'.format(item=create_db_query(item, type_=type_))
        # TODO DEFAULTS
        elif item is None:
            txt += 'DEFAULT,'
    return txt[:-1]


def create_conditions(conds: dict, operator: str) -> str:
    """
    Create right postgres conditions using WHERE operator
    :param conds:conditions
    :param operator: AND or OR {and, or}
    :return: conditions query
    """
    txt = ''
    for key, value in conds.items():
        txt += '{key} = {value}  {operator}'.format(
            key      = create_db_query((key, ), type_='usual'),
            value    = create_db_query((value, ), type_='values'),
            operator = operator.upper(),
        )
    return txt[:-4]
