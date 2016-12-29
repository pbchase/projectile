
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.constants as const

g = const.g     # gravitation constant (meters/second^2)
dt = 1e-3       # integration time step, delta t (seconds)
v0 = 2.1        # initial speed at t=0 (meters/second)
x0 = -0.381     # initial x coordinate (meters)
y0 = 0.406      # initial y coordinate (meters)
radians_per_degree = math.pi/180
angles_in_degrees = np.arange(50,61,5)
angles = angles_in_degrees * radians_per_degree

gamm = 0   #gamma (used to compute f, below)
h = 10     #height (used to compute f, below)
fence_height = 25.25/12 * 0.3048
perimeter_height = (11.5/12)* 0.3048
arena_width = (140.5/12) * 0.3048
high_score_boundary = ((140.5/2-34.63)/12) * 0.3048

def traj_fr(angle, v0, x0, y0):  #function that computes trajectory for some launch angle & velocity
    vx0 = math.cos(angle)*v0     #compute x components of starting velocity
    vy0 = math.sin(angle)*v0     #compute y components of starting velocity
    x = [0,0]            #initialise x array
    y = [0,0]            #initialise y array
    x[0],y[0] = x0,y0    #initial position at t=0s, ie motion starts at (0,0)
    x[1],y[1] = x[0] + vx0*(2*dt), y[0]+vy0*(2*dt)  #calculating 2nd elements of x & y based on init velocity

    i=1
    while y[i]>=0:  #loop continuous until y becomes <0, ie projectile hits ground
        f = 0.5 * gamm * (h - y[i]) * dt        #intermediate 'function'; used in calculating x & y vals below
        y.append(((2*y[i]-y[i-1]) + (f * y[i-1]) - g*(dt**2) ) / (1 + f))      # ...& y[i+1]
        x.append(((2*x[i]-x[i-1]) + (f * x[i-1])) / (1 + f))     #numerical integration to find x[i+1]...
        i = i+1 	#increment i for next iteration

	x = x[0:i+1]        #truncate x array
    y = y[0:i+1]        #truncate y array
    return x, y, (dt*i), x[i]       #return x, y, flight time, range of projectile

n = len(angles)
maxrange = []

for i in range(n): 		#loop to run angles through traj_fr function & populate maxrange array with distance results
    x,y,duration,range = traj_fr(angles[i], v0, x0, y0)
    maxrange.append(range)
    plt.plot(x,y, color='b', linestyle='-', linewidth=1)       #quick plot of x vs y to check trajectory

# Print critical inputs
init_speed = 'Initial speed at t=0 (m/s): ' + str(v0)
init_x = 'Initial x coordinate (m): ' + str(x0)
init_y = 'Initial y coordinate (m): ' + str(y0)
print init_speed
print init_x
print init_y

maxrange = np.round(maxrange,2)
print 'Launch angles above horizon (degrees): ', angles_in_degrees
print 'x-coordinates at y=0 (m): ', maxrange
optimal_angle_degrees = angles_in_degrees[np.where(maxrange==np.max(maxrange))]
optimal_angle_radians = optimal_angle_degrees * radians_per_degree
max_x = 'Maximum x at impact (m): ' + str(np.max(maxrange))
angle_for_max_x = 'Angle for maximum x at impact (degrees): ' + str(optimal_angle_degrees)
print max_x
print angle_for_max_x

x,y,duration,range = traj_fr(optimal_angle_radians, v0, x0, y0)

print 'Duration of flight for maximum x (s): ' , duration

plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Predicted trajectories')
plt.plot([0,0], [0,fence_height], color='k', linestyle='-', linewidth=2)
plt.plot([-arena_width/2,-arena_width/2], [0,perimeter_height], color='k', linestyle='-', linewidth=2)
plt.plot([arena_width/2,arena_width/2], [0,perimeter_height], color='k', linestyle='-', linewidth=2)
plt.plot([high_score_boundary, high_score_boundary], [0,0.01], color='k', linestyle='-', linewidth=2)
plt.axis([-2, 2, -0.0, 1.5])

newline="\n"
text_label = newline.join((init_speed, init_x, init_y, max_x, angle_for_max_x))
plt.text(-1.9, 1.1, text_label )

plt.show()

#Reference https://www.physicsforums.com/threads/using-python-to-calculate-projectile-motion-with-resistance.848512/
