from typing import Tuple, Dict
import os
import json
from dotenv import load_dotenv
import requests
import streamlit as st
from openai import OpenAI


load_dotenv()
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")



token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Error: {response.status_code}")
        # Check if the response is valid JSON
        data = response.json()
        conversion_result = data["conversion_result"]
        return base, target, amount, f"{conversion_result:.2f}"
    except requests.exceptions.RequestException as e:
        print(f"RequestException {e} for {base} {target} {amount}")
        return base, target, amount, None

def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    
    tools = [{
        "type": "function",
        "function": {
            "name": "exchange_rate_function",
            "description": "Convert a given amount of money from one currency to another. Each currency is represented by a 3-letter code (e.g., USD, EUR).",
            "parameters": {
                "type": "object",
                "properties": {
                    "base":   {"type": "string", "description": "The base currency code (e.g., USD, EUR)"},
                    "target": {"type": "string", "description": "The target currency code (e.g., USD, EUR)"},
                    "amount": {"type": "string", "description": "The amount of money to convert"},
                },
                "required": ["base", "target", "amount"],
                "additionalProperties": False
            },
            "strict": True
        }
    }]



    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
            tools=tools
        )
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Exception {e} for {text}")
    else:
        return response

def run_pipeline():
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    if True: #tool_calls
        # Update this
        st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}')

    elif True: #tools not used
        # Update this
        st.write(f"(Function calling not used) and response from the model")
    else:
        st.write("NotImplemented")



import streamlit as st

# Title of the app
st.title("Multilingual Money Changer")

# Text input box
user_input = st.text_input("Enter the amount and currency:")

# Submit button
if st.button("Submit"):
    # Print the contents of the text box below
    response = call_llm(user_input)
    response_arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    base = response_arguments["base"]
    target = response_arguments["target"]
    amount = response_arguments["amount"]
    exchange_response = get_exchange_rate(base, target, amount)
    # Display the response
    st.write(exchange_response)