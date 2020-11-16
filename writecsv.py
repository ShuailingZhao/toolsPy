import csv
import os
my_file = './traWeightLoss.csv'
if os.path.exists(my_file):
	os.remove(my_file)
traWeightLoss=[]

for num in range(1,10):
	traWeightLoss.append([num,num+1,num+20])
for val in traWeightLoss:
	with open('traWeightLoss1.csv', "a+") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerow(val)
