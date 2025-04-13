from passlib.context import CryptContext

class KuroTools:
    def __init__(self):
        pass
    def filter2List(self, list1, data_list, keys):
        """
        List1 : Expected filter list
        List2 : All data list
        keys : keys for comparement filtering (if list1[keys] == list2[keys])
        """
        list1 = {item[keys] for item in list1}
        return [item for item in data_list if item.get(keys) in list1]

    def hasherContext(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.hasherContext().verify(plain_password, hashed_password)

    def hash_password(self, password):
        return self.hasherContext().hash(password)