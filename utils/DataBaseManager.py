import mysql.connector
from mysql.connector import Error


class DBManager:

    def __init__(self, address: str, user: str, password: str, db_name: str = 'messenger'):
        self.address = address
        self.user = user
        self.password = password
        self.try_to_create_connection = self.create_connection()
        self.db_name = db_name

    def __del__(self):
        self.try_to_create_connection.close()
        print('Closed DB connection.')

    def create_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.address,
                user=self.user,
                password=self.password
            )
            print('Connected to DB success')

        except Error as err:
            print(f"Something went wrong: {err}")

        return connection

    def update(self):
        pass

    def delete_from_table(self):
        pass

    def find_a_match(self, table_name: str, column_name: str, data: str):
        query = f'SELECT * FROM {self.db_name}.{table_name} WHERE {table_name}.{column_name} LIKE "{data}"'
        return self.exec_query_for_reading(query)

    def get_data(self, table_name: str) -> list:
        query = f'SELECT * FROM {self.db_name}.{table_name}'
        return self.exec_query_for_reading(query)

    def exec_query_for_creating(self, query):
        cursor = self.try_to_create_connection.cursor()

        try:
            cursor.execute(query)
            self.try_to_create_connection.commit()
            #cursor.fetchall()
            print(f'The query "{query}" was sent success!')

        except Error as err:
            print(f"Something went wrong: {err}")
            return None

    def exec_query_for_reading(self, query):
        cursor = self.try_to_create_connection.cursor()

        try:
            cursor.execute(query)
            record = cursor.fetchall()
            print(f'The query "{query}" was sent success!')
            return record

        except Error as err:
            print(f"Something went wrong: {err}")
            return None

    def get_databases_list(self) -> list:
        query = 'SHOW DATABASES'
        data = self.exec_query_for_reading(query)
        empty_list = []
        for item in data:
            empty_list.append(item[0])
        return empty_list

    def get_tables_list(self, database) -> list:
        query = f'SHOW TABLES FROM {database}'
        data = self.exec_query_for_reading(query)

        if data is None:
            return None

        empty_list = []
        for item in data:
            empty_list.append(item[0])
        return empty_list

