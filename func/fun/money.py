import random, pickledb
class User:
    def __init__(self, name, money) -> None:
        self.name = name
        self.money = money


def steal_from_user(user, rdm_user):
    num = random.randint(1,100)
    if num < 61:
        money_change = random.randint(80,240)
        msg_content = f"{user.mention} successfully stole **{money_change}€** from {rdm_user.mention}!"
    else:
        money_change = random.randint(-90,-30)
        msg_content = f"{user.mention} couldn't steal any money from {rdm_user.mention}, losing {money_change}€ instead."
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

    reasons = ["Tripped, fell on their face and passed out.", "A neighbor heard a strange noise and contacted the police, which has arrested you and fined you.", "The home owner was at home and had a gun by his side, robbing you instead before you flee out of the house."]

    num = random.randint(1,100)
    money_change = 0

    if num < 26:
        received_items = []
        for i in range(random.randint(1,5)):
            received_items.append(items[random.randint(0,len(items)-1)])
        
        msg_content = f"{user} robbed a house, he received the following items:\n"

        for i in range(len(received_items)):
            msg_content += f"\n*{received_items[i][0]}:*    **{received_items[i][1]}€**"
            money_change += received_items[i][1]
        
        msg_content += f"\n\nTotal: **{money_change}€**"

    else:
        max_iteration = len(reasons)-1
        money_change = random.randint(-150,-80)
        msg_content = f"{user} was not able to rob the house.\nReason: {reasons[random.randint(0,max_iteration)]}\nMoney lost: {money_change}€"
    
    return msg_content, money_change