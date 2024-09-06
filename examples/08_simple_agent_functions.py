'''Example of a simple agent-like chat bot using OpenAI API functions'''
from typing import Optional
from collections import deque
import json
import random
import requests

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
            'model': 'gpt-4o',
            'messages': msgs,
            'tools': TOOLS
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


def get_delivery_time(order_id: int) -> int:
    '''Returns delivery time in minutes based on id'''
    print(f'{'-' * 80}\n⚙️: Getting delivery time for order {order_id}\n{'-' * 80}')
    return random.randint(1, 120)


def update_order(order_id: int, new_items: list) -> bool:
    '''Updates order with new items if it is possible'''
    # do some update logic
    print(f'{'-' * 80}\n⚙️: Updating order {order_id} with {new_items}\n{'-' * 80}')
    return True


MAIN_CONTEXT = '''You are a helpful assistant in pizza shop. 
Use the supplied tools to assist the user. Never make up any function parameters. Ask the user.
Always ask for concerete pizza types'''

TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'get_delivery_time',
            'description': ('Gets the time remaining until delivery in minutes. '
                            'Call this whenever you need to know how much time '
                            'is remaing unitl the delivery, for example '
                            'when a customer asks "When will be my order delivered?"'),
            'parameters': {
                'type': 'object',
                'properties': {
                    'order_id': {
                        'type': 'integer',
                        'description': 'The users order id.',
                    },
                },
                'required': ['order_id'],
                'additionalProperties': False,
            },
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'update_order',
            'description': ('Updates the order if it is possible. '
                             'Call this whenever user wants to update the order.'
                             'For example when "Add two salami pizzas to my order"'),
            'parameters': {
                'type': 'object',
                'properties': {
                    'order_id': {
                        'type': 'integer',
                        'description': 'The users order id.',
                    },
                    'new_items': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                        },
                        'description': 'The list of new items to be added to the order.',
                    }
                },
                'required': ['order_id', 'new_items'],
                'additionalProperties': False,
            },
        }
    }
]

if __name__ == '__main__':
    print('🤖: How can I help you: ')
    while True:
        question = input('🧑: ')
        prompts.append({'role': 'user', 'content': question})
        messages = [{'role': 'system', 'content': MAIN_CONTEXT}] + \
            list(prompts)

        answer_data = send_request(messages)
        if not answer_data:
            print('🤖: Im sorry, an error occurred')
        else:
            answer = get_answer(answer_data)
            if answer:
                print(f'🤖: {answer}')
                prompts.append({'role': 'assistant', 'content': answer})
            else:
                # use tools
                tools = answer_data['choices'][0]['message']['tool_calls']
                for tool in tools:
                    tool_name = tool['function']['name']
                    arguments = json.loads(tool['function']['arguments'])
                    match tool_name:
                        case 'get_delivery_time':
                            delivery_time = get_delivery_time(**arguments)
                            response_message = f'The delivery time is approximately {delivery_time} minutes.'
                        case 'update_order':
                            is_successful = update_order(**arguments)
                            response_message = 'Your order has been updated successfully.' + \
                                               f'You added: {', '.join(arguments['new_items'])}.'
                        case _:
                            response_message = 'No valid command found.'
                    print(f'🤖: {response_message}')
                    prompts.append({'role': 'assistant',
                                    'content': response_message})
