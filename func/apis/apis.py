import requests, datetime

def update_time():
    rn = datetime.datetime.now()
    day = rn.day
    month = rn.month
    hour = rn.hour
    minute = rn.minute
    second = rn.second
    return day, month, hour, minute, second

def witzede():
    day, month, hour, minute, second = update_time()
    WITZ_URL = "https://witzapi.de/api/joke/?limit=1&language=de"

    rsp = requests.get(WITZ_URL)
    data = rsp.json()
    joke = data[0]["text"]
    return joke

def memeapi():
    day, month, hour, minute, second = update_time()
    MEME_URL = "https://meme-api.com/gimme"

    rsp = requests.get(MEME_URL)
    data = rsp.json()
    meme = data["url"]
    filename = f"cache/meme_{day}{month}{hour}{minute}{second}"
    write_temp(filename, meme)
    return filename

def write_temp(name, content):
    with open(name, "w", encoding="UTF-8") as f:
        f.write(content)
    return