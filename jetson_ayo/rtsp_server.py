import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class RTSPServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        self.factory = GstRtspServer.RTSPMediaFactory()
        self.factory.set_launch((
            "( nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! "
            "nvvidconv ! video/x-raw, format=I420 ! "
            "omxh264enc bitrate=8000000 ! video/x-h264, stream-format=byte-stream ! "
            "h264parse ! rtph264pay name=pay0 pt=96 )"
        ))
        self.factory.set_shared(True)
        self.server.get_mount_points().add_factory("/stream", self.factory)
        self.server.attach(None)

    def run(self):
        loop = GObject.MainLoop()
        loop.run()

if __name__ == '__main__':
    Gst.init(None)
    server = RTSPServer()
    server.run()

