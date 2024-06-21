import requests
import os

print(api_key := os.getenv("OPENAI_API_KEY"))

def get_account_balance(api_key):
    url = "https://api.openai.com/v1/dashboard/billing/credit_grants"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

balance_info = get_account_balance(api_key)
print("\033[31;0mAccount Balance Information:", balance_info, "\033[0m")
