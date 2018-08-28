from cefpython3 import cefpython as cef
import platform
import sys
import json


def run_cef_gui(url_target, title):
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url=url_target,
                          window_title=title)
    cef.MessageLoop()
    cef.Shutdown()


def check_versions():
    print("[cef_gui.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[cef_gui.py] Python {ver} {arch}".format(
          ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_cef_gui("localhost:5000/" + sys.argv[1], "GAOnline")
    else:
        run_cef_gui("localhost:5000/" , "GAOnline")