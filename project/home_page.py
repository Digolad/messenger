from utils.DataBaseManager import DBManager
from utils.FileManager import FileManager


class HomePage:
    """
    Describing all that users can do on the Home page.
    """
    fm = FileManager()
    db_configuration = fm.get_data_from_json_file(file='configuration/db_access_configuration.json')
    db_manager = DBManager(
        address=db_configuration['address'],
        user=db_configuration['login'],
        password=db_configuration['password']
        )

    def get_users_data(self):
        return self.db_manager.get_data(table_name='users')

    def get_user_by_mail(self, mail: str):
        data = self.db_manager.find_a_match(table_name='users', data=mail)
        user_data = {}
        if len(data) > 0:
            """
            create User module?
            """
            user_data['name'] = data[0][1]
            user_data['password'] = data[0][2]
            user_data['mail'] = data[0][3]
            return user_data
        return None
