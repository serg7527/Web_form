import requests

url = 'http://localhost:5000/get_form'
data = {
    'user_name': 'test',
    'order_date': '01.01.2023',
    'lead_email': 'test@test.com'
}

response = requests.post(url, data=data)

if response.status_code == 200:
    try:
        print(response.json())
    except ValueError as e:
        print(f"JSON decode error: {e}")
        print("Response text:", response.text)
else:
    print(f"Error: {response.status_code} - {response.text}")