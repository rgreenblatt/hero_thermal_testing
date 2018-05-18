from __future__ import print_function
import scipy.optimize as optimize
import csv

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math




x_a = []
y_a = []
z_a = []
k_a = []
f_a = []
b_a = []


with open('waste_data.csv', 'rt') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		#print(row)
		x_a.append(float(row["current"]))
		y_a.append(float(row["RPM"]))
		f_a.append(float(row["force"]))
		z_a.append(float(row["waste_watts"]))
		k_a.append(float(row["voltage"]))
		b_a.append((float(row["waste_watts"]) + float(row["RPM"]) *  float(row["force"]) * 2 * math.pi / 60.0) / float(row["current"]))



s_p = []
c_p = []
v_p = []
b_p = []
wl_p =[]



with open('../../../../775pro-motor-curve-data.csv', 'rt') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		s_p.append(float(row['Speed (RPM)']))
		c_p.append(float(row['Current (A)']))
		wl_p.append(float(row['Power Dissipation (W)']))
		v_p.append(12)
		b_p.append(12)


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

eff = 1.0

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
'''
#Motor curve data:


plt.scatter(c_p, wl_p)
plt.show()


plt.scatter(c_p, wl_p)
plt.show()


plt.scatter(s_p, wl_p)
plt.show()


fig = plt.figure()
ax = Axes3D(fig)


independent = np.array([c_p, s_p])


guess = ( 0.055401662, 0.0000001,  0.001333333 )


def func(data, a, b, c):
	return data[0] * data[0] *  a + data[1] * c + data[1] * data[1] * b

params, pcov = optimize.curve_fit(func, independent, wl_p, guess)
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


#full data set
print(str("wl_p: ") )
print( wl_p)

eff = 0.8

wl_f = np.hstack((wl_p, z_a * eff))
print(wl_f)
c_f  = np.hstack((c_p, x_a))
s_f = np.hstack((s_p, y_a))
v_f = np.hstack((v_p,k_a))
b_f = np.hstack((b_p,b_a))

print("s1: ",  wl_f.shape, "s2: ",  c_f.shape, "s3: ",  s_f.shape, "s1: ",  v_f.shape)


independent2 = np.array([c_f, s_f, v_f])


guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03, 7.48935360e+00, -2.20884602e-02) 


def func(data, a, b, c, d, e):
	return data[0] * data[0] *  a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e

params, pcov = optimize.curve_fit(func, independent2, wl_f, guess)

print("without curr term, quadratic v fit")
print(params)

#for c, s, v, w in zip(inde


#def mse(f, data, 



#print("mse f1: " (

independent3 = np.array([c_f, s_f, v_f, b_f])


guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03, 7.48935360e+00, -2.20884602e-02) 


def func(data, a, b, c, d, e):

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / data[2], 0)

	return curr_term * a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e

params, pcov = optimize.curve_fit(func, independent3, wl_f, guess)
print("with curr term, quadratic v fit")
print(params)




independent3 = np.array([c_f, s_f, v_f, b_f])


guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03) 


def func(data, a, b, c):
	d = 0
	e = 0

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / (data[2] * data[2]), 0)

	return curr_term * a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e

params, pcov = optimize.curve_fit(func, independent3, wl_f, guess)
print("with curr term and extra div no quadratic v fit")
print(params)


















