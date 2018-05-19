import csv
import math
import sys

force_conv_factor = .0565		
RPM_conv_factor = 1

logger_name =  str(sys.argv[1])
talon_name =   str(sys.argv[2])#str(input("talon file: "))



out_name =   str(sys.argv[3])#str(input("output file: "))

	



if(talon_name == "fill_zero"):
	with open(logger_name, 'rt', encoding='utf-8') as logger_csvfile:
		logger_reader = csv.DictReader(logger_csvfile, delimiter=',')
		logger_field_names = logger_reader.fieldnames
		with open(out_name, 'w') as csvfile:
			fieldnames = ['time_talon', 'time_logger', 'temp1', 'temp2', 'temp3', 'force', 'voltage', 'current', 'RPM', 'bus_voltage']

			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
			writer.writeheader()
			for row in logger_reader:
				writer.writerow({'time_talon': row[logger_field_names[0]], 'time_logger': row[logger_field_names[0]], 'temp1': float(row['Latest: Temperature 1 (°C)']) + 273.15, 'temp2': float(row['Latest: Temperature 2 (°C)']) + 273.15,'temp3': float(row['Latest: Temperature 3 (°C)']) + 273.15,'force': float(row['Latest: Force (N)']) * force_conv_factor, 'voltage': 0.0, 'current': 0.0,'RPM': 0.0, 'bus_voltage': 12.0 })


else:

	talon_count = 0
	with open(talon_name, 'rt') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			if(float(row[3]) > .1):
				break
			talon_count += 1

	logger_count = 0
	logger_field_names = []
	with open(logger_name, 'rt', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		print("Field names: ")
		logger_field_names = reader.fieldnames
		print(logger_field_names)
		for row in reader:
			if(float(row['Latest: Force (N)']) < -0.2):
				break
			logger_count += 1


	sum_RPM = 0
	last_RPM = 0
	with open(logger_name, 'rt', encoding='utf-8') as logger_csvfile:
		logger_reader = csv.DictReader(logger_csvfile, delimiter=',')
		logger_rows = list(logger_reader)
			
		with open(talon_name, 'rt') as talon_csvfile:
			talon_reader = csv.reader(talon_csvfile, delimiter=',')
			talon_rows = list(talon_reader)
			with open(out_name, 'w') as csvfile:
				fieldnames = ['time_talon', 'time_logger', 'temp1', 'temp2', 'temp3', 'force', 'voltage', 'current', 'RPM', 'bus_voltage']

				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

				time_talon = 0.0	
				time_talon_last = 0.0
				time_logger = 0.0	

				zero_time_talon = float(talon_rows[talon_count][0])
				zero_time_logger = float(logger_rows[logger_count][logger_field_names[0]])
		
				
				i = talon_count
				k = logger_count
				logger_end = False
				manual = False
				
				if(len(sys.argv) > 5):
					trial_length = float(sys.argv[5])#float(input("trial length: "))
					print("manual")
					manual = True
				else:
					#trial_length = float(talon_rows[-1][0]) - zero_time_talon - .02
					#trial_length = min(trial_length, float(logger_rows[-1][logger_field_names[0]]) - zero_time_logger) - .2
					trial_length = 0.0
					#print(trial_length)
					 

				writer.writeheader()
				while ((time_talon < trial_length or not manual) and (i < len(talon_rows) - 10.0 / 0.01) and not logger_end):
			

					sum_RPM += float(talon_rows[i][2]) * RPM_conv_factor /60.0  * (time_talon - time_talon_last)
					time_talon_last = time_talon

					#print(sum_RPM, " and ", talon_rows[i][1])
				
					rpm = float(talon_rows[i][2]) * RPM_conv_factor
	
					if(i != talon_count and abs(last_RPM) - abs(rpm) > 50):
						print("last rpm: ", last_RPM, "rpm: ", rpm, " row: ", i)

						rpm = last_RPM
		

					writer.writerow({'time_talon': time_talon, 'time_logger': time_logger, 'temp1': float(logger_rows[k]['Latest: Temperature 1 (°C)']) + 273.15, 'temp2': float(logger_rows[k]['Latest: Temperature 2 (°C)']) + 273.15,'temp3': float(logger_rows[k]['Latest: Temperature 3 (°C)']) + 273.15,'force': float(logger_rows[k]['Latest: Force (N)']) * force_conv_factor, 'voltage': talon_rows[i][3], 'current': talon_rows[i][4],'RPM': rpm, 'bus_voltage': talon_rows[i][5] })

					last_RPM = rpm

					i+=1
				
					if(manual and i % 1000  == 0):
						print(time_talon)
					



					time_talon = float(talon_rows[i][0]) - zero_time_talon


					'''					
					if(float(talon_rows[i][0]) % 1.0 == 0.0):
						print("1.0 MOD")


					if(float(talon_rows[i][0]) % 60.0 == 0.0):
						print("60.0 MOD")
					'''

					
					if(abs(time_talon_last - time_talon) > 0.05):
						zero_time_talon = float(talon_rows[i][0]) - .01 - time_talon_last	
						print(" time last: ", float(talon_rows[i-1][0]), " time_talon: ", float(talon_rows[i][0]), " row: ", i)
						time_talon = float(talon_rows[i][0]) - zero_time_talon
		

					while True:
						if(k  > len(logger_rows) -10.0 / 0.1):
							logger_end  = True
							break	

						if(abs(time_logger - time_talon) > abs(float(logger_rows[k + 1][logger_field_names[0]]) - zero_time_logger - time_talon)):
			


							k+=1
						else:
							break
					time_logger = float(logger_rows[k][logger_field_names[0]]) - zero_time_logger
				








if(bool(sys.argv[4])):
	import os
	os.system('python /home/ryan/Documents/hero_thermal_testing/data/data_display.py ' + str(out_name) + ' False')
