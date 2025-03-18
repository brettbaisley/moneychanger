from typing import Tuple, Dict
import os
from dotenv import load_dotenv
import requests

load_dotenv()
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")

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
    try:
        completion = ...
    except Exception as e:
        print(f"Exception {e} for {text}")
    else:
        return completion

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