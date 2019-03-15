import json


class RealityDB:
    def __init__(self):
        with open("DataBaseReality.txt", mode='r') as file:
            database = file.read()
            self.database = json.loads(database)

    def database_commit(self):  # сохранение изменений в базе
        with open("DataBaseReality.txt", mode='w') as file:
            database = json.dumps(self.database)
            file.write(database)

    def change_database(self, username, reality=None, properties=None, mode='del'):
        if mode == 'del' and reality is None:  # условие полной очистки всей недвижимости пользователя
            self.database[username] = {}
        elif mode == 'del' and reality:  # условие для очистки определённой недвижимости
            del self.database[username][reality]
        elif mode == 'add' and reality and properties:  # условие добавления недвижимости
            self.database[username][reality] = properties
        self.database_commit()

    def add_user(self, username):
        self.database[username] = {}
        self.database_commit()

