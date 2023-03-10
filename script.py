from utils.DataBaseManager import DBManager
from utils.FileManager import FileManager

from datetime import datetime
from faker import Faker
import random
import os
import hashlib

fm = FileManager()
db_configuration = fm.get_data_from_json_file(file='configuration/db_access_configuration.json')

database_name = 'messenger'
create_data_base = f'CREATE DATABASE {database_name}'

create_user_table = f'CREATE TABLE {database_name}.user ' \
               f'(id int AUTO_INCREMENT KEY , name varchar(50), mail varchar(50))'

create_authentication_table = f'CREATE TABLE {database_name}.authentication ' \
                              f'( Id INT PRIMARY KEY AUTO_INCREMENT, ' \
                              f'user_id INT, ' \
                              f'hash_password VARCHAR(250) NULL DEFAULT NULL, ' \
                              f'token VARCHAR(50) NULL DEFAULT NULL, ' \
                              f'authentication_state VARCHAR(50) NULL DEFAULT NULL, ' \
                              f'FOREIGN KEY (user_id)  REFERENCES messenger.user (Id));'

create_user_info_table = f'CREATE TABLE {database_name}.user_info ' \
                         f'( Id INT PRIMARY KEY AUTO_INCREMENT, ' \
                         f'user_id INT, ' \
                         f'status VARCHAR(50), ' \
                         f'birthday VARCHAR(50), ' \
                         f'edited_time VARCHAR(50), ' \
                         f'FOREIGN KEY (user_id)  REFERENCES messenger.user (Id));'

create_avatar_table = f'CREATE TABLE {database_name}.avatar ' \
                         f'( Id INT PRIMARY KEY AUTO_INCREMENT, ' \
                         f'user_id INT, ' \
                         f'avatar VARCHAR(50) NULL DEFAULT NULL, ' \
                         f'date_load VARCHAR(50), ' \
                         f'FOREIGN KEY (user_id)  REFERENCES messenger.user (Id));'


def connection():
    return DBManager(
        address=db_configuration['address'],
        user='root',
        password=db_configuration['password'],
        db_name=database_name
    )


def create_database():
    db_manager = connection()

    databases = db_manager.get_databases_list()
    if database_name not in databases:
        db_manager.exec_query_for_creating(create_data_base)
    else:
        print(f'The database "{database_name}" already exists')


def create_tables():
    db_manager = connection()

    tables = {
        "user": create_user_table,
        "authentication": create_authentication_table,
        "user_info": create_user_info_table,
        "avatar": create_avatar_table
    }

    db_tables = db_manager.get_tables_list(database=database_name)

    for table in tables:
        if table not in db_tables or db_tables is None:
            db_manager.exec_query_for_creating(query=tables[table])
        else:
            print(f'The table: "{table}" already exist')


def add_data_in_user_table(user_name, mail):
    return f'INSERT INTO {database_name}.user (NAME, MAIL) VALUE("{user_name}", ' \
                    f'"{mail}")'


def add_data_in_user_info_table(user_id, status, birthday, edited_time, method_mode='insert'):
    if method_mode == 'insert':
        return f'INSERT INTO {database_name}.user_info (USER_ID, STATUS, BIRTHDAY, EDITED_TIME)' \
               f' VALUE("{user_id}", "{status}","{birthday}","{edited_time}")'
    # else:
    #     return f'UPDATE {database_name}.user_info SET avatar = {avatar},' \
    #                 f'status = {status}, birthday = {birthday}, ' \
    #                 f'edited_time = {edited_time} WHERE user_id = {user_id}'


def add_data_in_avatar_table(user_id, avatar, date_load):
    return f'INSERT INTO {database_name}.avatar (USER_ID, AVATAR, DATE_LOAD) ' \
           f'VALUE("{user_id}", "{avatar}","{date_load}")'


def add_data_in_authentication_table(user_id, hash_password, token, authentication_state):
    return f'INSERT INTO {database_name}.authentication (USER_ID, HASH_PASSWORD, TOKEN, AUTHENTICATION_STATE)' \
           f' VALUE("{user_id}", "{hash_password}", "{token}","{authentication_state}")'

# def generation_user_data():
#
#     db_manager = connection()
#
#     users_list = db_manager.get_data(table_name=table_name)
#
#     if len(users_list) == 0:
#         for user in users_data:
#
#             query = f'INSERT INTO {database_name}.{table_name} (NAME, PASSWORD, MAIL) VALUE("{user["user_name"]}", ' \
#                     f'"{user["password"]}", "{user["mail"]}")'
#
#             new_db_manager.exec_query_for_creating(query)
#     else:
#         for user_from_user_data in users_data:
#             for user_from_user_list in users_list:
#                 if user_from_user_data["mail"] in user_from_user_list:
#                     print(f'The user: {user_from_user_data} already exist')
#                     continue


users_data = [
    {
        "user_name": "Sima",
        "mail": "sima@mail.com",
        "hash_password": "12345",
        "avatar": "storage/users/imgs/avatar1.png",
        "birthday": "1977-05-17",
        "edited_time": "2012-12-12 00:00:00"
    },

    {
        "user_name": "Shurik",
        "mail": "shurik@mail.com",
        "hash_password": "12345",
        "avatar": "storage/users/imgs/avatar2.png",
        "birthday": "1977-05-17",
        "edited_time": "2012-12-12 00:00:00"
    }
]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


fake_count = 4
the_faker = Faker()
fake_mail = 'account'
password = '12345'
hash_password = hash_password(password)

# Getting images list
folder_name = 'storage/users/imgs'
path = os.path.abspath(folder_name)
files = os.listdir(path)
current_datetime = str(datetime.fromtimestamp(1576280665))


for i in range(0, fake_count):
    users_data.append(
        {
            "user_name": the_faker.name(),
            "mail": fake_mail+str(i)+'@test.com',
            "hash_password": hash_password,
            "avatar": folder_name + '/' +files[random.randrange(1, len(files))],
            "birthday": the_faker.date(),
            "edited_time": current_datetime
        }
    )

    # print(i, 'Name: ' + the_faker.name())
    # print('Mail: ' + fake_mail+str(i)+'@test.com')
    # print('Password: ', password)
    # avatar = files[random.randrange(1, len(files))]
    # print('Avatar: ', folder_name+'/'+avatar)
    # print('birthday', the_faker.date())
    # print(current_datetime)


def generation_user_data():
    def get_data_like(table, column_name, data):
        return db_manager.find_a_match(table_name=table, column_name=column_name, data=data)

    db_manager = connection()
    for user in users_data:
        match_user_data = get_data_like(table='user', column_name='mail', data=user['mail'])
        if len(match_user_data) == 0:
            db_manager.exec_query_for_creating(query=add_data_in_user_table(
                user_name=user['user_name'],
                mail=user['mail']
            ))
            match_user_data = get_data_like(table='user', column_name='mail', data=user['mail'])
            user_id = match_user_data[0][0]
        else:
            user_id = match_user_data[0][0]

        match_user_info_data = get_data_like(table='user_info', column_name='user_id', data=user_id)
        if len(match_user_info_data) == 0:
            db_manager.exec_query_for_creating(query=add_data_in_user_info_table(
                user_id=user_id,
                status='test generation',
                birthday=user['birthday'],
                edited_time=user['edited_time'],
                method_mode='insert'
                ))

        match_avatar_data = get_data_like(table='avatar', column_name='user_id', data=user_id)
        if len(match_avatar_data) == 0:
            db_manager.exec_query_for_creating(query=add_data_in_avatar_table(
                user_id=user_id,
                avatar=user['avatar'],
                date_load=user['edited_time']
            ))

        match_authentication_data = get_data_like(table='authentication', column_name='user_id', data=user_id)
        if len(match_authentication_data) == 0:
            db_manager.exec_query_for_creating(query=add_data_in_authentication_table(
                user_id=user_id,
                token=0,
                hash_password=user['hash_password'],
                authentication_state='Do not'
            ))


create_database()
create_tables()
generation_user_data()
