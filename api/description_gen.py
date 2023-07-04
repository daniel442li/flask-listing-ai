import api.constants
import requests
import json

def description_gen(description):
    description = "bullet points only key ideas " + description

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + constants.api_key
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": description}],
        "temperature": 0.7
    }

    url = "https://api.openai.com/v1/chat/completions"
    response = requests.post(url, headers=headers, json=data)
    response_data = json.loads(response.text)

    # Process the response data as needed
    return response_data['choices'][0]['message']['content']