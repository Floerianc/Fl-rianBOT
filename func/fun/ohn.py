def ohn_func():
    ohn_association = ["DNA", "Flörian", "Fabix", "Nightwolf", "Matxilla"]
    ohn_websites = ["www.dnascanner.de", "flo.ohhellnaw.de", "www.bagelxd.de", "nightwolf.ohhellnaw.de", "mat.ohhellnaw.de"]

    msg_content = f""
    for name in zip(ohn_association, ohn_websites):
        msg_content += f"\n### [{name[0]}'s Website](https://{name[1]})"

        if name[0] == "Flörian":
            msg_content += f" *(The creator of this bot hehe :3)*"
    
    return msg_content