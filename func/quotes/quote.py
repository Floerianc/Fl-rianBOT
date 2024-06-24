import random
def get_quote():
    with open("func\quotes\quotes.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
    quote = random.choice(lines).replace(";", "\n")
    quote = quote.replace("@", "- ")
    return quote