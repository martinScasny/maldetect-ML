import pe_parser
import csv

def writeValuesForAnalysisToCSV(features):
  with open("./analysis/values.csv","a") as csv_file:
    csv_file.write(f"\n{features[0]},{features[1]},{features[2]}")
    