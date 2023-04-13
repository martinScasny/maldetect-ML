import csv
import json
import pandas as pd
from pandas.io.json import json_normalize

values = {}
stats = {}
sources = ["generated", "VirusTotal", "negative"]
# output json
# 1. presnost jednotlivy enginov podla source
# pre kazdy source a pre kazdy engine TP, TN, FP, FN
# Priemerne hodnota enginov
# 
with open('partial_results.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    firstLine = 1
    for row in reader:
        if firstLine:
            firstLine = 0
            continue
        filename = row[0]
        engine = row[1]
        source = row[2]
        val = row[3]
        
        if filename not in values:
            values[filename] = {"source": source, "engines":{}}

        val_calc = True if val == 'True' else False 
        values[filename]["engines"][engine] = val_calc

print(len(values))


for filename in values:
    source = values[filename]["source"]
    engines = values[filename]["engines"]
    
    if source not in stats:
        stats[source] = { "count": 0, "engines": {}}
    
    stats[source]["count"] += 1
    
    for k,v in engines.items():
        if k not in stats[source]["engines"]:
            stats[source]["engines"][k] = 0
        if v:
            stats[source]["engines"][k] += 1

# Create a DataFrame from the "stats" dictionary
engine_order = [
    "Bkav",
    "Lionic",
    "Elastic",
    "MicroWorld-eScan",
    "FireEye",
    "CAT-QuickHeal",
    "ALYac",
    "Malwarebytes",
    "Zillya",
    "Sangfor",
    "K7AntiVirus",
    "Alibaba",
    "K7GW",
    "CrowdStrike",
    "Baidu",
    "VirIT",
    "Cyren",
    "SymantecMobileInsight",
    "Symantec",
    "tehtris",
    "ESET-NOD32",
    "APEX",
    "Paloalto",
    "ClamAV",
    "Kaspersky",
    "BitDefender",
    "NANO-Antivirus",
    "SUPERAntiSpyware",
    "Avast",
    "Tencent",
    "Trustlook",
    "Emsisoft",
    "F-Secure",
    "DrWeb",
    "VIPRE",
    "TrendMicro",
    "McAfee-GW-Edition",
    "Trapmine",
    "CMC",
    "Sophos",
    "SentinelOne",
    "GData",
    "Jiangmin",
    "Webroot",
    "Google",
    "Avira",
    "MAX",
    "Antiy-AVL",
    "Gridinsoft",
    "Xcitium",
    "Arcabit",
    "ViRobot",
    "ZoneAlarm",
    "Avast-Mobile",
    "Microsoft",
    "Cynet",
    "BitDefenderFalx",
    "AhnLab-V3",
    "Acronis",
    "McAfee",
    "TACHYON",
    "VBA32",
    "Cylance",
    "Panda",
    "Zoner",
    "TrendMicro-HouseCall",
    "Rising",
    "Yandex",
    "Ikarus",
    "MaxSecure",
    "Fortinet",
    "BitDefenderTheta",
    "AVG",
    "DeepInstinct"
]

engines = set()
for source in stats:
    engines |= set(stats[source]['engines'].keys())
engine_order = sorted(engines)

# create empty dataframe
df = pd.DataFrame(columns=engine_order)

# fill dataframe with data
for source in stats:
    engine_data = stats[source]['engines']
    row = pd.DataFrame(engine_data, index=[source])
    df = pd.concat([df, row], axis=0, sort=False)

# fill NaN values with 0
df = df.fillna(0)

# save dataframe to CSV
df.to_csv('output.csv', index=True)





