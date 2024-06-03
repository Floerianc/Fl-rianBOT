def write_vbs(msg):
    import os
    with open("cache/msg_from_user.vbs", "w", encoding="UTF-8") as vbs:
        vbs.write(f'x = msgbox("{msg}", 16+0, "Message from User")')
    os.system("start cache/msg_from_user.vbs")
