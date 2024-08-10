import random
class User:
    def __init__(self, name, money) -> None:
        self.name = name
        self.money = money

def casino(option, user, user_money):
    if option == "poor":
        profit = 500; cost = -75; chance = 15
    elif option == "normie":
        profit = 1500; cost = -120; chance = 10
    elif option == "rich":
        profit = 5000; cost = -450; chance = 5
    
    if user_money < cost:
        content = f"{user} does not have enough money to use the casino functions."; money_change = 0
        return content, money_change

    num = random.randint(0,100)
    if num <= chance:
        money_change = profit
        content = f"{user} Won in the Casino! {user} has won {profit}€!"
    else:
        money_change = cost
        content = f"{user} did not win in the Casino, losing {cost}€."
    return content, money_change


def steal_from_user(user, users):
    while True:
        rdm_user = random.choice(users)
        if rdm_user == user:
            random.choice(users)
        else:
            break

    num = random.randint(1,100)
    if num < 61:
        money_change = random.randint(80,240)
        msg_content = f"{user} successfully stole **{money_change}€** from {rdm_user}!"
    else:
        money_change = random.randint(-90,-30)
        msg_content = f"{user} couldn't steal any money from {rdm_user}, losing {money_change}€ instead."
    return msg_content, money_change

def break_into_house(user):
    items = [
        ("Smartphone", 100),
        ("TV", 120),
        ("Shirt", random.randint(10,25)),
        ("Pants", random.randint(10,25)),
        ("Hoodie", random.randint(10,25)),
        ("Shoes", random.randint(20,35)),
        ("Console", 90),
        ("Wallet", random.randint(10,225)),
    ]

    reasons = [
        "Tripped, fell on their face and passed out.",
        "A neighbor heard a strange noise and contacted the police, which has arrested you and fined you.",
        "The home owner was at home and had a gun by his side, robbing you instead before you flee out of the house."
    ]

    num = random.randint(1,100)
    money_change = 0

    if num < 41:
        received_items = []

        for i in range(random.randint(1,5)):
            received_items.append(items[random.randint(0,len(items)-1)])
        
        msg_content = f"{user} robbed a house, he received the following items:\n"

        for item in received_items:
            msg_content += f"\n*{item[0]}:*\t**{item[1]}€**"
            money_change += item[1]
        
        msg_content += f"\n\nTotal: **{money_change}€**"

    else:
        max_iteration = len(reasons)-1
        money_change = random.randint(-150,-80)
        msg_content = f"{user} was not able to rob the house.\nReason: {reasons[random.randint(0,max_iteration)]}\nMoney lost: {money_change}€"
    
    return msg_content, money_change


def steal_from_another_user(users, user_calling_command, option_name, amount):
    user_keys = []
    for i in range(len(users)):
        user_keys.append(users[i][0])
    
    user_option_position = list(user_keys).index(str(option_name))
    user_position = list(user_keys).index(str(user_calling_command))

    if amount > users[user_option_position][1]:
        message_content = f"{option_name} does not have enough money to be robbed for {amount}€."
        return None, message_content
    
    elif amount > users[user_position][1]:
        message_content = f"{user_calling_command} would have less than 0 money if they fail, you probably shouldn't do that :)"
        return None, message_content
    
    else:
        chance_to_rob = users[user_option_position][2]
        rdm_num = random.randint(0,100)

        if rdm_num < chance_to_rob:
            message_content = f"You managed to rob {option_name} for {amount}€!"
            return True, message_content
        
        else:
            message_content = f"You failed robbing {option_name} for {amount}€!\nLosing -{amount}€ instead!"
            return False, message_content


def roulette_decider(arg):
    winning_num = random.randint(0,36)
    multiplicator = 2
    win = False
    
    if arg == "Black" or arg == "Red":
        blacks = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
        red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]

        if winning_num in blacks and arg == "Black":
            win = True
        elif winning_num in red and arg == "Red":
            win = True

        
    if arg == "Even" or arg == "Odd":
        if winning_num % 2 == 0 and arg == "Even":
            win = True
        elif winning_num % 2 != 0 and arg == "Odd":
            win = True
    
    if arg == "0" and winning_num == 0:
        multiplicator = 37
        win = True

    print(winning_num, arg)
    return win, multiplicator