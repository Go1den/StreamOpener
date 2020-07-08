import platform
from win10toast import ToastNotifier

def toast():
    if platform.release() == "10":
        print("yay")
    toaster = ToastNotifier()
    toaster.show_toast("New live streams!", "andy, cleartonic, and IvanGPX", threaded=True, icon_path='streamopenericon.ico', duration=8)

toast()