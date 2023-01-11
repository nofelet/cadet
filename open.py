import numpy
import cv2
import math

varots = [18,53]

def imageSecondProcessing(tvec,ids):
    if len(tvec) > 2:
        if ids[0] == 33:
            distance_to_target = math.sqrt(tvec[0][0][2] ** 2 + tvec[0][0][0] ** 2)
            target_bearing = math.atan2(tvec[0][0][0], tvec[0][0][2])
            target = (1,target_bearing,0,distance_to_target)
        elif ids[1] == 33:
            distance_to_target = math.sqrt(tvec[1][0][2] ** 2 + tvec[1][0][0] ** 2)
            target_bearing = math.atan2(tvec[1][0][0], tvec[1][0][2])
            target = (1, target_bearing, 0, distance_to_target)
        elif ids[0] in varots and ids[1] in varots:
            z3 = tvec[1][0][2]-tvec[0][0][2]
            x3 = tvec[1][0][0]-tvec[0][0][0]
            distance_to_target = math.sqrt(z3**2 + x3**2)
            target_bearing = math.atan2(x3,z3)
            angle_of_target = math.atan2(tvec[1][0][2]-tvec[0][0][2],tvec[1][0][0]-tvec[0][0][0])
            target = (0, target_bearing, angle_of_target, distance_to_target)
        else:
            return None
    else:
        if ids[0] == 33:
            distance_to_target = math.sqrt(tvec[1][0][2] ** 2 + tvec[1][0][0] ** 2)
            target_bearing = math.atan2(tvec[1][0][0], tvec[1][0][2])
            target = (1, target_bearing, 0, distance_to_target)
        else:
            return None
    return target

def imageProcessing (frame,markerSizeInCM):
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    cameraMatrix = numpy.array(
        [[1.40298102e+03, 0.00000000e+00, 9.40410469e+02], [0.00000000e+00, 1.39648065e+03, 5.12864174e+02],
         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    distCoeffs = numpy.array([[0.04419532, -0.11262258, -0.00592735, -0.00627272, 0.02306133]])
    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInCM, cameraMatrix, distCoeffs)
    if corners != ():
        return None
    else:
        return imageSecondProcessing(tvec,ids)