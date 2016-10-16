
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.constants as const

g = const.g     # gravitation constant
dt = 1e-3       # integration time step (delta t)
v0 = 2.7       # initial speed at t=0
x0 = -0.229     # initial x coordinate
y0 = 0.406      # initial y coordinate
angle = math.pi / 4     #launch angle in radians
gamm = 0    #gamma (used to compute f, below)
h = 100         #height (used to compute f, below)
fence_height = 2.0 * 0.3048

def traj_fr(angle, v0, x0, y0):             #function that computes trajectory for some launch angle & velocity
    vx0 = math.cos(angle)*v0        #compute x components of starting velocity
    vy0 = math.sin(angle)*v0        #compute y components of starting velocity
    x = [0,0]         #initialise x array
    y = [0,0]         #initialise y array
    x[0],y[0] = x0,y0     #initial position at t=0s, ie motion starts at (0,0)
    x[1],y[1] = x[0] + vx0*(2*dt), y[0]+vy0*(2*dt)  #calculating 2nd elements of x & y based on init velocity

    i=1
    while y[i]>=0:  #loop continuous until y becomes <0, ie projectile hits ground
        f = 0.5 * gamm * (h - y[i]) * dt        #intermediate 'function'; used in calculating x & y vals below
        y.append(((2*y[i]-y[i-1]) + (f * y[i-1]) - g*(dt**2) ) / (1 + f))      # ...& y[i+1]
        x.append(((2*x[i]-x[i-1]) + (f * x[i-1])) / (1 + f))                 #numerical integration to find x[i+1]...
        i = i+1 	#increment i for next iteration

	x = x[0:i+1]        #truncate x array
    y = y[0:i+1]        #truncate y array
    return x, y, (dt*i), x[i]       #return x, y, flight time, range of projectile

n = 19
angles = np.linspace(0, math.pi/2, n)   #generate array of n angles
maxrange = np.zeros(n)                  #generate array of n elements to take range from traj_fr

for i in range(n): 				        #loop to run angles through traj_fr function & populate maxrange array with distance results
    x,y,duration,maxrange[i] = traj_fr(angles[i], v0, x0, y0)
    plt.plot(x,y, color='b', linestyle='-', linewidth=1)       #quick plot of x vs y to check trajectory

angles = angles / 2 / math.pi * 360       #convert radians to degrees
print 'Launch Angles: ', angles
print 'Ranges: ', maxrange
optimal_angle_degrees = angles[np.where(maxrange==np.max(maxrange))]
optimal_angle_radians = optimal_angle_degrees / 180 * math.pi
print 'Optimum Angle and range: ', optimal_angle_degrees, np.max(maxrange)

x,y,duration,range = traj_fr(optimal_angle_radians, v0, x0, y0)

print 'Optimal duration: ' , duration

# find the height at x=0

minimum_x = np.min(np.absolute(x))
index_of_minimum_x = np.where(np.abs(x)==minimum_x)
y_at_x_near_zero = y[index_of_minimum_x[0][0]]

print 'Minimum x:', minimum_x
print 'Height at x ~= 0: ', y_at_x_near_zero

plt.xlabel('x')
plt.ylabel('y')
plt.plot([0,0], [0,y_at_x_near_zero], color='k', linestyle='-', linewidth=2)
plt.show()

#Reference https://www.physicsforums.com/threads/using-python-to-calculate-projectile-motion-with-resistance.848512/
