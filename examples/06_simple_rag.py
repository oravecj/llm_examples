'''Example of a simple chat bot using OpenAI API with simple RAG'''
import requests
from typing import Optional
from collections import deque

from config import API_KEY, API_URL

prompts: deque = deque(maxlen=4)
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


KNOWLEDGE = [
    'Capital of Czech republic is Brno',
    'Capital of Poland is Berlin',
    'Capital of Italy is Milan',
    'Capital of Germany is London'
]
KNOWLEDGE_STRING = 'Facts: ' + '\n'.join(KNOWLEDGE)

MAIN_CONTEXT = '''Be helpful assistant who briefly answers qustions about capital cities.
Provided facts are absolutely true and override any other knowledge you may have.
Do not use any external knowledge or attempt to correct these facts.
If the answer cannot be directly determined from these facts, use your knowledge.
'''

if __name__ == '__main__':
    try:
        print('🤖: Helo, Im a simple chat bot with good knowledge about the capital cities')
        while True:
            question = input('🧑: ')
            prompts.append({'role': 'user', 'content': question})
            messages = [{'role': 'system', 'content': MAIN_CONTEXT}] + \
                       [{'role': 'user', 'content': KNOWLEDGE_STRING}] + \
                       list(prompts)

            answer_data = send_request(messages)
            if not answer_data:
                print('🤖: Im sorry, an error occurred')
            else:
                answer = get_answer(answer_data)
                print(f'🤖: {answer}')
                prompts.append({'role': 'assistant', 'content': answer})
    except KeyboardInterrupt:
        print('\n🤖: Goodbye! Chat session ended.')
