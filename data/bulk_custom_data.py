import csv
import sys
import matplotlib.pyplot as plt
import numpy as np


#http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay


val_set = [[1.0, 29.0], [31.0, 59.0], [61.0, 89.0], [91.0, 119.0]]

index = 0
for file_name in sys.argv:
	index +=1
	if(index == 1):
		continue

	file_name = str(file_name)
	
	temp1 = []
	temp2 = []
	temp3 = []

	time_logger = []
	time_talon = []

	force = []

	voltage = []
	bus_voltage = []

	current = []

	RPM = []

	with open(file_name, 'rt') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		#print(reader.fieldnames)
		for row in reader:
			temp1.append(float(row['temp1']))
			temp2.append(float(row['temp2']))
			temp3.append(float(row['temp3']))
			time_talon.append(float(row['time_talon']))
			time_logger.append(float(row['time_logger']))
			force.append(float(row['force']))
			voltage.append(float(row['voltage']))
			bus_voltage.append(float(row['bus_voltage']))
			current.append(float(row['current']))
			RPM.append(float(row['RPM']))
		
	force = np.array(force)




	temp1 = np.array(temp1)
	temp2 = np.array(temp2)
	temp3 = np.array(temp3)
	time_talon = np.array(time_talon)

	time_logger = np.array(time_logger)
	force = np.array(force)
	voltage = np.array(voltage)
	bus_voltage = np.array(bus_voltage)#moving_average(np.array(bus_voltage), 1000)
	current = np.array(current)#moving_average(np.array(current), 1000)
	RPM = np.array(RPM)



	import math

	for cuts in val_set:	

		cut_begin =  cuts[0]
		cut_end =  cuts[1]


		import os 
		print(str(np.average((- RPM  * force * 2 * math.pi / 60.0 + bus_voltage * current)[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])) + ", " + str(np.abs(np.average(RPM[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]]))) + ", " + str(np.average(current[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])) + ", " + str(np.average(voltage[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])) + ", " + str(abs(np.average(force[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]]))) + ", " +str(os.getcwd()) + "/" + file_name)

