import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "YOUR-URI"

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


def create_new_user(name):
    client, collection = connect()
    new_user = {"name": f"{name}", "points": 0, "chance": 30, "upgrade-chance": False}
    collection.insert_one(new_user)


def user_exists(name, collection=None):
    client, collection = connect()
    user = collection.find_one({"name": name})
    return user is not None


def update_user(name, value: int, collection=None):
    client, collection = connect()
    current_user = collection.find_one({"name": name})
    current_points = int(current_user["points"])

    collection.update_one({"name": name}, { "$set": {"points": (current_points+value)}})
    return


def update_database(name, value: int):
    client, collection = connect()
    send_ping(client)

    if user_exists(name, collection):
        print(f"Updating {name}...")
        update_user(name, value, collection)
    else:
        try:
            create_new_user(name)
        except Exception as e:
            print(e)


def find_user(name):
    client, collection = connect()

    if user_exists(name, collection):
        user = collection.find_one({"name": name})
        return int(user["points"])
    else:
        return None


def show_leaderboard(user_calling_command):
    scores = find_all_users()
    scores.sort(key = lambda item: item[1], reverse=True)

    user_keys = []
    for i in range(len(scores)):
        user_keys.append(scores[i][0])
    
    try:
        user_position = list(user_keys).index(user_calling_command)
    except:
        create_new_user(user_calling_command)
        message_content = "You are not registered in our Database yet, will create new Account just for you..."
        return message_content

    message_content = f""
    for i in range(10):
        try:
            message_content += f"**{i+1}.** {scores[i][0]} | *{int(scores[i][1]):,}€*\n"
        except Exception as e:
            pass
    message_content += f"\nYour Position: **{user_position+1}.** {user_calling_command} | *{int(scores[user_position][1]):,}€*"
    return message_content


def find_all_users():
    client, collection = connect()
    users = []

    all_records = collection.find()
    for doc in all_records:
        username = doc["name"]
        points = doc["points"]
        chance = doc["chance"]
        users.append(tuple((username, points, chance)))
    return users


def upgrade_chance(name):
    client, collection = connect()
    current_user = collection.find_one({"name": name})
    upgrade_cost = 50000

    if current_user["upgrade-chance"] is True:
        message_content = f"{name} already bought this Upgrade."
        return message_content
    
    if current_user["points"] < upgrade_cost:
        message_content = f"{name} does not have enough money to buy this upgrade.\n`{upgrade_cost:,}€` are required but {name} only has `{current_user["points"]:,}€`."
    else:
        collection.update_many({"name": name}, {"$set": {"chance": 20, "upgrade-chance": True, "points": (current_user["points"]-upgrade_cost)}})
        message_content = f"{name} managed to buy the Chance Upgrade for {upgrade_cost:,}€!"
    return message_content


def update_all_users_DEBUG():
    client, collection = connect()
    all_users = find_all_users()

    for i in range(len(all_users)):
        collection.update_one({"name": all_users[i][0]}, {"$set": {"chance": 30}})