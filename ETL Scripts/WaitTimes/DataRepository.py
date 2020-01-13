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
        sql = '''SELECT \'Connection test passed\''''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            result = result + '\n' + str(row)
        self.connection.commit()
        return result

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def format_wait_time_data(self, data):
        counter = 0
        queries = []
        for parkname, attractions in data.items():
            for attraction, rows in attractions.items():
                for row in rows:
                    if counter == 0:
                         query = 'INSERT INTO \"Warehouse\".\"AttractionWaitTimesBuffer\"\nVALUES\n'
                    query = query + f'\t($${parkname}$$, $${attraction}$$, $${row["timestamp"]}$$, {row["wait_time"]})'
                    counter = counter + 1
                    if counter >= self.rows_per_insert:
                        counter = 0
                        queries.append(query)
                        query = ""
                    else:
                        query = query + ',\n'
        return queries  

    def format_extended_wait_time_data(self, data):
        queries = []
        counter = 0
        for row in data:
            if counter == 0:
                query = 'INSERT INTO \"Warehouse\".\"AttractionWaitTimesExpanded\" (\"attractionid\",\"timestamp\", \"waittime\") \nVALUES\n'
            query = query + f'\t($${row[0]}$$, $$\'{row[1]}\'$$, $${row[2]}$$)'
            counter = counter + 1
            if counter >= self.rows_per_insert:
                counter = 0
                queries.append(query)
                query = ""
            else:
                query = query + ',\n'
        return queries   






