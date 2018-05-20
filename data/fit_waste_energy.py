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

wl_f = np.hstack((z_a * eff,np.hstack((z_a * eff,np.hstack((z_a * eff, np.hstack((z_a * eff, wl_p))))))))
c_f = np.hstack((x_a,np.hstack((x_a,np.hstack((x_a, np.hstack((x_a, c_p))))))))
s_f = np.hstack((y_a,np.hstack((y_a,np.hstack((y_a, np.hstack((y_a, s_p))))))))
v_f = np.hstack((k_a,np.hstack((k_a,np.hstack((k_a, np.hstack((k_a,v_p))))))))
b_f = np.hstack((b_a,np.hstack((b_a,np.hstack((b_a, np.hstack((b_a,b_p))))))))

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


guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03, 7.48935360e+00, -2.20884602e-02, 1.15) 


def func1(data, a, b, c, d, e, f):

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / data[2] ** f, 0)

	return curr_term * a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e

params1, pcov = optimize.curve_fit(func1, independent3, wl_f, guess)
print("with curr term, quadratic v fit")
print(params1)




independent3 = np.array([c_f, s_f, v_f, b_f])


guess = (1.05, -3.18269661e-07, 1.78534872e-03) 


def func2(data, a, b, c):
	d = 0
	e = 0

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / (data[2] * data[2]), 0)

	return curr_term * a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e

params2, pcov = optimize.curve_fit(func2, independent3, wl_f, guess)
print("with curr term and extra div no quadratic v fit")
print(params2)


independent4 = np.array([c_f, s_f, v_f, b_f])


guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03) 


def func3(data, a, b, c):

	d = 1.5

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / (data[2] ** d), 0)

	return curr_term * a + data[1] * c + data[1] * data[1] * b 

params3, pcov = optimize.curve_fit(func3, independent3, wl_f, guess, maxfev = 10000)
print("with curr term and extra div ^2 no quadratic v fit")
print(params3)






guess = (8.49558651e-02, -3.18269661e-07, 1.78534872e-03, 0.0001) 


def func4(data, a, b, c, d):
	e = 0

	curr_term = np.where(data[2] > 0.2, data[0] * data[0] *  data[3] / (data[2] * data[2]), 0)

	return curr_term * a + data[1] * c + data[1] * data[1] * b + data[2] *d  +data[2] *data[2] *e

params4, pcov = optimize.curve_fit(func4, independent3, wl_f, guess)
print("with curr term and extra div, linear v fit")
print(params4)




mse_1 = (((func1(independent3, params1[0],  params1[1], params1[2],  params1[3], params1[4], params1[5])) - wl_f)**2).mean(axis=None)
mse_2 = ((func2(independent3, params2[0],  params2[1],  params2[2]) - wl_f)**2).mean(axis=None)
mse_3 = ((func3(independent3, params3[0],  params3[1], params3[2]) - wl_f)**2).mean(axis=None)
mse_4 = ((func4(independent3, params4[0],  params4[1], params4[2], params4[3]) - wl_f)**2).mean(axis=None)
	

print("mse 1: ", mse_1, " mse 2: ", mse_2, " mse 3: ", mse_3, " mse 4: ", mse_4)

















