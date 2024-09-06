'''Example of a simple agent-like chat bot using OpenAI API'''
import requests
from typing import Optional
from collections import deque

from config import API_KEY, API_URL

prompts: deque = deque(maxlen=10)
messages: list = []

HEADER = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}


def send_request(msgs: list) -> Optional[dict]:
    try:
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': msgs
        }
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


def set_heating(temp: float, lvl: int) -> float:
    return temp + lvl


def set_cooling(temp: float, lvl: int) -> float:
    return temp - lvl * 0.5


MAIN_CONTEXT = '''Your task is to keep the temperature in the room comfortable for ALL users.
You will get a request or description about how the users in the room feels.
You will also get a actual temperature in celsius degrees in the room from sensor.
Each message could be from different user. You have to find compromise to suit all users.
You can use commands: 'heating' and 'cooling'.
You can set level of heating from 0 to 5 and cooling from 0 to 5.
0 means off, 5 means maximum power.
Heating raises the temperature and cooling lowers it.
You can use only one command at time. Return in the format: level command.
For example: heating 0
'''

if __name__ == '__main__':
    try:
        temperature = 20.0
        print('🤖: Waiting for prompt...')
        while True:
            question = input('🧑: ') + f'\n Actual temperature: {temperature} C'
            prompts.append({'role': 'user', 'content': question})
            messages = [{'role': 'system', 'content': MAIN_CONTEXT}] + \
                list(prompts)

            answer_data = send_request(messages)
            if not answer_data:
                print('🤖: Im sorry, an error occurred')
            else:
                answer = get_answer(answer_data)
                print(f'🤖: {answer}')
                prompts.append({'role': 'assistant', 'content': answer})
                match answer.split():
                    case ('heating', level):
                        temperature = set_heating(temperature, int(level))
                    case ('cooling', level):
                        temperature = set_cooling(temperature, int(level))
                    case _:
                        print('⚙️: No command')
                print(f'⚙️: Current temperature: {temperature} C')
    except KeyboardInterrupt:
        print('\n🤖: Goodbye! Chat session ended.')
