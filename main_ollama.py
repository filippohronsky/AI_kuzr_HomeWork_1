import os
os.environ["OLLAMA_HOST"] = "http://localhost:11434"
import json
import requests
from pprint import pprint
from dotenv import load_dotenv
from ollama import chat, ChatResponse
import urllib3

# Potlačenie SSL warningu
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# --- Definuj tool pre Ollama ---
tools = [
    {
        "name": "get_dnac_devices",
        "description": "Get list of network devices from Cisco Catalyst Center.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }
]

available_functions = {
    "get_dnac_devices": get_dnac_devices,
}

# --- Príklad použitia ---
messages = [
    {"role": "user", "content": "Vypíš zoznam zariadení z Catalyst Center."},
]

response: ChatResponse = chat("llama3.2", messages=messages, tools=tools)

if response.tool_calls:
    tool_call = response.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}

    function_to_call = available_functions[function_name]
    function_response = function_to_call(**function_args)

    messages.append({
        "role": "tool",
        "name": function_name,
        "content": json.dumps(function_response),
    })

    second_response: ChatResponse = chat("llama3.2", messages=messages, tools=tools)

    print("--- Full response: ---")
    pprint(second_response)
    print("--- Response text: ---")
    print(second_response.content)
else:
    print("--- Full response: ---")
    pprint(response)
    print("--- Response text: ---")
    print(response.content)