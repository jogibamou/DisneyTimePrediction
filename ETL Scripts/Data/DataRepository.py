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
        self.schema_name = "Warehouse"

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
   
    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def insert_rows_into_table(self, table_name, columns, rows):
        if(len(columns) == 0):
            raise ValueError("Must provide column list")
        if(len(rows) == 0):
            raise ValueError("Must provide at least one row of data to insert")
        if(len(columns) != len(rows[0])):
            raise ValueError("Number of rows and columns must match")
        queries = []
        accumulator = []
        counter = 0
        for row in rows:
            accumulator.append(row)
            if( len(accumulator) == self.rows_per_insert or len(accumulator) + self.rows_per_insert * counter == len(rows)):
                counter = counter + 1
                print(f'Creating insert statement #{counter}')
                queries.append(self.__create_insert_statement__(table_name, columns, accumulator))
                accumulator = []
        counter = 0
        for query in queries:
            counter = counter + 1
            print(f'Executing query #{counter}') # should change these print statements to use a passed-in logger thing
            self.execute_query(query)
        print('Query execution completed!')

    # This seems to be slow as shit but it works
    def __create_insert_statement__(self, table_name, columns, rows):
            query = f'INSERT INTO "{self.schema_name}"."{table_name}"\n'
            query = query + '('
            for col in columns:
                query = query +'\n\t' + col + ','
            query = query[:-1] + '\n)'
            query = query + '\nVALUES'
            for row in rows:
                query = query + '\n\t('
                for value in row:
                    query = query + str(value) + ','
                query = query[:-1] + '),'
            query = query[:-1]
            return str(query) 