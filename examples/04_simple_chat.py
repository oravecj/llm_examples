'''Example of a simple chat bot using OpenAI API with unlimited context'''
from typing import Optional
import requests

from config import API_KEY, API_URL

messages: list = []

HEADER = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}


def send_request(msgs: list) -> Optional[dict]:
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': msgs
    }
    try:
        response = requests.post(url=API_URL,
                                 headers=HEADER,
                                 json=payload,
                                 timeout=60,
                                 verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'🚨: {e}')
        return None


def get_answer(response: dict) -> str:
    return response['choices'][0]['message']['content']


def get_token_count(response: dict) -> int:
    return response['usage']['total_tokens']


if __name__ == '__main__':
    try:
        print('🤖: Helo, Im a simple chat bot')
        context = input('🤖: Please specify how should I behave: ')
        messages.append({'role': 'system', 'content': context})
        while True:
            question = input('🧑: ')
            messages.append({'role': 'user', 'content': question})

            answer_data = send_request(messages)
            if not answer_data:
                print('🤖: Im sorry, an error occurred')
            else:
                answer = get_answer(answer_data)
                print(f'🤖: {answer}')
                messages.append({'role': 'assistant', 'content': answer})
                print(f'⚙️: (used {get_token_count(answer_data)} tokens)')
    except KeyboardInterrupt:
        print('\n🤖: Goodbye! Chat session ended.')
