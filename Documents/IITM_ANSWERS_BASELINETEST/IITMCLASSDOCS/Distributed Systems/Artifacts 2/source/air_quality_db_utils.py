def insert_single(collection, data):
    try:
        if data is None:
            print("No data is available.")
        else:
            result = collection.insert_one(data)
            print(result.inserted_id)
            print("Query successful")
            return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def insert_multiple(collection, data):
    try:
        if data is None:
            print("No data is available.")
        else:
            result = collection.insert_many(data)
            print(result.inserted_ids)
            print("Query successful")
            return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def find_single(collection, data):
    try:
        if data is None:
            print("No data is available. Please provide the data.")
        else:
            result = collection.find_one(data)
            print("Query successful")
            return result
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def find_multiple(collection, data):
    try:
        if data is None:
            print("No data is available. Please provide the data.")
        else:
            result = collection.find(data)
            print("Query successful")
            return result
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def delete_single(collection, data):
    try:
        if data is None:
            print("No data is available. Please provide the data.")
        else:
            result = collection.delete_one(data)
            print("Query successful")
            return result
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def delete_multiple(collection, data):
    try:
        if data is None:
            print("No data is available. Please provide the data.")
        else:
            result = collection.delete_many(data)
            print("Query successful")
            return result
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def single_update(collection, query_data, update_data):
    try:
        if update_data is None:
            print("No data is available. Please provide the data.")
        else:
            result = collection.update_one(query_data, update_data)
            print("Query successful")
            return result
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def aggregate_data(collection, query):
    try:
        result = collection.aggregate(query)
        print("Query successful")
        return result

    except Exception as e:
        print("An exception occurred ::", e)
        return False
