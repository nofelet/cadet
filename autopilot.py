import math
import numpy
r = 6372795
kp = 0.4
kd = 100
ki = 0.1

def sign(x):
    if x<0:
        return -1
    elif x>0:
        return 1
    else:
        return 0

def azimuth2(latA, longA, latB, longB):
    radLatA = math.radians(latA)
    radLatB = math.radians(latB)
    radDelta = math.radians(longB - longA)
    x = math.cos(radLatA) * math.sin(radLatB) - math.sin(radLatA) * math.cos(radLatB) * math.cos(radDelta)
    y = math.sin(radDelta) * math.cos(radLatB)
    z = math.degrees(math.atan(-1*y/x))
    if x<0 :
        z = z + 180
    z2 = z + 180
    z2 = 180 - math.fmod(z2,360)
    return z2

target = None
target_coordinates = (59.57, 30.19)
current_coordinates = (55.75, 37.61)
current_heading = 0.0
errSum = 0
errCount = 0
errOld = 0
if target == None:
    newCourse = azimuth2(current_coordinates[0],current_coordinates[1],target_coordinates[0],target_coordinates[1])

    err = newCourse - current_heading
    errSum = errSum + err

    errCount = errCount + 1

    if abs(err) > math.pi:
        err = sign(err) * (err - 2 * math.pi)
    dErr = err - errOld

    P = kp * err
    D = kd * dErr
    I = ki * errSum / errCount
    power = P + D + I
    errOld = err



    if abs(power) > math.radians(35):
        power = sign(power) * math.radians(35)

elif len(target[0]) == 2:
    newCourse = abs(target[1][0]-target[1][1])/2

elif len(target[0]) == 1:
    cat1 = math.sin(abs(target[1]))*target[3]
    cat2 = math.cos(abs(target[1]))*target[3]
    newCourse = math.atan(cat1/cat2)

err = newCourse - current_heading
errSum = errSum + err

errCount = errCount + 1

if abs(err) > math.pi:
    err = sign(err) * (err - 2 * math.pi)
dErr = err - errOld

P = kp * err
D = kd * dErr
I = ki * errSum / errCount
power = P + D + I
errOld = err



if abs(power) > math.radians(35):
    power = sign(power) * math.radians(35)



print(power)
print(newCourse)