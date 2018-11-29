import psycopg2
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor() # create a cursor
        cur.execute('select * from "Places"') # execute command

        row = cur.fetchone() # get first row

        # print every row until there are any
        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close() # close the connection

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
