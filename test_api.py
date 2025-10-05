# test_api.py
import requests

url = "http://127.0.0.1:8000/predict/"
test_url = "https://pazy.io/"

response = requests.post(url, json={"url": test_url})

print("Status Code:", response.status_code)
print("Content-Type:", response.headers.get('content-type'))
print("Response Text:", response.text)

if response.status_code == 200:
    try:
        data = response.json()
        print("\n✅ Parsed JSON:", data)
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
else:
    print("❌ Request failed with status code:", response.status_code)
    print("❌ Response text:", response.text)
    