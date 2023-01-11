import os
import pickle

import cv2
import numpy as np

def intersection_list(list1, list2): 
   return set(list1).intersection(list2) 

def flatten(l):
    return [item for sublist in l for item in sublist]

class ArucoTracker:
	def __init__(self, aruco_dict, size, marker_numbers, file_matrix='./CameraCalibration.pckl') -> None:
		self.marker_length = size
		if not os.path.exists(file_matrix):
			print("You need to calibrate the camera you'll be using. See calibration project directory for details.")
		else:
			with open(file_matrix, 'rb') as f:
				(cameraMatrix, distCoeffs, _, _) = pickle.load(f)
				self.cameraMatrix = cameraMatrix
				self.distCoeffs = distCoeffs
				f.close()
				if self.cameraMatrix is None or self.distCoeffs is None:
					print(
						"Calibration issue. Remove {file_matrix} and recalibrate your camera with calibration_ChAruco.py.")

		# Constant parameters used in Aruco methods
		self.ARUCO_PARAMETERS = cv2.aruco.DetectorParameters_create()
		self.ARUCO_DICT = cv2.aruco.Dictionary_get(aruco_dict)
		self.marker_numbers = marker_numbers
	

	def processFrame(self, frame) -> float:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
		corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.ARUCO_DICT, parameters=self.ARUCO_PARAMETERS)
		frame = cv2.aruco.drawDetectedMarkers(frame, corners, borderColor=(0, 0, 255))

		result = []

		if ids is not None and len(ids) > 0:
			flatten_ids = flatten(ids)
			intersects = intersection_list(flatten_ids, self.marker_numbers)

			for id in intersects:
				index = np.where(ids == [id])
				if index[0] is not None:
					rvecs, tvecs, _objpoints = cv2.aruco.estimatePoseSingleMarkers(corners[int(index[0])], 
					self.marker_length, self.cameraMatrix, self.distCoeffs)
					
					result.append({
						"id": id,
						"tvecs": tvecs[0][0],
					})
				
		return sorted(result, key=lambda x: x['tvecs'][2])

				