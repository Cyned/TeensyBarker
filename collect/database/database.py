import psycopg2
from database.config import config


def execute(query):
    """ Connect to the PostgreSQL database server and execute the query"""
    conn = None
    result = []
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()  # create a cursor
        cur.execute(query)  # execute the query

        try:
            row = cur.fetchone()  # get first row

            # print every row until there are any
            while row is not None:
                result.append(row)
                row = cur.fetchone()
        except:
            pass

        conn.commit()
        cur.close()  # close the connection

    except (Exception, psycopg2.DatabaseError) as error:
        print('Error')
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')

    return result
