import csv
import math
import sys

import matplotlib.pyplot as plt
import numpy as np



logger_name =  str(sys.argv[1])


time = []

t1 = []
t2 = []
t3 = []




with open(logger_name, 'rt', encoding='utf-8') as logger_csvfile:
	reader = csv.DictReader(logger_csvfile, delimiter=',')
	logger_field_names = reader.fieldnames
	for row in reader:
		time.append(float(row[logger_field_names[0]]))
		t1.append(float(row['Latest: Temperature 1 (°C)']))
		t2.append(float(row['Latest: Temperature 1 (°C)']))
		t3.append(float(row['Latest: Temperature 3 (°C)']))
		
time = np.array(time)
t1 = np.array(t1)
t2 = np.array(t2)
t3 = np.array(t3)

print(t1.size)
print(t1[::50].size)



plt.plot(time[::50], t1[::50])
plt.plot(time[::50], t2[::50])
plt.plot(time[::50], t3[::50])


plt.show()

print("hhhhhhhh")

start = float(input("time start: " ))

start_index = np.nonzero(time > start)[0][0]

time = time[start_index:]
t1 = t1[start_index:]
t2 = t2[start_index:]
t3 = t3[start_index:]



plt.plot(time[::10], t1[::10])
plt.plot(time[::10], t2[::10])
plt.plot(time[::10], t3[::10])


plt.show()


import scipy.optimize as optimize
import scipy.integrate as integrate


t = (t1 + t2 + t3) / 3.0



#returner = np.zeros(time[::10].size)
#index = 0
#def solout(t, y):
#	returner[index] = y 



amb_v = 0
k_v = 0
emis_v = 0



def func(times, ambient, t_initial, k, emis_term):
	global amb_v
	global k_v
	global emis_v
	k_v = k
	amb_v = ambient
	emis_v = emis_term


	returner = np.zeros(times.size)
	returner[0] = t_initial
	
	for i in range(times.size - 1):
		integrator = integrate.solve_ivp(dtemp_func, (times[i], times[i+1]), [returner[i]], 'RK45')
		#integrator.set_solout(solout)
		#print(integrator.y)
		returner[i+1] = integrator.y[0][-1] 


	return returner




def dtemp_func(time, temp):
	global amb_v
	global k_v
	global emis_v

	#print(amb_v)
	#print(k_v)
	#print(emis_v)
	return - k_v * ( temp - amb_v ) + emis_v * (temp*temp*temp*temp - amb_v*amb_v*amb_v*amb_v)


guess = ( 2.09336377e+01,  4.56555121e+01,  5.92638331e-04, -5.91152503e-10) 

print(time[::10].size)
print(t[::10].size)
params, pcov = optimize.curve_fit(func, time[::10], t[::10], guess)
print(params)
#print(pcov)

y_vals = func(time[::10], params[0], params[1], params[2], params[3])


plt.plot(time[::10], y_vals)
plt.plot(time[::10], t[::10])

plt.show()
