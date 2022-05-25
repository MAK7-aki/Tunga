import gi
import cv2

# import required library like Gstreamer and GstreamerRtspServer
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

# Sensor Factory class which inherits the GstRtspServer base class and add
# properties to it.
class SensorFactory(GstRtspServer.RTSPMediaFactory):

    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.cap =cv2.VideoCapture("rtsp://admin:tunga@2020@10.223.45.100")
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
            bbox = None
            tracker = cv2.TrackerMOSSE_create()
            if ret:
                # frame=self.cap.read()
                timer = cv2.getTickCount()
                # It is better to change the resolution of the camera 
                # instead of changing the image shape as it affects the image quality.
                frame = cv2.resize(frame, (640, 480), \
                    interpolation = cv2.INTER_LINEAR)

                fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
                cv2.putText(frame,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

                if bbox is not None :
                    ok,bbox=tracker.update(frame)
                    # if ok:
                    (x,y,w,h)=[int(v) for v in bbox]
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
                    # else:
                    #     bbox = None
                    #     cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                # cv2.imshow('Tracking',frame)
                # key = cv2.waitKey(1) & 0XFF
                    
                #if cv2.waitKey(1) & 0XFF == ord('a'):
                tracker = cv2.TrackerMOSSE_create()
                bbox = (270 ,190, 100 ,150)
                tracker.init(frame,bbox)

                # elif cv2.waitKey(1) & 0XFF == ord('w'):
                #     bbox = None

            #     elif key == ord("q"):
            #         break

            # cv2.destroyAllWindows()




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
        self.rtspServer.set_address("127.0.0.1")
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