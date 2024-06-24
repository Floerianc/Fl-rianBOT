import requests

DAWUM_API_URL = 'https://api.dawum.de/'

def get_current_json():
    rsp = requests.get(DAWUM_API_URL) # Sends a request to the API_URL
    data = rsp.json() # Converts it into a JSON
    return data

def most_recent_survey(data):
    keys = list(data["Surveys"].keys())
    MRS = data["Surveys"][f"{keys[0]}"] # MRS (Most Recent Survey) is now the first key in the Surveys Section
    return MRS

def get_values(MRS, data):
    date = MRS["Date"] # Gets date of first Survey
    surveyed_people = MRS["Surveyed_Persons"] # How many people contributed
    results = MRS["Results"] # Results of all Parties who were there
    parliament_ID = MRS["Parliament_ID"] # Parliament ID
    institute_ID = MRS["Institute_ID"] # usw...
    parliament_name = data["Parliaments"][f"{parliament_ID}"]["Name"]
    institute_name = data["Institutes"][f"{institute_ID}"]["Name"]

    parties = []
    percentages = []
    abbreviations = []
    for key in results.keys(): # Gets the KEYS of the 'results' dict (1, 7...)
        parties.append(data["Parties"][f"{key}"]["Name"]) # Alternative für Deutschland... usw
        abbreviations.append(data["Parties"][f"{key}"]["Shortcut"]) # AfD, CDU/CSU...
        percentages.append(results[f"{key}"]) # 30%, 17%...
    
    return date, surveyed_people, parliament_name, institute_name, abbreviations, percentages, parties, parliament_ID, institute_ID


def full_message(data, date, surveyed_people, parliament_name, institute_name, abbreviations, percentages, parties, parliament_ID, institute_ID):
    def get_url(data):
        # https://dawum.de/Europawahl/Forschungsgruppe_Wahlen/2024-05-30/
        parliament_url = data["Parliaments"][f"{parliament_ID}"]["Election"]
        institute_url = institute_name.replace(" ", "_")
        mrs_url = f"https://dawum.de/{parliament_url}/{institute_url}/{date}"
        return mrs_url
    mrs_url = get_url(data)

    results = ""
    content = f"Parlament: **{parliament_name}**\nInstitut: **{institute_name}**\nDatum: **{date}**\nAnzahl befragte Personen: **{surveyed_people}**\n# __Ergebnisse__\n"

    for i in range(len(abbreviations)):
        if i == 0:
            heading = "#"*(i+3) # a hashtag '#' in a discord message makes the font size bigger, so the top 1 party have a bigger font than the rest.
        else:
            heading = "" # if the party is not in the top 1, the texts size will be normal
        
        results += f"\n> {heading} **{i+1}.** {parties[i]} *({abbreviations[i]}):* {percentages[i]}%"
    results += f"\n\nUm die Ergebnisse nochmal auf der offiziellen DAWUM-Website einzusehen, klicken Sie [hier.]({mrs_url})"

    content = content + results # combines date, surveyed people, parliament, institute and the results into one big string
    return content