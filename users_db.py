class UsersDB():

    users_list = [{"user": "Sakthi", "password": "sakthi",
                           "mobile": '044-45985645'}, {"user": "prakash", "password": "prakash", "mobile": '85497826352'}]

    def read_db(self, user_name: str, password: str):

        for i in self.users_list:
            if (i["user"] == user_name and i["password"] == password):
                return True
        return False

    def write_db(self, user_name: str, password: str, mobile: str):

        self.users_list.append(
            {"user": user_name, "password": password, "mobile": mobile})

        return True

    def getNumber(self, user):
        for i in self.users_list:
            if i["user"] == user:
                return i["mobile"]
