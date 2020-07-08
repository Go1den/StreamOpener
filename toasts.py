import platform
from win10toast import ToastNotifier

def toast():
    if platform.release() == "10":
        toaster = ToastNotifier()
        toaster.show_toast("New live streams!", "andy, cleartonic, and IvanGPX", threaded=True, icon_path='streamopenericon.ico', duration=8)
