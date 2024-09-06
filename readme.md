# Python LLM Example Project

## Project Overview

This project provides simple examples demonstrating how to interact with the OpenAI API using Python. It covers a variety of simple basic use cases, from sending basic requests to implementations like chat with history, retrieval-augmented generation (RAG), and agent-based conversations.

The project is structured to progressively introduce different functionalities, starting from basic requests and building up to more complex scenarios.

---

## Files Overview

### 1. `01_simple_request.py`
**Description**:  
This example sends a basic request to the OpenAI API. The request contains a system context and a user query, and prints the response from the API.

### 2. `02_simple_request_price.py`
**Description**:  
This example builds on the basic request, introducing the calculation of token usage and cost based on OpenAI's pricing. It helps estimate how much each request will cost depending on the token consumption.

### 3. `03_simple_request_with_history.py`
**Description**:  
In this example, the script demonstrates how to send a request that includes previous conversation history, enabling a more context-aware response from the model.

### 4. `04_simple_chat.py`
**Description**:  
This example extends to a simple chat interface where the user can send multiple queries to the API, and responses are given in real-time. It shows a basic implementation of conversational AI.

### 5. `05_simple_chat_limited_history.py`
**Description**:  
Similar to `04_simple_chat.py`, but with limited conversation history. This example restricts the amount of previous messages sent in the request to control the context and manage token usage.

### 6. `06_simple_rag.py`
**Description**:  
This example introduces a basic implementation of Retrieval-Augmented Generation (RAG), where the model is combined with external data retrieval to provide more informed responses. It can be used to augment LLM responses with additional knowledge.

### 7. `07_simple_agent.py`
**Description**:  
A simple agent-based example where the LLM acts as an intelligent agent, taking user inputs and responding with actions or suggestions. The agent's behavior can be extended based on specific tasks or scenarios.

### 8. `08_simple_agent_functions.py`
**Description**:  
This example demonstrates the use of functions in the agent-based system, allowing the LLM to perform specific tasks or make decisions. It showcases how to integrate the model with more advanced logic.

---
### Prerequisites
- Python 3.8+
- `requests` and `dotenv` library
- OpenAI API key

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/oravecj/llm_examples
   cd llm-examples
2. Install requirements:
   python -m venv venv
   source venv/Scipts/activate
   pip install -r requirements.txt

3. Create .env and set API KEY
    `API_KEY = 'your-api-key'`
    `API_URL = 'https://api.openai.com/v1/chat/completions'`
