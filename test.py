from aruco import ArucoTracker
import cv2

marker_size = 0.5
markers = [i for i in range(100)]
tracker = ArucoTracker(cv2.aruco.DICT_4X4_100, marker_size, markers)
src = 0
# src = 'rtsp://admin:a123456789@192.168.13.165:554/Streaming/Channels/101?transportmode=unicast&profile=Profile_1'

capture = cv2.VideoCapture(src)

counter = 0

while True:
	ret, frame = capture.read()
	if ret == True:
		counter += 1

		if counter == 1:
			counter = 0
			result = tracker.processFrame(frame)

			print(result)
			
		scale_percent = 50  # percent of original size
		width = int(frame.shape[1] * scale_percent / 100)
		height = int(frame.shape[0] * scale_percent / 100)
		dim = (width, height)
		resized = cv2.resize(frame, dim)
		cv2.imshow('frame', resized)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break