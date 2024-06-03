import datetime, colorama, time
def catch_error(ex):
    currentDateAndTime = datetime.datetime.now()
    time = currentDateAndTime.strftime("%H\\%M\\%S")
    print(colorama.Fore.CYAN + f"{time} " + colorama.Fore.LIGHTRED_EX + f"{ex}")
    file = open(f"Log.txt", "a", encoding="UTF-8")
    file.write(f"\n{time} - {ex}")

def check(client):
    while True:
        currentDateAndTime = datetime.datetime.now()
        currentTime = currentDateAndTime.strftime("%H\\%M\\%S")
        print(colorama.Fore.LIGHTGREEN_EX + f"{client} IS STILL ONLINE " + colorama.Fore.BLACK + colorama.Back.WHITE + f"{currentTime}" + colorama.Style.RESET_ALL)
        time.sleep(300)