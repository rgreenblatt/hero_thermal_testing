import csv
import math

logger_name = str(input("logger pro file: "))
talon_name = str(input("talon file: "))
out_name = str(input("output file: "))
trial_length = float(input("trial length: "))

talon_count = 0
with open(talon_name, 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		if(float(row[3]) > .1):
			break
		talon_count += 1

logger_count = 0
with open(logger_name, 'rt') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		if(float(row['Latest: Force (N)']) < -0.2):
			break
		logger_count += 1


with open(logger_name, 'rt') as logger_csvfile:
	logger_reader = csv.DictReader(logger_csvfile, delimiter=',')
	logger_rows = list(logger_reader)
		
	with open(talon_name, 'rt') as talon_csvfile:
		talon_reader = csv.reader(talon_csvfile, delimiter=',')
		talon_rows = list(talon_reader)
		with open(out_name, 'w') as csvfile:
			fieldnames = ['Time_talon', 'Time_logger', 'temp1', 'temp2', 'temp3', 'force', 'voltage', 'current', 'RPM']

			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			time_talon = 0.0	
			time_logger = 0.0	

			zero_time_talon = float(talon_rows[talon_count][0])
			zero_time_logger = float(logger_rows[logger_count]['Latest: Time (s)'])
	
			
			i = talon_count
			k = logger_count

			force_conv_factor = 1.0		
			RPM_conv_factor = 1.0
			writer.writeheader()
			while time_talon < trial_length +1.0:
			

				writer.writerow({'Time_talon': time_talon, 'Time_logger': time_logger, 'temp1': float(logger_rows[k]['Latest: Temperature 1 (°C)']) + 273.15, 'temp2': float(logger_rows[k]['Latest: Temperature 2 (°C)']) + 273.15,'temp3': float(logger_rows[k]['Latest: Temperature 3 (°C)']) + 273.15,'force': float(logger_rows[k]['Latest: Force (N)']) * force_conv_factor, 'voltage': talon_rows[i][3], 'current': talon_rows[i][4],'RPM': float(talon_rows[i][2]) * RPM_conv_factor })


				i+=1
			

				time_talon = float(talon_rows[i][0]) - zero_time_talon
				while True:
					if(abs(time_logger - time_talon) > abs(float(logger_rows[k + 1]['Latest: Time (s)']) - zero_time_logger - time_talon)):
						k+=1
					else:
						break
				time_logger = float(logger_rows[k]['Latest: Time (s)']) - zero_time_logger
				

