import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient


def get_db():
    """ setup connection with Bili_impression database """
    load_dotenv()
    url = os.getenv('MONGODB_URL')
    client = MongoClient(url)
    return client.get_database("Bili_impression")


def insert_document(collection, docu):
    """ insert documents in given collection """
    db = get_db()
    records = db.get_collection(collection)
    records.insert_one(docu)


def insert_dict(collection, dic):
    """
    Insert books or authors collection in database
    :param collection: the collection to insert
    :param dic: the dictionary that need to be inserted
    :return: no return value
    """
    db = get_db()
    records = db.get_collection(collection)
    records.insert_many(dic)


def update_dicts(collection, identifier, content):
    """
    Update documentations in a given collection
    :param collection: the collection where document to be updated is.
    :param identifier: the identifier of the documentation we want to find
    :param content: the content to update
    :return: no return value
    """
    db = get_db()
    records = db.get_collection(collection)
    print(content)
    result = records.update_one(
        identifier,
        {"$set": content},
        upsert=True
    )
    print("matched documentation: " + str(result.matched_count))
    print("modified documentation: " + str(result.modified_count))


def get_documents_json(collection, identifier):
    """
    find documentations specified by the identifier and output a json data
    :param collection: the collection where the data is
    :param identifier: identifier of the documents we want, {} means locate the whole collection
    :return: json file of selected documentations
    """
    db = get_db()
    records = db.get_collection(collection)
    data = records.find(identifier)
    file = {collection: []}
    for item in data:
        item.pop("_id")
        file[collection].append(item)
    return json.dumps(file)


def download_collection(collection, identifier, name):
    """
    download books collection or authors collection
    :param collection: selected collection
    :param identifier: identifier of the documents we want to download;
    empty({}) means selected all documents in given collection
    :param name: file name of downloaded json
    :return: JSON file of the collection
    """
    json_file = get_documents_json(collection, identifier)
    load_dotenv()
    file_root = os.getenv('FILE_ROOT')
    with open(file_root + name + ".json", "w") as output:
        output.write(json_file)


def clean(collection, identifier):
    """
    delete specific documents in given collection
    :param collection: selected collection
    :param identifier: identifier of the documents we want to delete;
    empty({}) means selected all documents in given collection
    :return: no return value
    """
    db = get_db()
    records = db.get_collection(collection)
    return records.delete_many(identifier).deleted_count
