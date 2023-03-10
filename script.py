from utils.DataBaseManager import DBManager
from utils.FileManager import FileManager

fm = FileManager()
db_configuration = fm.get_data_from_json_file(file='configuration/db_access_configuration.json')

database_name = 'messenger'
table_name = 'users'
create_data_base = f'CREATE DATABASE {database_name}'
create_table = f'CREATE TABLE {database_name}.{table_name} ' \
               f'(id int AUTO_INCREMENT KEY , name varchar(50), password varchar(50), mail varchar(50))'

create_data_in_table_1 = f'INSERT INTO {database_name}.{table_name} ' \
                         f'(NAME, PASSWORD, MAIL) VALUE("Shurik", "12345", "shurik@mail.com")'

create_data_in_table_2 = f'INSERT INTO {database_name}.{table_name} ' \
                         f'(NAME, PASSWORD, MAIL) VALUE("Sima", "12345", "sima@mail.com")'

commands_list = [create_data_in_table_1, create_data_in_table_2]

users_data = [
    {
        "user_name": "Sima",
        "mail": "sima@mail.com",
        "password": "12345"
    },

    {
        "user_name": "Shurik",
        "mail": "shurik@mail.com",
        "password": "12345"
    }
]

db_manager = DBManager(
    address=db_configuration['address'],
    user='root',
    password=db_configuration['password'],
    db_name=database_name
)


def create_database():

    databases = db_manager.get_databases_list()
    if database_name not in databases:
        db_manager.exec_query_for_creating(create_data_base)
    else:
        print(f'The database "{database_name}" already exists')


def create_table_users():
    tables = db_manager.get_tables_list(database=database_name)
    if tables is None:
        db_manager.exec_query_for_creating(query=create_table)
    elif table_name not in tables:
        db_manager.exec_query_for_creating(query=create_table)
    else:
        print(f'The table "{table_name}" already exists')


def generation_user_data():

    new_db_manager = DBManager(
        address=db_configuration['address'],
        user='root',
        password=db_configuration['password'],
        db_name=database_name
    )

    users_list = db_manager.get_data(table_name=table_name)

    if len(users_list) == 0:
        for user in users_data:

            query = f'INSERT INTO {database_name}.{table_name} (NAME, PASSWORD, MAIL) VALUE("{user["user_name"]}", ' \
                    f'"{user["password"]}", "{user["mail"]}")'
            new_db_manager.exec_query_for_creating(query)
    else:
        for user_from_user_data in users_data:
            for user_from_user_list in users_list:
                if user_from_user_data["mail"] in user_from_user_list:
                    print(f'The user: {user_from_user_data} already exist')
                    continue


create_database()
create_table_users()
generation_user_data()
