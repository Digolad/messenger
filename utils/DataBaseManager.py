import mysql.connector
from mysql.connector import Error


class DBManager:

    def __init__(self, address: str, user: str, password: str, db_name: str = 'messanger_db'):
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

    def find_a_match(self, table_name: str, data: str):
        query = f'SELECT * FROM {self.db_name}.{table_name} WHERE {table_name}.mail LIKE "{data}"'
        return self.exec_query(query)

    def get_data(self, table_name: str) -> list:
        query = f'SELECT * FROM {self.db_name}.{table_name}'
        return self.exec_query(query)

    def exec_query(self, query) -> list:
        cursor = self.try_to_create_connection.cursor()

        try:
            cursor.execute(query)
            self.try_to_create_connection.commit()
            record = cursor.fetchall()

            print('The query was sent success!')
            print(f'The query: {query}')
            return record

        except Error as err:
            print(f"Something went wrong: {err}")
            return None

    # def insert_varibles_into_user_table(self, mySql_insert_query, record: list):
    #     cursor = self.try_to_create_connection.cursor()
    #
    #     try:
    #         cursor.execute(mySql_insert_query, record)
    #         self.try_to_create_connection.commit()
    #         print("Record inserted successfully into Laptop table")
    #
    #     except mysql.connector.Error as error:
    #         print("Failed to insert into MySQL table {}".format(error))
    #
    #     finally:
    #         if self.try_to_create_connection.is_connected():
    #             cursor.close()
    #             self.try_to_create_connection.close()
    #             print("MySQL connection is closed")



