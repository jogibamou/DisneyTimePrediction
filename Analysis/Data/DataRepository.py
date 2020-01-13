import psycopg2
from psycopg2 import connect as pg_connect

# Main purpose of this module is to push data onto the database

class DataRepository:
    def __init__(self, db_info, rows_per_insert):
        # Set up connection to database
        self.connection = pg_connect(
            database=db_info["database"],
            user=db_info["username"],
            password=db_info["password"],
            host=db_info["host"],
            port=db_info["port"]
        )
        self.rows_per_insert = rows_per_insert

    def __del__(self):
       self.connection.close()

    def test_connection(self):
        result = ""
        cursor = self.connection.cursor()
        sql = '''SELECT \'test\''''
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(tuple(row))
        self.connection.commit()
        return "DB Connection established" if result[0][0] == "test" else "DB Connection failed"
   
    def execute_query_return_rows(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(tuple(row))
        self.connection.commit()
        return result

