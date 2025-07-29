import requests
username_list = ["youraj Verma"]
# Replace 'john_doe' with the username you want to query

url = f"http://127.0.0.1:8000/email/{username_list[0]}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json().get("value")
    print(type(data))
except requests.exceptions.RequestException as e:
    print("Request failed")