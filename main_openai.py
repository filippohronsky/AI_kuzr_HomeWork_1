import os
import json
import requests
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

# Load environment variables (ak chceš, môžeš credentials nechať natvrdo v kóde)
load_dotenv()

# --- Cisco Catalyst Center API konfigurácia ---
DNAC_HOST = "10.10.20.85"
DNAC_USER = "administrator"
DNAC_PASS = "Cisco1234!"

# ---- Funkcia pre získanie zoznamu zariadení z Catalyst Center API ----
def get_dnac_token():
    url = f"https://{DNAC_HOST}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=(DNAC_USER, DNAC_PASS), verify=False)
    response.raise_for_status()
    return response.json()["Token"]

def get_dnac_devices():
    token = get_dnac_token()
    url = f"https://{DNAC_HOST}/dna/intent/api/v1/network-device"
    headers = {"X-Auth-Token": token}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    devices = response.json()["response"]
    # Napríklad vypíš len názvy a IP adresy
    return [{"hostname": d.get("hostname"), "managementIpAddress": d.get("managementIpAddress")} for d in devices]

# --- Definuj tool pre OpenAI ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_dnac_devices",
            "description": "Get list of network devices from Cisco Catalyst Center.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
    }
]

available_functions = {
    "get_dnac_devices": get_dnac_devices,
}

# --- Spracovanie AI požiadavky ---
def get_completion_from_messages(messages, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    print("First response:", response_message)

    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        tool_id = tool_call.id

        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)

        print(function_response)

        messages.append({
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_id,
                    "type": "function",
                    "function": {
                        "name": function_name,
                        "arguments": json.dumps(function_args),
                    }
                }
            ]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_id,
            "name": function_name,
            "content": json.dumps(function_response),
        })

        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        final_answer = second_response.choices[0].message

        print("Second response:", final_answer)
        return final_answer

    return "No relevant function call found."


# --- Príklad použitia ---
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Vypíš zoznam zariadení z Catalyst Center."},
]

response = get_completion_from_messages(messages)
print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.content)