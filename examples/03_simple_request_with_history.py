'''Example of sending a simple request to the OpenAI API with chat history'''
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
         'content': 'You are a helpful assistant that remebers the chat history.'},  # context
        {'role': 'user',
         'content': 'Hello, My name is Jakub, what is your name?'},  # chat history
        {'role': 'assistant',
         'content': 'Hello Jakub, Im a helpful assistant. How can I assist you today?'},  # chat history
        {'role': 'user',
         'content': 'Do you remember anything about me?'}  # user query
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
    print(f'🚨: {e}')
else:
    response_data = response.json()
    print('🤖: ' + response_data['choices'][0]['message']['content'])
