import sys
import requests

if len(sys.argv) != 2:
    print("Usage: python client.py <filename>")
    sys.exit(1)

url = 'http://localhost:5000/upload'
file_path = sys.argv[1]

try:
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})

    if response.status_code == 200:
        print("File uploaded and processed successfully.")
        print("Prediction result:", response.json()['prediction'])
        print(response.json())
    elif response.status_code == 500:
        print("Error: Internal server error.")
    else:
        print("Error:", response.json()['error'])
except FileNotFoundError:
    print(f"File not found: {file_path}")
