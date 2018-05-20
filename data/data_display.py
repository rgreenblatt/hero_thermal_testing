import csv
import sys
import matplotlib.pyplot as plt
import numpy as np


#http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')



def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n



file_name =  str(sys.argv[1])

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
	
#for volt in time_talon:
#	print(volt)

#voltage = savitzky_golay(np.array(voltage), 101, 3)
#current = savitzky_golay(np.array(current), 101, 3)
#RPM = savitzky_golay(np.array(RPM), 101, 3)
force = np.array(force)

print(force.size)
#force = moving_average(force, 100)    #savitzky_golay(np.array(force), 101, 3)



temp1 = np.array(temp1)
temp2 = np.array(temp2)
temp3 = np.array(temp3)
time_talon = np.array(time_talon)

print(time_talon.size)
print(force.size)
time_logger = np.array(time_logger)
force = np.array(force)
voltage = np.array(voltage)
bus_voltage = np.array(bus_voltage)#moving_average(np.array(bus_voltage), 1000)
current = np.array(current)#moving_average(np.array(current), 1000)
RPM = np.array(RPM)



import math


plt.title("Bus Voltage")
plt.plot(time_talon[::3], bus_voltage[::3])
plt.show()


plt.title("RPM")
plt.plot(time_talon[::3], RPM[::3])
plt.show()

plt.title("force")
plt.plot(time_talon[::3], force[::3])
plt.show()

plt.title("ma force")
plt.plot(time_talon[::3][50:-49], moving_average(force[::3], 100))
plt.show()


plt.title("current")
plt.plot(time_talon[::3], current[::3])
plt.show()



plt.title("force * 100 v current v voltage")
plt.plot(time_talon[::3], force[::3] * 100)
plt.plot(time_talon[::3], current[::3])
plt.plot(time_talon[::3], voltage[::3])
plt.show()

plt.title("rpm / 1000 v current v voltage")
plt.plot(time_talon[::3], RPM[::3] /  1000)
plt.plot(time_talon[::3], current[::3])
plt.plot(time_talon[::3], voltage[::3])
plt.show()

plt.title("voltage")
plt.plot(time_talon[::3], voltage[::3])
plt.show()


plt.title("temp1")
plt.plot(time_talon[::3], temp1[::3])
plt.show()

plt.title("temp2")
plt.plot(time_talon[::3], temp2[::3])
plt.show()

plt.title("temp3")
plt.plot(time_talon[::3], temp3[::3])
plt.show()

plt.plot(time_talon[::3], bus_voltage[::3] * current[::3])
plt.plot(time_talon[::3], RPM[::3]  * force[::3] * 2 * math.pi / 60.0)
plt.show()







plt.plot(time_talon[::3][50:-49], moving_average(- RPM[::3]  * force[::3] * 2 * math.pi / 60.0 + (bus_voltage[::3] * current[::3]), 100))
plt.show()

if('True' == sys.argv[2]):


	plt.plot(time_talon[::3], RPM[::3])
	plt.show()

	cut_begin =  float(raw_input("begin: "))
	cut_end =  float(raw_input("end: "))

	print(np.nonzero(time_talon > cut_begin)[0][0])
	print(np.nonzero(time_talon > cut_end)[0][0])


	plt.plot(time_talon[np.nonzero(time_talon > cut_begin)[0][0]:np.nonzero(time_talon > cut_end)[0][0]], (- RPM  * force * 2 * math.pi / 60.0 + (bus_voltage * current))[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])

	plt.show()

	plt.plot(time_talon[np.nonzero(time_talon > cut_begin)[0][0]:np.nonzero(time_talon > cut_end)[0][0]], (voltage)[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])

	plt.show()


	plt.plot(time_talon[np.nonzero(time_talon > cut_begin)[0][0]:np.nonzero(time_talon > cut_end)[0][0]], (RPM)[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])

	plt.show()


	print("avg waste watts", np.average((- RPM  * force * 2 * math.pi / 60.0 + bus_voltage * current)[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]]))

	print("avg RPM", np.abs(np.average(RPM[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])))

	print("avg current", np.average(current[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]]))
	print("avg voltage", np.average(voltage[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]]))
	print("avg force", abs(np.average(force[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])))

	import os 
	print(str(os.getcwd()) + "/" + file_name)

	print(str(np.average((- RPM  * force * 2 * math.pi / 60.0 + bus_voltage * current)[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])) + ", " + str(np.abs(np.average(RPM[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]]))) + ", " + str(np.average(current[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])) + ", " + str(np.average(voltage[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]])) + ", " + str(abs(np.average(force[np.nonzero(time_talon > cut_begin)[0][0] : np.nonzero(time_talon > cut_end)[0][0]]))) + ", " +str(os.getcwd()) + "/" + file_name)



	#plt.plot(time_talon[::3], force[::3])
	#plt.show()

	#plt.plot(time_talon[::3], RPM[::3])
	#plt.show()

	#plt.plot(time_talon[::3], voltage[::3])
	#plt.show()


	#plt.plot(time_talon[::3], bus_voltage[::3])
	#plt.show()


	#plt.plot(time_talon[::3], current[::3])
	#plt.show()
