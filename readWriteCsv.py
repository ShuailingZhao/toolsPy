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
			
class txtLoader:
	def __init__(self, dataPath):
		self.f = open(dataPath,"r")

	def nextRow(self):
		oneLine = self.f.readline().strip('\n')
		data = oneLine.split(',')
		return data
	
	def close(self):
		self.f.close()
