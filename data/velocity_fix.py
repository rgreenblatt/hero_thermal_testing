from tempfile import NamedTemporaryFile
import shutil
import csv
import sys


file_name =  str(sys.argv[1])

tempfile = NamedTemporaryFile(delete=False)

max_a = 150

last_RPM = 0

with open(file_name, 'rb') as csvFile, tempfile:
	reader = csv.DictReader(csvFile, delimiter=',')
	out_field_names = reader.fieldnames
	writer = csv.DictWriter(tempfile, fieldnames=out_field_names)
	
	writer.writeheader()
	index = 0
	counter = 0
	for row in reader:
		#if(not first and abs(last_RPM - float(row['RPM'])) > max_a):
		#	print("wow")
	#`		row['RPM'] = str(last_RPM)
		writer.writerow(row)
		last_RPM = float(row['RPM'])
		print(last_RPM)
		first = False
shutil.move(tempfile.name, file_name)
