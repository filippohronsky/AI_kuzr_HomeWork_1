import json
import requests
from ollama import chat

# --- Cisco Catalyst Center API konfigurácia ---
DNAC_HOST = "10.10.20.85"
DNAC_USER = "administrator"
DNAC_PASS = "Cisco1234!"

def get_dnac_devices():
    url = f"https://{DNAC_HOST}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=(DNAC_USER, DNAC_PASS), verify=False)
    response.raise_for_status()
    token = response.json()["Token"]

    url = f"https://{DNAC_HOST}/dna/intent/api/v1/network-device"
    headers = {"X-Auth-Token": token}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    devices = response.json()["response"]
    return [{"hostname": d.get("hostname"), "managementIpAddress": d.get("managementIpAddress")} for d in devices]

# --- Namiesto tools (nie je potrebné), stačí slovník funkcií ---
available_functions = {
    "get_dnac_devices": get_dnac_devices,
}

# --- Example usage ---
messages = [
    {"role": "user", "content": "Vypíš zoznam zariadení z Catalyst Center."}
]

response = chat(
    "mistral:instruct",
    messages=messages,
)

print("First response:", response.message.content)

# Skús vyparsovať názov funkcie z odpovede modelu (z textu)
if "get_dnac_devices" in response.message.content:
    function_name = "get_dnac_devices"
    function_to_call = available_functions[function_name]
    function_response = function_to_call()
    print("Function response:", function_response)

    # Pridaj odpoveď z toolu ako novú správu
    messages.append({
        "role": "tool",
        "name": function_name,
        "content": json.dumps(function_response),
    })

    # Získaj finálnu odpoveď od modelu
    final_response = chat("mistral:instruct", messages=messages)
    print("Second response:", final_response.message.content)
else:
    print("Model nepožiadal o žiadnu známu funkciu.")