from bson.objectid import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError, ConnectionFailure

uri = f"mongodb://localhost:27017/"

# Підключення до бази даних
try:
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client["task2"]
    collections = db["cats"]
    client.admin.command("ismaster")
    print("Підключення до бази даних успішне")
except ConnectionFailure:
    print("Помилка підключення до бази даних")


def read():
    return db.cats.find()


def create_cat():
    try:
        name = input("введіть ім'я котика: ")
        age = input("введіть вік котика: ")
        features = input("введіть характеристики котика через кому: ").split(",")
        cat = {"name": name, "age": age, "features": features}
        collections.insert_one(cat)
        print("Котика успішно додано")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою: {e}")
    except ValueError as e:
        print(f"Помилка при додаванні котика: {e}")


def read_all():
    cats = list(collections.find({}))
    for cat in cats:
        print(cat)


def read_cat_by_name():
    name = input("Введіть ім'я котику для пошуку: ")
    cat = collections.find_one({"name": name})
    print(cat)


def update_cat_age():
    try:
        name = input("Введіть ім'я котика для оновлення віку: ")
        age = input("Введіть новий вік котика: ")
        res = collections.update_one({"name": name}, {"$set": {"age": age}})
        if res.modified_count > 0:
            print("Вік котика успішно оновлено")
        else:
            print("Котика з таким ім'ям не знайдено")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою: {e}")
    except ValueError as e:
        print(f"Помилка при оновленні віку котика: {e}")


def add_feature():
    try:
        name = input("Введіть ім'я котика для додавання характеристик: ")
        features = input("Введіть нову характеристику котика: ")
        res = collections.update_one(
            {"name": name}, {"$addToSet": {"features": features}}
        )
        if res.modified_count > 0:
            print("Характеристику котика успішно додано")
        else:
            print("Котика з таким ім'ям не знайдено")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою: {e}")
    except ValueError as e:
        print(f"Помилка при додаванні характеристик котика: {e}")


def delete_cat():
    try:
        name = input("Введіть ім'я котика для видалення: ")
        res = collections.delete_one({"name": name})
        if res.deleted_count > 0:
            print("Котика успішно видалено")
        else:
            print("Котика з таким ім'ям не знайдено")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою: {e}")
    except ValueError as e:
        print(f"Помилка при видаленні котика: {e}")


def delete_all():
    try:
        res = collections.delete_many({})
        if res.deleted_count > 0:
            print("Всі котики успішно видалені")
        else:
            print("Немає котів для видалення")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою: {e}")


if __name__ == "__main__":
    create_cat()
    create_cat()
    create_cat()
    create_cat()
    read_all()
    read_cat_by_name()
    update_cat_age()
    add_feature()
    delete_cat()
    read_all()
    delete_all()
    read_all()

