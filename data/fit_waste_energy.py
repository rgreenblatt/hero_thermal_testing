
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


with open('waste_data.csv', 'rt') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		#print(row)
		x_a.append(float(row["current"]))
		y_a.append(float(row["RPM"]))
		f_a.append(float(row["force"]))
		z_a.append(float(row["waste_watts"]))
		k_a.append(float(row["voltage"]))



x_a = np.array(x_a)
k_a = np.array(k_a)
f_a = np.array(f_a)
y_a = np.array(y_a)
z_a = np.array(z_a)



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
	return data[0] * data[0] *  a + data[1] * c

guess = ( 0.055401662, 0.001333333 )


params, pcov = optimize.curve_fit(func, independent, z_a, guess)
print(params)
print(pcov)


X = np.arange(0, 25, 0.25)
Y = np.arange(0, 17000, 170)

X, Y = np.meshgrid(X, Y)

Z = X * X * params[0] +  +params[1] *Y

ax.plot_wireframe(X, Y, Z)





ax.scatter((np.array(z_a) + np.array(y_a) *  np.array(f_a) * 2 * math.pi / 60.0) / k_a, np.array(y_a), np.array(z_a))

ax.set_xlim(0, 25)
ax.set_ylim(0, 17000)
ax.set_zlim(0, 100)

plt.show()



