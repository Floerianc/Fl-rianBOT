import datetime, colorama

def catch_error(ex):
    currentDateAndTime = datetime.datetime.now()
    time = currentDateAndTime.strftime("%H\\%M\\%S")
    print(colorama.Fore.CYAN + f"{time} " + colorama.Fore.LIGHTRED_EX + f"{ex}" + colorama.Style.RESET_ALL)
    file = open(f"Log.txt", "a", encoding="UTF-8")
    file.write(f"\n{time} - {ex}")