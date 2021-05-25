import pymongo
import ssl


# Класс "База данных"
class Database:
    STRING = None
    CLIENT = None
    DB = None
    COLLECTION = None

    # ---- ОСНОВА ----

    def __init__(self, string_db):
        self.STRING = string_db
        self.CLIENT = pymongo.MongoClient(self.STRING, ssl=False, ssl_cert_reqs=ssl.CERT_NONE)

    def enter_database(self, name_database):
        self.DB = self.CLIENT[name_database]  # База данных

    def enter_collection(self, name_collection):
        self.COLLECTION = self.DB[name_collection]  # Коллекция

    # ---- ДОПОЛНИТЕЛЬНО ----

    # Добавление нового продукта в коллекцию
    def save(self, data):
        _id = self.COLLECTION.save(data)
        return _id

    # Проверяем есть ли документы с содержимым "data" в коллекции
    def check_documents(self, data):
        documents = []
        _id = []
        temp = self.COLLECTION.find(data)
        for item in temp:
            documents.append(item)
            _id.append(item["_id"])
        if not documents:
            return False
        else:
            return _id