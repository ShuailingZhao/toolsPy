import csv
import os
import sys

def readCSV(fileName='./traWeightLoss.csv'):
	if not os.path.exists(fileName):
		sys.exit(0)
	with open(fileName, 'r') as f:
		reader = csv.reader(f)
		result = list(reader)
		return result

def writeCSV(data, fileName='./traWeightLoss.csv'):
	if os.path.exists(fileName):
		os.remove(fileName)
	with open(fileName, "a+") as output:
		writer = csv.writer(output, lineterminator='\n')
		for val in data:
			writer.writerow(val)
