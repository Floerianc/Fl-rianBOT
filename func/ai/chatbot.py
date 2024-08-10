from openai import OpenAI

def initiate_ai_client():
    client = OpenAI(
        api_key="YOUR-API-KEY-HERE",
        base_url="https://api.aimlapi.com",
    )
    return client

def ai_send_response(user_content: str):
    client = initiate_ai_client()
    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant who knows everything. You are polite but you like to joke around at times and occasionally you have massive mood-swings and you are depressed as fuck, try to somehow maintain a positive attitude, sometimes. KEEP YOUR RESPONSES SHORT, MAX 80 WORDS AND STOP USING THOSE DUMB HASHTAGS",
                },
                {
                    "role": "user",
                    "content": user_content
                },
            ],
        )
    except:
        message = "Hit hourly Token limit, woops"; return message

    message = response.choices[0].message.content
    return message