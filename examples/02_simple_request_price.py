'''
Example of sending a simple request to the OpenAI API with price computation
'''
import requests

from config import API_KEY, API_URL

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

payload = {
    'model': 'gpt-3.5-turbo',  # gpt-4o-mini
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
    print(e)
else:
    response_data = response.json()
    for key, value in response_data.items():
        print(f'{key} : {value}')


# compute price of a prompt
def get_price(n_tokens: int, price_per_mil: float = 2) -> float:
    return n_tokens / 1_000_000 * price_per_mil


INPUT_PRICE = 0.5  # 0.15
OUTPUT_PRICE = 1.5  # 0.60

prompt_tokens = response_data['usage']['prompt_tokens']
completion_tokens = response_data['usage']['completion_tokens']

prompt_price = get_price(prompt_tokens, price_per_mil=INPUT_PRICE)
completion_price = get_price(completion_tokens, price_per_mil=OUTPUT_PRICE)
total_price = prompt_price + completion_price

print('-' * 80)
print(f'💸: Price for this request: {total_price:.6f} $')
print(f'💸: Thats a total of: {total_price * 22.7:.6f} CZK')
print(f'💸: Price for input: {prompt_price} $')
print(f'💸: Price for output: {completion_price} $')
print('-' * 80)
