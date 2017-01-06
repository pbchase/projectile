
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.constants as const

g = 9.81     # gravitation constant (meters/second^2)
dt = 0.001       # integration time step, delta t (seconds)
v0 = 4.0        # initial speed at t=0 (meters/second)
x0 = -0.381     # initial x coordinate (meters)
y0 = 0.406      # initial y coordinate (meters)
radians_per_degree = math.pi/180
angles_in_degrees = np.arange(50,61,5)
angles = angles_in_degrees * radians_per_degree

fence_height = 25.25/12 * 0.3048
perimeter_height = (11.5/12)* 0.3048
arena_width = (140.5/12) * 0.3048
high_score_boundary = ((140.5/2-34.63)/12) * 0.3048

def traj_fr(angle, v0, x0, y0):  #function that computes trajectory for some launch angle & velocity
    vx0 = math.cos(angle)*v0     #compute x components of starting velocity
    vy0 = math.sin(angle)*v0     #compute y components of starting velocity
    x = [0]            #initialise x array
    y = [0]            #initialise y array
    vy = [0]
    x[0],y[0] = x0,y0    #initial position at t=0s, ie motion starts at (0,0)
    vy[0] = vy0
    x.append(x[0] + vx0*dt)
    y.append(y[0] + vy[0]*dt - 0.5 * g * dt**2)  #calculating 2nd elements of x & y based on init velocity
    vy.append(vy[0] - g*dt)

    i=1
    while y[i]>=0:  #loop continuous until y becomes <0, ie projectile hits ground
        i = i+1     #increment i for next iteration
        y.append( (y[i-1]) + vy[i-1]*dt  - 0.5 * g * dt**2 )
        x.append( x[i-1] + vx0*dt )
        vy.append( vy[i-1] - g*dt )

    return x, y, (dt*i), x[i]       #return x, y, flight time, range of projectile

n = len(angles)
maxrange = []
durations = []

for i in range(n): 		#loop to run angles through traj_fr function & populate maxrange array with distance results
    x,y,duration,range = traj_fr(angles[i], v0, x0, y0)
    maxrange.append(range)
    durations.append(duration)
    plt.plot(x,y, color='b', linestyle='-', linewidth=1)       #quick plot of x vs y to check trajectory

# Print critical inputs
init_speed = 'Initial speed at t=0 (m/s): ' + str(v0)
init_x = 'Initial x coordinate (m): ' + str(x0)
init_y = 'Initial y coordinate (m): ' + str(y0)
print "time increment (s): ", dt
print init_speed
print init_x
print init_y

maxrange = np.round(maxrange,2)
print 'Launch angles above horizon (degrees): ', angles_in_degrees
print 'x-coordinates at y=0 (m): ', maxrange
print 'durations at y=0 (s): ', durations
optimal_angle_degrees = angles_in_degrees[np.where(maxrange==np.max(maxrange))]
optimal_angle_radians = optimal_angle_degrees * radians_per_degree
max_x = 'Maximum x at impact (m): ' + str(np.max(maxrange))
angle_for_max_x = 'Angle for maximum x at impact (degrees): ' + str(optimal_angle_degrees)
print max_x
print angle_for_max_x

x,y,duration,range = traj_fr(optimal_angle_radians, v0, x0, y0)
time_for_max_x = 'Duration of flight for maximum x (s): ' + str(duration)
print time_for_max_x

plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Predicted trajectories')
plt.plot([0,0], [0,fence_height], color='k', linestyle='-', linewidth=2)
plt.plot([-arena_width/2,-arena_width/2], [0,perimeter_height], color='k', linestyle='-', linewidth=2)
plt.plot([arena_width/2,arena_width/2], [0,perimeter_height], color='k', linestyle='-', linewidth=2)
plt.plot([high_score_boundary, high_score_boundary], [0,0.01], color='k', linestyle='-', linewidth=2)
plt.axis([-2, 2, -0.0, 1.5])

newline="\n"
text_label = newline.join((init_speed, init_x, init_y, max_x, angle_for_max_x, time_for_max_x))
plt.text(-1.9, 1.1, text_label )

plt.show()

#Reference https://www.physicsforums.com/threads/using-python-to-calculate-projectile-motion-with-resistance.848512/
