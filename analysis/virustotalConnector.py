import os
import json
import time
import requests
import csv

API_KEY = "7bde630c6bbed3657fd6f55c85a8ad30dd291c7b924ec10bf24c99d054bcb9b8"
POSITIVE_SAMPLES_DIR_1 = r"C:\Users\Martin\Desktop\Samples\tests\positive\generated"
POSITIVE_SAMPLES_DIR_2 = r"C:\Users\Martin\Desktop\Samples\tests\positive\win2020EXE"
NEGATIVE_SAMPLES_DIR = r"C:\Users\Martin\Desktop\Samples\tests\negative_samples"
BASE_URL = "https://www.virustotal.com/api/v3"
STATS_JSON = "stats.json"
STATS_CSV = "stats.csv"
PARTIAL_RESULTS_CSV = "partial_results.csv"

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

def wait_for_analysis_completion(analysis_id, max_retries=10, interval=30):
    retries = 0
    print("Sleeping")
    time.sleep(interval)
    while retries < max_retries:
        report = get_analysis_report(analysis_id)
        status = report["data"]["attributes"]["status"]
        if status not in ["queued", "in_progress"]:
            return report
        
        print(f"Sleeping n.{retries}")
        time.sleep(interval)
        retries += 1
    print(f"Analysis did not complete after {max_retries} retries.")
    return None

def compute_statistics(results):
    stats = {}
    for sample, report, source in results:
        for scan_engine in report["data"]["attributes"]["results"].values():
            engine_name = scan_engine["engine_name"]
            detected = scan_engine["category"] == "malicious"
            if engine_name not in stats:
                stats[engine_name] = {"source": source, "TP": 0, "TN": 0, "FP": 0, "FN": 0}
            if source != "negative" and detected:
                stats[engine_name]["TP"] += 1
            elif source != "negative" and not detected:
                stats[engine_name]["FN"] += 1
            elif source == "negative" and detected:
                stats[engine_name]["FP"] += 1
            else:
                stats[engine_name]["TN"] += 1
    return stats

def save_stats_to_json(stats, output_file):
    with open(output_file, "w") as f:
        json.dump(stats, f, indent=2)

def save_stats_to_csv(stats, output_file):
    fieldnames = ["Engine", "Source", "Accuracy"]
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for engine, data in stats.items():
            accuracy = (data["TP"] + data["TN"]) / (data["TP"] + data["TN"] + data["FP"] + data["FN"])
            writer.writerow({"Engine": engine, "Source": data["source"], "Accuracy": accuracy})


def process_samples(samples_dir, source):
    for sample in os.listdir(samples_dir):
        sample_path = os.path.join(samples_dir, sample)
        try:
            print(f"Uploading file {sample} from {source}...")
            upload_response = upload_file(sample_path)
            if upload_response.get("data"):
                analysis_id = upload_response["data"]["id"]
                print("Analysis id" + analysis_id)
                report = wait_for_analysis_completion(analysis_id)
                if report:
                    print(report)
                    result = (sample, report, source)
                    save_partial_result_to_csv(result, PARTIAL_RESULTS_CSV)
                else:
                    print(f"Analysis did not complete for {sample}")
            else:
                print(f"Failed to retrieve report for {sample}")
        except Exception as e:
            print(f"Error processing {sample}: {e}")
        time.sleep(15)  # To avoid exceeding the API rate limit


def save_partial_result_to_csv(result, output_file):
    sample, report, source = result
    if "results" not in report["data"]["attributes"]:
        print(f"results not found in the report for {sample}")
        return
    with open(output_file, "a", newline="") as f:
        writer = csv.writer(f)
        for scan_engine in report["data"]["attributes"]["results"].values():
            engine_name = scan_engine["engine_name"]
            detected = scan_engine["category"] == "malicious"
            writer.writerow([sample, engine_name, source, detected])


def main():
    with open(PARTIAL_RESULTS_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Sample", "Engine", "Source", "Detected"])

    positive_results_1 = process_samples(POSITIVE_SAMPLES_DIR_1, "generated")
    positive_results_2 = process_samples(POSITIVE_SAMPLES_DIR_2, "VirusTotal")
    negative_results = process_samples(NEGATIVE_SAMPLES_DIR, "negative")
    results = positive_results_1 + positive_results_2 + negative_results
    stats = compute_statistics(results)
    save_stats_to_json(stats, STATS_JSON)
    save_stats_to_csv(stats, STATS_CSV)
    print(f"Saved statistics to {STATS_JSON} and {STATS_CSV}")
if __name__ == "__main__":
    main()
