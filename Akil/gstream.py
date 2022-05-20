from imutils.video import VideoStream
from collections import deque
import imutils
import cv2
import datetime
import numpy as np
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
    
class SensorFactory(GstRtspServer.RTSPMediaFactory):
    
    def __init__(self, **properties):
        pts = deque(maxlen=20)
        initBB = None
        tracker = cv2.TrackerMOSSE_create()
        vs = VideoStream(src="rtsp://admin:tunga@2020@10.223.45.100").start()
        while True:
            frame =  vs.read()
            if frame is None:
                break

            frame = imutils.resize(frame, height=480,width=640)
            (H, W) = frame.shape[:2]

            if  initBB is not None:
                (success, box) = tracker.update(frame)

                if success:
                    (x, y, w, h) = [int(v) for v in box]
                    bb_centroid = ((2*x+w)/2,(2*y+h)/2)
                    ey = (2*y+h)/2 - H/2
                    ex = (2*x+w)/2 - W/2
                    cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 255), 2)
                    a = (round(ex),round(ey),2000)
                    pts.append(bb_centroid)

                elif not success:
                    initBB = None
                    a = (320,240)

                for i in range(1, len( pts)):
                    if  pts[i - 1] is None or  pts[i] is None:
                        continue

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("a"):
                tracker = cv2.TrackerMOSSE_create()
                initBB = (W/2 - 50 ,H/2 - 50, 100 ,150)
                tracker.init(frame,  initBB)

            elif key == ord('w'):
                initBB = None
                
            elif key == ord("q"):
                vs.stop()
                break

            super(SensorFactory, self).__init__(**properties)
            self.cap = frame
            self.number_frames = 0
            self.fps = 30
            self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
            self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                                'caps=video/x-raw,format=BGR,width=640,height=480,framerate={}/1 ' \
                                '! videoconvert ! video/x-raw,format=I420 ' \
                                '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                                '! rtph264pay config-interval=1 name=pay0 pt=96'.format(self.fps)

    def on_need_data(self, src, lenght):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            cv2.imshow('frame',frame)
            if ret:
                data = frame.tostring()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                retval = src.emit('push-buffer', buf)
                print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                                                                                       self.duration,
                                                                                       self.duration / Gst.SECOND))
                if retval != Gst.FlowReturn.OK:
                    print(retval)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
       # super(GstServer, self).__init__(**properties)
        #self.factory = SensorFactory()
        #self.factory.set_shared(True)
        #self.get_mount_points().add_factory("/stream1", self.factory)
        #self.attach(None)

        self.rtspServer = GstRtspServer.RTSPServer()
        self.rtspServer.set_address("192.168.1.233")
        factory = SensorFactory()
        factory.set_shared(True)
        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory("/stream1", factory)
        self.rtspServer.attach(None)


GObject.threads_init()
Gst.init(None)

server = GstServer()

loop = GObject.MainLoop()
loop.run()

cv2.destroyAllWindows()

