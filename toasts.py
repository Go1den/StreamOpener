import platform

from win10toast import ToastNotifier

from constants.messageConstants import MessageConstants
from sanitize import sanitize

def toast(previouslyLiveStreams, refreshedLiveStreams):
    if platform.release() == "10":
        previouslyLiveStreamNames = [stream.stylizedStreamName for stream in previouslyLiveStreams]
        streamsToToast = [stream for stream in refreshedLiveStreams if stream.stylizedStreamName not in previouslyLiveStreamNames]
        for stream in streamsToToast:
            toaster = ToastNotifier()
            toaster.show_toast(MessageConstants.TOAST.format(stream.stylizedStreamName), sanitize(stream.streamTitle), threaded=False, icon_path='streamopenericon.ico', duration=8)
