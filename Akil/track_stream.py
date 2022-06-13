import cv2
import gi
from collections import deque
import datetime
import numpy as np
import imutils
import serial

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0') 
from gi.repository import Gst, GstRtspServer, GObject

class SensorFactory(GstRtspServer.RTSPMediaFactory):
	def __init__(self, **properties):
		super(SensorFactory, self).__init__(**properties) 
		self.cap = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")
		#self.cap = cv2.VideoCapture("rtsp://192.168.43.1:8554/fpv_stream")
		#vid = day_stream()
		#self.cap = vid.image()
		self.number_frames = 0 
		self.fps = 30
		self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds 
		self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME caps=video/x-raw,format=BGR,width=640,height=480,framerate={}/1  ! videoconvert ! video/x-raw,format=I420 ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay config-interval=1 name=pay0 pt=96 rtspsrc host=127.0.0.1 port=8554'.format(self.fps)

	def on_need_data(self, src, lenght):

		if self.cap.isOpened():
			ret, frame = self.cap.read()
			#cv2.imshow('frame',frame)
			if ret:

				pts = deque(maxlen=40)
				center = None
				initBB = None
				dat = datetime.datetime.now()
				prev = None

				kf = cv2.KalmanFilter(4,2)
				kf.measurementMatrix = np.array([[1, 0, 0, 0],[0, 1, 0, 0]], np.float32)
				kftransitionMatrix = np.array([[1, 0, 1, 0],[0, 1, 0, 1],[0, 0, 1, 0],[0, 0, 0, 1]], np.float32)

				#vs = VideoStream(src="rtsp://192.168.43.1:8554/fpv_stream").start()
				#vs = VideoStream(src=0).start()
				tracker = cv2.legacy.TrackerMOSSE_create()
				bbox = []

				# try:
				# 	ser = serial.Serial('COM4',19200,timeout=0)
				# except:
				# 	ser = serial.Serial('COM4',19200,timeout=0)
				# red = ser.read()
				red="a"

				frame = imutils.resize(frame, height=480,width=640)
				(H, W) = frame.shape[:2]
				centroid = (W/2,H/2)
				#cv2.drawMarker(frame, centroid, (0,255,255),0,30,thickness=2)
				if initBB is not None:
					(success, box) = tracker.update(frame)
					if success:
					
						(x, y, w, h) = [int(v) for v in box]
						bb_centroid = ((2*x+w)/2,(2*y+h)/2)
						ey = (2*y+h)/2
						ex = (2*x+w)/2
						prev_x = ex
						prev_y = ey
						if prev_x==0 and prev_y==0:

							erx = prev_x - (W/2)
							ery = prev_y - (H/2)

						erx = prev_x - (W/2)
						ery = prev_y - (H/2)
						kf.correct(np.array((bb_centroid),np.float32))
						retval = kf.predict() 
						prev = retval
						cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 255), 2)
						#cv2.rectangle(frame, (int(x2[0][0]), int(y2[0][0])), (int(x2[0][0]) + w, int(y1[0][0]) + h),(0, 255, 255), 2)
						a = (erx,ery)
						pts.append(bb_centroid)
						# ser.write(str(a))
					elif not success:
						tracker = cv2.legacy.TrackerMOSSE_create()			
						initBB = (prev[0][0]-50,prev[1][0]-50,100,100)
						tracker.init(frame, initBB)
						a = (320,240)
						# ser.write(str(a))	
					for i in range(1, len(pts)):
						if pts[i - 1] is None or pts[i] is None:
							continue
						
						cv2.line(frame, pts[i - 1], pts[i], (255, 255,255), 2)
				#cv2.imshow("Frame", frame)
				key = cv2.waitKey(1) & 0xFF
				bbox = frame
				# cf		or tracking, a for photo, b for pilot window (serial read)

				if red == "a":
					cv2.imwrite('Image_Day '+str(dat.strftime("%d/%m/%Y %H:%M:%S"))+'.jpg',frame)

				elif red == "c":
				
					if initBB is not None:
					
						initBB = None
						# ser.write('e')

					else:
					
						tracker = cv2.legacy.TrackerMOSSE_create()		
						initBB = (W/2 - 100 ,H/2 - 100, 150 ,150)
						tracker.init(frame,  initBB)	
						# ser.write('f')
				
								#self.vs.release()
				#
				#ob 	= day_stream()


				data = frame.tostring() 
				# print(data)
				buf = Gst.Buffer.new_allocate(None, len(data), None)
				buf.fill(0, data)
				buf.duration = self.duration
				timestamp = self.number_frames * self.duration
				buf.pts = buf.dts = int(timestamp)
				buf.offset = timestamp
				#self.number_frames += 1
				retval = src.emit('push-buffer', buf) 
				print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames, self.duration, self.duration / Gst.SECOND)) 

			#if retval != Gst.FlowReturn.OK: 
			#	print(retval) 
			cv2.destroyAllWindows()
	def do_create_element(self, url): 
		return Gst.parse_launch(self.launch_string) 

	def do_configure(self, rtsp_media): 
		self.number_frames = 0 
		appsrc = rtsp_media.get_element().get_child_by_name('source') 
		appsrc.connect('need-data', self.on_need_data) 


class GstServer(GstRtspServer.RTSPServer): 
	def __init__(self, **properties): 
		super(GstServer, self).__init__(**properties) 
		self.factory = SensorFactory()
		self.set_address('192.168.168.2')
		self.factory.set_shared(True)
		#self.auth = GstRtspServer.RTSPAuth()
		#self.auth.add_basic(GstRtspServer.RTSPAuth.make_basic('user','user'),GstRtspServer.RTSPToken())
		self.get_mount_points().add_factory("/video_stream", self.factory) 
		self.attach(None) 

		#self.rtspServer = GstRtspServer.RTSPServer()
		#self.rtspServer.set_address('127.0.0.1')
		#self.factory = SensorFactory()
		#self.factory.set_shared(True)
		#mountPoints = self.rtspServer.get_mount_points()
		#mountPoints.add_factory("/stream1", self.factory)
		#self.attach(None)


GObject.threads_init() 
Gst.init(None) 

server = GstServer() 

loop = GObject.MainLoop() 
loop.run()
