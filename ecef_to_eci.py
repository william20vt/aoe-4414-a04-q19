# ecef_to_eci.py
#
# Usage: python3 ymdhms_to_jd.py I J K Hour Minute Second
#  Converts date to fractional julian date using the ACM letters to the edditor fortran equation and other conversions
# Parameters:
#  I:year
#  J=month
#  K=day
#  Hour
#  Minute
#  Second
#  ecef x
#  ecef y
#  ecef z
#  ...
# Output:
#  ECI components
#
# Written by William Sosnowski
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import sys # argv
import math

# "constants"
# e.g., R_E_KM = 6378.137

# helper functions

## function description
# def calc_something(param1, param2):
#   pass

# initialize script arguments
I=float('nan')
J=float('nan')
K=float('nan')
Hour=float('nan')
Minute=float('nan')
Second=float('nan')
x=float('nan')
y=float('nan')
z=float('nan')

# parse script arguments
if len(sys.argv)==10:
  I = float(sys.argv[1])
  J  = float(sys.argv[2])
  K = float(sys.argv[3])
  Hour = float(sys.argv[4])
  Minute = float(sys.argv[5])
  Second = float(sys.argv[6])
  x=float(sys.argv[7])
  y=float(sys.argv[8])
  z=float(sys.argv[9])
  


else:
  print(\
  'Usage: '\
  'python3 ymdhms_to_jd.py  Year Month Day Hour Minute Seconds xkm ykm zkm'\
  )
  exit()


#converting hour min and sec to portion of the day (k) value

#K=K+(Hour/24)+(Minute/1440)+(Second/86400)
K = K + (Hour/24.0) + (Minute/1440.0) + (Second/86400.0)

if J <= 2:  # Adjust for January and February
    I = I-1
    J = J+12

#JD=K-32075+1461*(I+4800+(J-14)/12)/4+
#     367*(J-2-(J-14)/144)/12-
#     3*((I+4900+(J-14)/12)/100)/4
#off by 0.5 to 1.5
#JD = K - 32075 + math.floor(1461*(I+4800+(J-14)/12)/4)+\
 #    math.floor(367*(J-2-12*((J-14)/12))/12)-\
 #    math.floor(3*((I+4900+(J-14)/12)/100)/4)
 #also off, forgot to account for the fact that fortrane uses integers
JD = (K - 32075 + 
      math.floor(1461*(I+4800 +(J-14)//12)/4)+ 
      math.floor(367*(J-2-12*((J-14)//12))/12)- 
      math.floor(3*((I+4900+(J-14)//12)//100)/4))

jd_frac=JD-2.5


print(jd_frac)

t = (jd_frac - 2451545.0) / 36525.0
    
    # GMST in seconds
gmst_seconds = 280.46061837 + 360.98564736629 * (jd_frac - 2451545.0) + t * t * (0.000387933 - t / 38710000.0)
    
    # Normalize to [0, 360) degrees and convert to radians
gmst_degrees = gmst_seconds % 360.0
gmst_radians=gmst_degrees*(math.pi/180.0)

g=67310.54841+(876600*60*60+8640184.812866)*t+0.093104*t*t+(-6.2*10**-6)*t**3
gg=g %360

print(gmst_degrees)
rads=-gmst_radians

#R = [
#        [math.cos(rads) , -math.sin(rads), 0],
#        [math.sin(rads) ,  math.cos(rads), 0],
#        [              0,               0, 1]
#    ]

RT= [
        [math.cos(rads), math.sin(rads), 0],
        [-math.sin(rads), math.cos(rads), 0],
        [0              , 0,              1]
]

eci_x_km = R[0][0] * x + R[0][1] * y + R[0][2] * z
eci_y_km = R[1][0] * x + R[1][1] * y + R[1][2] * z
eci_z_km = R[2][0] * x + R[2][1] * y + R[2][2] * z

print(eci_x_km)
print(eci_y_km)
print(eci_z_km)