import gi
import cv2
import sys
from pymavlink import mavutil


# import required library like Gstreamer and GstreamerRtspServer
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

# Sensor Factory class which inherits the GstRtspServer base class and add
# properties to it.
class SensorFactory(GstRtspServer.RTSPMediaFactory):

    def __init__(self, **properties):       
        super(SensorFactory, self).__init__(**properties)
        self.a=1 
        self.master = mavutil.mavlink_connection("/dev/ttyUSB0", baud=115200)       
        self.bbox=None
        self.nt=0
        self.tracker = cv2.legacy.TrackerMOSSE_create()
        self.cap = cv2.VideoCapture("rtsp://admin:tunga@2020@192.168.168.64")
        self.number_frames = 0
        self.fps = 30
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
                             .format(640, 480, self.fps)
    # method to capture the video feed from the camera and push it to the
    # streaming buffer.
    def on_need_data(self, src, length):
        if self.cap.isOpened():
            ret, frame = self.cap.read()            
            if ret:
                # It is better to change the resolution of the camera 
                # instead of changing the image shape as it affects the image quality.
                frame = cv2.resize(frame, (640, 480), \
                    interpolation = cv2.INTER_LINEAR)

                if self.number_frames == 3:
                    self.master.mav.command_long_send(self.master.target_system, self.master.target_component,
                                            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

                    msg = self.master.recv_match(type='COMMAND_ACK', blocking=True)
                    print(msg)

                if self.bbox is not None :
                    ok,self.bbox=self.tracker.update(frame)
                    if ok:
                        (x,y,w,h)=[int(v) for v in self.bbox]
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
                    else:
                        self.bbox = None
                        self.nt=self.nt+1
                        cv2.putText(frame,'Tracking Lost',(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                        if self.nt==1:
                            self.master.mav.command_long_send(self.master.target_system, self.master.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

                            msg2 = self.master.recv_match(type='COMMAND_ACK', blocking=True)
                            print(msg2)
                    
                if self.a==1:
                    self.bbox = (270 ,190, 100 ,150)
                    self.tracker.init(frame,self.bbox)
                    self.a=self.a+1

                # elif self.a>1 and self.bbox == None:
                #     self.a=1


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
                # if self.a>1 and bbox == None:
                #     self.a=1                                                                                                                                           
                if retval != Gst.FlowReturn.OK:
                    print(retval)
    # attach the launch string to the override method
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)
    
    # attaching the source element to the rtsp media
    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)

# Rtsp server implementation where we attach the factory sensor with the stream uri
class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        self.rtspServer = GstRtspServer.RTSPServer()
        self.rtspServer.set_address("192.168.168.2")
        factory = SensorFactory()
        factory.set_shared(True)
        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory("/video_stream", factory)
        self.rtspServer.attach(None)

# initializing the threads and running the stream on loop.
GObject.threads_init()
Gst.init(None)
server = GstServer()
loop = GObject.MainLoop()
loop.run()