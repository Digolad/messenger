from utils.DataBaseManager import DBManager
from utils.FileManager import FileManager

fm = FileManager()
db_configuration = fm.get_data_from_json_file(file='configuration/db_access_configuration.json')

database_name = 'test'
table_name = 'users'
create_data_base = f'CREATE DATABASE {database_name}'
create_table = f'CREATE TABLE {database_name}.{table_name} ' \
               f'(id int AUTO_INCREMENT KEY , name varchar(50), password varchar(50), mail varchar(50))'

create_data_in_table_1 = f'INSERT INTO {database_name}.{table_name} ' \
                         f'(NAME, PASSWORD, MAIL) VALUE("Shurik", "12345", "shurik@mail.com")'

create_data_in_table_2 = f'INSERT INTO {database_name}.{table_name} ' \
                         f'(NAME, PASSWORD, MAIL) VALUE("Sima", "12345", "sima@mail.com")'

commands_list = [create_data_base, create_table, create_data_in_table_1, create_data_in_table_2]

db_manager = DBManager(
    address=db_configuration['address'],
    user='root',
    password=db_configuration['password'],
    db_name=database_name
)

for cm in commands_list:
    db_manager.exec_query(query=cm)
