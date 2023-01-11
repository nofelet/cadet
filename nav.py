from regulator import CourseRegulator
import math

r = 6372795

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

def calculateAngleAndPower(
    target,
    target_coordinates,
    current_coordinates,
    current_speed,
    current_heading,
    course_regulator):


    """Расчет угла руля и мощности мотора

    # Returns:
    #     angle: угол мотора в градусах от -35 до 35
    #     power: мощность двигателя от -1 до 1"""
    spead = 1
    if target == None:
        newCourse = azimuth2(current_coordinates[0],current_coordinates[1],target_coordinates[0],target_coordinates[1])

    elif target[0] == 1:
        newCourse = current_heading + target[1]
        spead = 0.4
    elif target[0] == 0:
        if target[2] >44 or target[2] < -44:
            if target[2]>79 or target[2] < -79:
                if target[1] <75 or target[1] > -75:
                    return 35 * sign(target[1]),1
                return 0, 1
            return 35*sign(target[2])*-1,1
        newCourse = current_heading + target[1]

    return course_regulator.calculateAngle(current_heading,newCourse),spead
