import os
import json
import time
import requests

API_KEY = "<your_virustotal_api_key>"
POSITIVE_SAMPLES_DIR = "positive_samples"
NEGATIVE_SAMPLES_DIR = "negative_samples"
BASE_URL = "https://www.virustotal.com/api/v3"

def upload_file(file_path):
    with open(file_path, "rb") as file:
        headers = {
            "x-apikey": API_KEY
        }
        response = requests.post(f"{BASE_URL}/files", headers=headers, files={"file": file})
        return response.json()

def get_analysis_report(analysis_id):
    headers = {
        "x-apikey": API_KEY
    }
    response = requests.get(f"{BASE_URL}/analyses/{analysis_id}", headers=headers)
    return response.json()

def process_samples(samples_dir, is_positive):
    sample_results = []
    for sample in os.listdir(samples_dir):
        sample_path = os.path.join(samples_dir, sample)
        upload_response = upload_file(sample_path)
        analysis_id = upload_response["data"]["id"]
        time.sleep(30)  # Wait for the analysis to complete
        report = get_analysis_report(analysis_id)
        if report.get("data"):
            sample_results.append((sample, report, is_positive))
        else:
            print(f"Failed to retrieve report for {sample}")
        time.sleep(15)  # To avoid exceeding the API rate limit
    return sample_results

# Compute statistics and main functions remain the same as the previous script

if __name__ == "__main__":
    main()
