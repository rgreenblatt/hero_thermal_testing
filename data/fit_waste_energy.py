from __future__ import print_function

import scipy.optimize as optimize
import csv

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
from math import pi



x_a = []
e_a = []
w_a = []
y_a = []
z_a = []
k_a = []
f_a = []
b_a = []


weight_local_no_stall = 0.2
weight_local_stall = 10.0
weight_curve_data = 1.0

with open('waste_data_new.csv', 'rt') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		#print(row)
	

		if(float(row["RPM"]) > 3.0):
			w_a.append(weight_local_no_stall)
		else:
			w_a.append(weight_local_stall)
			
				
		e_a.append(1.0)
		print(row["file_address"])
		x_a.append(float(row["current"]))
		y_a.append(float(row["RPM"]) / 60 * 2 *pi)
		f_a.append(float(row["force"]))
		z_a.append(float(row["waste_watts"]))
		k_a.append(float(row["voltage"]))
		b_a.append((float(row["waste_watts"]) + float(row["RPM"]) *  float(row["force"]) * 2 * math.pi / 60.0) / float(row["current"]))



e_p = []
w_p = []
s_p = []
c_p = []
v_p = []
b_p = []
wl_p =[]



with open('../../../../775pro-motor-curve-data.csv', 'rt') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		w_p.append(weight_curve_data)
		e_p.append(0.0)
		s_p.append(float(row['Speed (RPM)']) / 60 * 2 * pi)
		c_p.append(float(row['Current (A)']))
		wl_p.append(float(row['Power Dissipation (W)']))
		v_p.append(12)
		b_p.append(12)


w_p = np.array(w_p)
w_a = np.array(w_a)
e_p = np.array(e_p)
e_a = np.array(e_a)
v_p = np.array(v_p)
b_p = np.array(b_p)
x_a = np.array(x_a)
k_a = np.array(k_a)
f_a = np.array(f_a)
y_a = np.array(y_a)
z_a = np.array(z_a)
s_p = np.array(s_p)
c_p = np.array(c_p)
wl_p =np.array(wl_p)

'''

plt.title("current")
plt.scatter(x_a, z_a)
plt.show()

plt.title("force")
plt.scatter(f_a, z_a)
plt.show()

plt.title("voltage")
plt.scatter(k_a, z_a)
plt.show()


plt.title("bus_voltage")
plt.scatter(b_a, z_a)
plt.show()





plt.scatter((np.array(z_a) + np.array(y_a) *  np.array(f_a) * 2 * math.pi / 60.0) / k_a, z_a)
plt.show()


plt.scatter(k_a, z_a)
plt.show()
		
plt.scatter(x_a, z_a)
plt.show()


plt.scatter(y_a, z_a)
plt.show()


fig = plt.figure()
ax = Axes3D(fig)


independent = np.array([(np.array(z_a) + np.array(y_a) *  np.array(f_a) * 2 * math.pi / 60.0)/k_a, y_a])



def func(data, a, c):
	b = 0
	return data[0] * data[0] *  a + data[1] * c + data[1] * data[1] * b

guess = ( 0.055401662,  0.001333333 )


params, pcov = optimize.curve_fit(func, independent, z_a * eff, guess)
print(params)
print(pcov)



X = np.arange(0, 25, 0.25)
Y = np.arange(0, 17000, 170)

X, Y = np.meshgrid(X, Y)

Z = X * X * params[0]  + params[1] * Y #+ params[1] * Y * Y

ax.plot_wireframe(X, Y, Z)





ax.scatter((np.array(z_a) + np.array(y_a) *  np.array(f_a) * 2 * math.pi / 60.0) / k_a, np.array(y_a), np.array(z_a) * eff)

ax.set_xlim(0, 25)
ax.set_ylim(0, 17000)
ax.set_zlim(0, 100)

plt.show()
#Motor curve data:


#plt.scatter(c_p, wl_p)
#plt.show()


#plt.scatter(c_p, wl_p)
#plt.show()


#plt.scatter(s_p, wl_p)
#plt.show()


fig = plt.figure()
ax = Axes3D(fig)


independent = np.array([c_p, s_p])


guess = ( 0.055401662, 0.0000001,  0.001333333 )

ones = np.full(wl_p.shape, 1.0)
print(ones)

def func(data, a, b, c):
	return (data[0] * data[0] *  a + data[1] * c + data[1] * data[1] * b) / wl_p

params, pcov = optimize.curve_fit(func, independent, ones, guess)
print("motor data")

print(params)
print(pcov)


X = np.arange(-5, 160, 5)
Y = np.arange(0, 20000, 800)

X, Y = np.meshgrid(X, Y)

Z = X * X * params[0]  + params[2] * Y+ params[1] * Y * Y

ax.plot_wireframe(X, Y, Z, color='orange')





ax.scatter(c_p, np.array(s_p), np.array(wl_p))

ax.set_xlim(-5, 160)
ax.set_ylim(0, 20000)
ax.set_zlim(0, 2000)

plt.show()


'''
#full data set

eff = 0.95


wl_f = np.hstack((z_a * eff, wl_p))
c_f = np.hstack((x_a, c_p))
s_f = np.hstack((y_a, s_p))
v_f = np.hstack((k_a,v_p))
b_f = np.hstack((b_a,b_p))
e_f = np.hstack((e_a,e_p))
w_f = np.hstack((w_a,w_p))

print("wlp shape: ", wl_p.shape, "za shape: ", z_a.shape)

ones = np.full(wl_f.shape, 1.0)

independent2 = np.array([c_f, s_f, v_f, e_f])


guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03, 7.48935360e+00, -2.20884602e-02, 0.00001) 


def func(data, a, b, c, d, e, f):
	return (data[0] * data[0] *  a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e  - data[3] * data[1] *f) / wl_f

params, pcov = optimize.curve_fit(func, independent2, ones, guess)

print("without curr term, quadratic v fit")
print(params)

#for c, s, v, w in zip(inde


#def mse(f, data, 




#print("mse f1: " (


independent3 = np.array([c_f, s_f, v_f, b_f, e_f, w_f])


guess = (8.49558651e-02, 3.18269661e-07, 0.0001, 0.0001, 0.00001, 0.0001) 


def func5(data, a, b, c, d, e, f):

	return (data[0] * a + data[0] *  data[0]* b  + data[1] * c + data[1] * data[1] * d + data[1] *  data[1]* data[1] * e - data[1] * data[4] * f) / wl_f

params7, pcov = optimize.curve_fit(func5, independent3, ones, guess)
print("with curr term, quadratic v fit")
print(params7)





guess = (8.49558651e-02, 3.18269661e-07, 0.0001, 0.0001, 0.000001) 


def func8(data, a, b, c, d, e):

	return (data[0] * a + data[0] *  data[0]* b  + data[1] * c + data[1] * data[1] * d - data[1] * data[4] * e) / wl_f

params8, pcov = optimize.curve_fit(func8, independent3, ones, guess)
print("with curr term, quadratic v fit")
print(params7)











guess = (8.49558651e-02, 3.18269661e-07, 0.0001, 0.0001, 0.00001) 

def func6(data, a, b, c, d, e):

	return (data[0] * a + data[0] *  data[0]* b + data[2] * c + data[2] * data[2] * d - data[1] * data[4] * e ) / wl_f

params6, pcov = optimize.curve_fit(func6, independent3, ones, guess)
print("with curr term, quadratic v fit")
print(params6)












guess = (6.57641200e-01, -1.59275713e-03,   2.32639233e-03, 9.39662805e-04, 8.49558651e-02, -3.18269661e-07)#, 1.78534872e-03, 7.48935360e+00, -2.20884602e-02, 0.00001, 0.00001, 0.001, 1.0) 

def func1(data, a, b, c,  j, h, k):
    curr_term = np.where(data[2] > 0.1, data[0] * data[0] *  data[3] / data[2] ** 2, data[0] * data[0] *  data[3] / 0.1 ** 2)
    return ((curr_term * a + data[1] * c + data[1] * data[1] * b +  data[0] **abs(h) * data[2] **abs(k) * j) / wl_f - 1)* data[5] +1





params1, pcov = optimize.curve_fit(func1, independent3, ones, guess, maxfev = 18000)
print("with curr term, quadratic v fit func1")
print(params1)




















guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03)


def func9(data, a, b, c):

	curr_term = np.where(data[2] > 0.1, data[0] *data[0] *  data[3] / data[2] ** 2, data[0] * data[0] *  data[3] / 0.1 ** 2)

	return ((curr_term * a  + data[1] * b + data[1] * data[1] * c  ) / wl_f - 1) *data[5] + 1

params9, pcov = optimize.curve_fit(func9, independent3, ones, guess, maxfev = 8000)
print("with curr term, quadratic v fit func9")
print(params9)




'''
fig = plt.figure()
ax = Axes3D(fig)

#ax.scatter(c_f, np.array(s_f), np.array(wl_f))


#X = np.arange(-5, 160, 5)
#Y = np.arange(0, 20000, 800)

#X, Y = np.meshgrid(X, Y)

#Z = X * params7[0] + X * X * params7[1]  + params7[2] * Y + params7[3] * Y * Y
Z = func9(independent3, params9[0], params9[1], params9[2], params9[3], params9[4]) - 1.0


ax.scatter(c_f, np.array(s_f), Z)

plt.title("current and speed residuals func 9")

ax.set_xlim(-5, 160)
ax.set_ylim(0, 20000)

plt.show()








#ax.scatter(c_f, np.array(s_f), np.array(wl_f))


#X = np.arange(-5, 160, 5)
#Y = np.arange(0, 20000, 800)

#X, Y = np.meshgrid(X, Y)

#Z = X * params7[0] + X * X * params7[1]  + params7[2] * Y + params7[3] * Y * Y
Z = c_f * params7[0] + c_f * c_f * params7[1]  + params7[2] * s_f + params7[3] * s_f * s_f - wl_f


ax.scatter(c_f, np.array(s_f), Z)

plt.title("current and speed residuals")

ax.set_xlim(-5, 160)
ax.set_ylim(0, 20000)
ax.set_zlim(0, 2000)

plt.show()
'''

guess = (1.05, -3.18269661e-07, 1.78534872e-03, .00001) 


def func2(data, a, b, c, f):
	d = 0
	e = 0

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / (data[2] * data[2]), 0)

	return (curr_term * a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e - data[1] * data[4] * f) / wl_f

params2, pcov = optimize.curve_fit(func2, independent3, ones, guess)
print("with curr term and extra div no quadratic v fit func2")
print(params2)


independent4 = np.array([c_f, s_f, v_f, b_f])


guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03, 0.0001) 


def func3(data, a, b, c, e):

	d = 1.5

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / (data[2] ** d), 0)

	return (curr_term * a + data[1] * c + data[1] * data[1] * b - data[1] * data[4] * e) / wl_f

params3, pcov = optimize.curve_fit(func3, independent3, ones, guess, maxfev = 10000)
print("with curr term and extra div ^2 no quadratic v fit func3")
print(params3)






guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03, 0.0001, 0.0001) 


def func4(data, a, b, c, d, f):
	e = 0

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / (data[2] * data[2]), 0)

	return (curr_term * a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e- data[1] * data[4] * f) / wl_f

params4, pcov = optimize.curve_fit(func4, independent3, ones, guess)
print("with curr term and extra div, linear v fit func4")
print(params4)




mse_1 = (((func1(independent3, params1[0],  params1[1], params1[2],  params1[3], params1[4],  params1[5])) - 1.0)**2).mean(axis=None)
mse_2 = ((func2(independent3, params2[0],  params2[1],  params2[2],  params2[3]) - 1.0)**2).mean(axis=None)
mse_3 = ((func3(independent3, params3[0],  params3[1], params3[2],  params3[3]) - 1.0)**2).mean(axis=None)
mse_4 = ((func4(independent3, params4[0],  params4[1], params4[2], params4[3],  params4[4]) - 1.0)**2).mean(axis=None)
mse_5 = ((func5(independent3, params7[0],  params7[1], params7[2], params7[3], params7[4],  params7[5]) - 1.0)**2).mean(axis=None)
mse_6 = ((func6(independent3, params6[0],  params6[1], params6[2], params6[3],  params6[4]) - 1.0)**2).mean(axis=None)
mse_7 = ((func8(independent3, params8[0],  params8[1], params8[2], params8[3],  params8[4]) - 1.0)**2).mean(axis=None)
mse_8 = ((func9(independent3, params9[0],  params9[1], params9[2]) - 1.0)**2).mean(axis=None)
	

print("mse 1: ", mse_1, " mse 2: ", mse_2, " mse 3: ", mse_3, " mse 4: ", mse_4, " mse 5: ", mse_5, " mse 6: ", mse_6, " mse 7: ", mse_7," mse 8: ", mse_8)

















