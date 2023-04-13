import requests
import os

url_ni = 'http://localhost:5000/ni/upload'
url_bi = 'http://localhost:5000/bi/upload'

folders = [r"C:\Users\Martin\Desktop\Samples\tests\positive\generated",
            r"C:\Users\Martin\Desktop\Samples\tests\positive\win2020EXE",
            r"C:\Users\Martin\Desktop\Samples\tests\negative_samples"]
results = []

for folder in folders:
    counter = 0
    for file in os.listdir(folder):
        try:
            file_path = f"{folder}\\{file}"
            with open(file_path, 'rb') as file:
                response = requests.post(url_bi, files={'file': file})

            if response.status_code == 200:
                print("File uploaded and processed successfully.")
                print("Prediction result:", response.json()['prediction'])
                if float(response.json()['prediction']) > 0.3:
                    counter += 1
                print(response.json())
            elif response.status_code == 500:
                print("Error: Internal server error.")
            else:
                print("Error:", response.json()['error'])
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    results.append(counter)
    
    print(results)