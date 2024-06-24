import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = <your-link-to-db>

def connect():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.FloerianBOT
    my_collection = db["MemberStats"]
    return client, my_collection

def send_ping(client):
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def user_exists(collection, name):
    print(name)
    user = collection.find_one({"name": name})
    return user is not None


def update_user(name, value: int, collection):
    current_user = collection.find_one({"name": name})
    current_points = int(current_user["points"])

    collection.update_one({"name": name}, { "$set": {"points": (current_points+value)}})
    return


def update_database(name, value: int):
    client, collection = connect()
    send_ping(client)

    if user_exists(collection, name):
        print(f"Updating {name}...")
        update_user(name, value, collection)
    else:
        new_user = {"name": f"{name}", "points": f"{value}"}
        collection.insert_one(new_user)


def find_user(name):
    client, collection = connect()
    send_ping(client)

    if user_exists(collection, name):
        user = collection.find_one({"name": name})
        return int(user["points"])
    else:
        return None


def show_leaderboard():
    client, collection = connect()
    scores = []

    all_records = collection.find()
    for doc in all_records:
        username = doc["name"]
        points = doc["points"]
        scores.append(tuple((username, points)))
    
    scores.sort(key = lambda item: item[1], reverse=True)

    message_content = f""
    for i in range(10):
        try:
            message_content += f"**{i+1}.** {scores[i][0]} | *{scores[i][1]}€*\n"
        except Exception as e:
            pass
    
    return message_content