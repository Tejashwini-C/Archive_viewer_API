class userCreation:
    @staticmethod
    def create_user_payload(name, username,email,roleId):
        return {
            "name": name,
            "username": username,
            "email": email,
            "roleId": roleId
}
    @staticmethod
    def update_password(username, newpsswrd):
        from test_02_userCreation import TestUserCreation
        old_password = TestUserCreation.user_password # Assuming you have a way to get the old password
        return {
        "username": username,
        "oldpsswrd": old_password,
        "newpsswrd": newpsswrd
        }
 
    @staticmethod
    def login_data(username, psswrd):
        return {
            "username": username,
            "psswrd": psswrd
        }