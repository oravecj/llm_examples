'''Example of sending a simple request to the OpenAI API'''
import requests

from config import API_KEY, API_URL

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

payload = {
    'model': 'gpt-3.5-turbo',
    'messages': [
        {'role': 'system',
         'content': 'You are a helpful assistant.'},  # context
        {'role': 'user',
         'content': 'Hello. How are you today?'}  # user query
        ],
}

try:
    response = requests.post(url=API_URL,
                             headers=headers,
                             json=payload,
                             timeout=60,
                             verify=False)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f'{e}')
else:
    response_data = response.json()
    for key, value in response_data.items():
        print(f'{key} : {value}')
