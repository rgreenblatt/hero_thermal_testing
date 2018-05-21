import csv
import math
import sys

force_conv_factor = .0565		
RPM_conv_factor = 1

logger_name =  str(sys.argv[1])
talon_name =   str(sys.argv[2])#str(input("talon file: "))



out_name =   str(sys.argv[3])#str(input("output file: "))




enable_impose_replace = True
#x rpm:  4194.141  max rpm index:  60.103000000000065
is_max_rpm = 4194.141
is_max_rpm_time =  60.103000000000065
is_start = 8.2

impose_replace_set = [[[0.0, 1000000.0], [-6200, -6200]]]
#[[[1.0, 29.0], [-10800.0, -10800.0]], [[31.0, 59.0], [-3200.0, -3200.0]], [[61.0, 89.0], [-7200.0, -7200.0]],  [[91.0, 119.0], [-9900.0, -10500.0]]]
# [[[0.0, is_start], [0.0, 0.0]], [[is_start, is_max_rpm_time], [0.0, -is_max_rpm]], [[is_max_rpm_time, (is_max_rpm_time - is_start) * 2 + is_start], [-is_max_rpm, 0.0]], [[(is_max_rpm_time - is_start) * 2 + is_start, 100000], [0.0, 0.0]]]

max_RPM = 0 
max_RPM_time = 0

max_voltage = 0 
max_voltage_time = 0

logger_shift = float(sys.argv[4])
logger_shift *= 10
logger_shift = int(logger_shift)

print("logger_shift: ", logger_shift)

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
			if(float(row[3]) > .01):
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

	logger_count += logger_shift
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
				print(zero_time_logger)
		
				
				i = talon_count
				k = logger_count
				logger_end = False
				manual = False
				
				if(len(sys.argv) > 6):
					trial_length = float(sys.argv[6])#float(input("trial length: "))
					print("manual")
					manual = True
				else:
					#trial_length = float(talon_rows[-1][0]) - zero_time_talon - .02
					#trial_length = min(trial_length, float(logger_rows[-1][logger_field_names[0]]) - zero_time_logger) - .2
					trial_length = 0.0
					#print(trial_length)
					 
				print("end_talon_time: ", float(talon_rows[-1][0]), " end_logger_time: ", float(logger_rows[-1][logger_field_names[0]]))


				writer.writeheader()
				while ((time_talon < trial_length or not manual) and (i < len(talon_rows) - 10.0 / 0.01) and not logger_end):
	

				
	
	

					sum_RPM += float(talon_rows[i][2]) * RPM_conv_factor /60.0  * (time_talon - time_talon_last)
					time_talon_last = time_talon

					#print(sum_RPM, " and ", talon_rows[i][1])
				
					rpm = float(talon_rows[i][2]) * RPM_conv_factor
					

	
					if(i != talon_count and abs(last_RPM) - abs(rpm) > 10 and (abs(time_talon % 30.0) < 2.5 or abs(time_talon % 30.0) > 27.5) and i <  10000000):
						print("last rpm: ", last_RPM, "rpm: ", rpm, " row: ", i)

						rpm = last_RPM
	
					if(enable_impose_replace):	
						for impose_replace in impose_replace_set:
							if(time_talon > impose_replace[0][0] and  time_talon < impose_replace[0][1]):
							#print("replacing rpm")
								rpm = (impose_replace[1][1] - impose_replace[1][0]) / (impose_replace[0][1] - impose_replace[0][0]) * (time_talon - impose_replace[0][0]) + impose_replace[1][0]

	

					writer.writerow({'time_talon': time_talon, 'time_logger': time_logger, 'temp1': float(logger_rows[k]['Latest: Temperature 1 (°C)']) + 273.15, 'temp2': float(logger_rows[k]['Latest: Temperature 2 (°C)']) + 273.15,'temp3': float(logger_rows[k]['Latest: Temperature 3 (°C)']) + 273.15,'force': float(logger_rows[k]['Latest: Force (N)']) * force_conv_factor, 'voltage': talon_rows[i][3], 'current': talon_rows[i][4],'RPM': rpm, 'bus_voltage': talon_rows[i][5] })

					last_RPM = rpm

					if(abs(rpm) > max_RPM):
						max_RPM = abs(rpm)
						max_RPM_time = time_talon
					


					if(abs(float(talon_rows[i][3])) > max_voltage):
						max_voltage = abs(float(talon_rows[i][3]))
						max_voltage_time = time_talon
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
				




print("max rpm: ", max_RPM, " max rpm index: ", max_RPM_time)
print("max voltage: ", max_voltage, " max voltage index: ", max_voltage_time)



if(sys.argv[5]=="True" or sys.argv[5]=="true"):
	import os
	os.system('python /home/ryan/Documents/hero_thermal_testing/data/data_display.py ' + str(out_name) + ' False')
