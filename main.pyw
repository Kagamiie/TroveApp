from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtWidgets
import win32api, win32con, win32gui
from PyQt5 import QtWidgets , uic
import assets.config as cfg
import threading
import keyboard
import signal
import ctypes
import time
import sys
import os


troveHwnd = win32gui.FindWindow(0, "Trove")
whandle = troveHwnd
pid = win32api.GetCurrentProcessId()


def boxColl(x,y, sizex, sizey, posx, posy):
    if posx > x and posx < x + sizex:
        if posy > y and posy < y + sizey:
            return True
    return False

if not os.path.isfile("assets/settings.ini"):
    cfg.createConfig()
    
config = cfg.readConfig()

class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()

        self.window_handle = whandle

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


        uic.loadUi('main.ui', self)
        self.oldPos = None
        self.startPos = None
        self.resizeSize = 10
        self.grabSize = 30

        self.setGeometry(config["pos"][0],config["pos"][1],config["size"][0],config["size"][1])


        self.stop_event = threading.Event()
        self.worker_thread = None

        self.grabber = self.findChild(QtWidgets.QWidget, 'sidebar')

        self.closeBtn = self.findChild(QtWidgets.QPushButton, 'closeBtn')
        self.closeBtn.released.connect(self.Close)

        self.minBtn = self.findChild(QtWidgets.QPushButton, 'minimizeBtn')
        self.minBtn.released.connect(self.minimize)

        # views
        self.classView = self.findChild(QtWidgets.QWidget, 'ClassView')
        self.otherView = self.findChild(QtWidgets.QWidget, 'OtherView')
        self.classView.show()
        self.otherView.hide()

        # view button
        self.classBtn = self.findChild(QtWidgets.QPushButton, 'classChange')
        self.classBtn.released.connect(lambda: self.switchView(1))
        self.otherBtn = self.findChild(QtWidgets.QPushButton, 'otherBtn')
        self.otherBtn.released.connect(lambda: self.switchView(2))


# ------------------- Class View -----------------------------

        self.hidePlayer = self.findChild(QtWidgets.QCheckBox, 'hidePlayer')
        self.hidePlayer.released.connect(self.visibility)

        self.NoAfk = self.findChild(QtWidgets.QCheckBox, 'NoAfk')
        self.NoAfk.stateChanged.connect(self.afkbtn)

        self.whisper = self.findChild(QtWidgets.QCheckBox, 'whisper')
        self.whisper.stateChanged.connect(self.autoWhis)

        self.join = self.findChild(QtWidgets.QCheckBox, 'join')
        self.join.stateChanged.connect(self.autoJoin)

        self.hit = self.findChild(QtWidgets.QCheckBox, 'hit')
        self.hit.stateChanged.connect(self.autoHit)

        self.IceSage = self.findChild(QtWidgets.QPushButton, 'IceSageBtn')   
        self.IceSage.released.connect(lambda: self.switchClass(1, whandle))

        self.Solarion = self.findChild(QtWidgets.QPushButton, 'SolarionBtn')
        self.Solarion.released.connect(lambda: self.switchClass(2, whandle))

        self.ShadowHunter = self.findChild(QtWidgets.QPushButton, 'ShadowHunterBtn')
        self.ShadowHunter.released.connect(lambda: self.switchClass(3, whandle))


# ------------------- Other View -----------------------------

# Ya rien mdr
        self.distanceLabel = self.findChild(QtWidgets.QLabel, 'distanceLabel')
        self.distanceSlider = self.findChild(QtWidgets.QSlider, 'distanceSlider')
        self.distanceSlider.valueChanged.connect(self.cameraDistance)
        

        self.show()

# ------------------- Views functions ------------------------

    def switchView(self, arg):
        if arg == 1:
            self.classView.show()
            self.otherView.hide()
        elif arg == 2:
            self.classView.hide()
            self.otherView.show()

    def minimize(self):
        if self.isMinimized():
            self.showNormal()
        else:
            self.showMinimized()

# ------------------- Non-Ui functions -----------------------

    def action(self, first_click_x, first_click_y, key_press, second_click_coords, window_handle):
        screen_resolution = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        if screen_resolution == (2560, 1080):
            second_click_x, second_click_y = second_click_coords['2560x1080']
        elif screen_resolution == (1920, 1080):
            second_click_x, second_click_y = second_click_coords['1920x1080']
        else:
            print("Invalid screen resolution")
            return

        win32gui.SetActiveWindow(whandle)

        win32api.SetCursorPos((first_click_x, first_click_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, first_click_x, first_click_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, first_click_x, first_click_y, 0, 0)
        keyboard.press_and_release('j')

        time.sleep(0.5)

        win32api.SetCursorPos((second_click_x, second_click_y))
        win32api.mouse_event( win32con.MOUSEEVENTF_LEFTDOWN, second_click_x, second_click_y, 0, 0)
        win32api.mouse_event( win32con.MOUSEEVENTF_LEFTUP, second_click_x, second_click_y, 0, 0)
        time.sleep(1)


    def switchClass(self, arg, whandle):
        if arg == 1:
            self.action(1280, 540, 'j', {
            '2560x1080': (1337, 770), # .75 HUD
            '1920x1080': (1030, 795) # 1 HUD
            }, whandle)
            print("Ice Sage")

        elif arg == 2:
            self.action(1280, 540, 'j', {
            '2560x1080': (900, 450), # .75 HUD
            '1920x1080': (535, 435) # 1 HUD
            }, whandle)      
            print("Solarion")

        elif arg == 3:
            self.action(1280, 540, 'j', {
            '2560x1080': (1190, 765), # .75 HUD
            '1920x1080': (1035, 745) # 1 HUD
            }, whandle)
            print("Shadow Hunter") 



    def visibility(self):
        if self.hidePlayer.isChecked():
            wParam = [0x2F, 0x68, 0x69, 0x64, 0x65, 0x70, 0x6C, 0x61, 0x79, 0x65, 0x72]

            try:
                for i in range(len(wParam)):
                    win32api.PostMessage(whandle, win32con.WM_CHAR,  wParam[i], 0)
                win32api.PostMessage(whandle, win32con.WM_KEYDOWN,  0x0D, 0x1C0001)
                win32api.PostMessage(whandle, win32con.WM_KEYUP,  0x0D, 0x1C0001)
            except:
                exit(0)
        else:
            wParam = [0x2F, 0x73, 0x68, 0x6F, 0x77, 0x70, 0x6C, 0x61, 0x79, 0x65, 0x72]

            try:
                for i in range(len(wParam)):
                    win32api.PostMessage(troveHwnd, win32con.WM_CHAR,  wParam[i], 0)
                win32api.PostMessage(troveHwnd, win32con.WM_KEYDOWN,  0x0D, 0x1C0001)
                win32api.PostMessage(troveHwnd, win32con.WM_KEYUP,  0x0D, 0x1C0001)
            except:
                exit(0)



    def afkbtn(self, state):
        if state == QtCore.Qt.Checked:
            self.stop_event.clear()
            self.worker_thread = threading.Thread(target=self.anti_afk, args=(self.stop_event,))
            self.worker_thread.start()
        else:
            self.stop_event.set()

    def anti_afk(self, stop_event):
        count = 0
        while not stop_event.is_set():
            count += 1
            print("Saute ta mère x" + str(count))
            win32api.PostMessage(troveHwnd, win32con.WM_CHAR)
            win32api.PostMessage(troveHwnd, win32con.WM_KEYDOWN,  0x20, 0x390001)
            win32api.PostMessage(troveHwnd, win32con.WM_KEYUP,  0x20, 0x390001)
            time.sleep(2)



    def autoWhis(self, state):
        if state == QtCore.Qt.Checked:
            self.stop_event.clear()
            self.worker_thread = threading.Thread(target=self.whis, args=(self.stop_event,))
            self.worker_thread.start()
        else:
            self.stop_event.set()

    def whis(self, stop_event):
        count = 0
        while not stop_event.is_set():
            wParam = [0x0D,0x2F, 0x77, 0x20, 0x4b, 0x49, 0x52, 0x4b, 0x49, 0x52, 0x31, 0x35, 0x20, 0x6e, 0x69, 0x20, 0x71, 0x75, 0x65, 0x20, 0x74, 0x61, 0x20, 0x6d, 0x65, 0x72, 0x65, 0x0d]

            try:
                for i in range(len(wParam)):
                    win32api.PostMessage(troveHwnd, win32con.WM_CHAR,  wParam[i], 0)
                time.sleep(0.1)
                win32api.PostMessage(troveHwnd, win32con.WM_KEYDOWN,  0x0D, 0x1C0001)
                win32api.PostMessage(troveHwnd, win32con.WM_KEYUP,  0x0D, 0x1C0001)
            except:
                exit(0)
            count += 1
            print("Nique ta mère x" + str(count))
            time.sleep(3)
    


    def autoJoin(self, state):
        if state == QtCore.Qt.Checked:
            self.stop_event.clear()
            self.worker_thread = threading.Thread(target=self.aJoin, args=(self.stop_event,))
            self.worker_thread.start()
        else:
            self.stop_event.set()

    def aJoin(self, stop_event):
        count = 0
        while not stop_event.is_set():
            wParam = [0x2F, 0x6A, 0x6F, 0x69, 0x6E, 0x6D, 0x65, 0x20, 0x4B, 0x49, 0x52, 0x4B, 0x49, 0x52, 0x31, 0x35]

            try:
                for i in range(len(wParam)):
                    win32api.PostMessage(whandle, win32con.WM_CHAR,  wParam[i], 0)
                win32api.PostMessage(whandle, win32con.WM_KEYDOWN,  0x0D, 0x1C0001)
                win32api.PostMessage(whandle, win32con.WM_KEYUP,  0x0D, 0x1C0001)
            except:
                exit(0)
            count += 1
            print("Rejoin ta mère x" + str(count))
            time.sleep(32)



    def autoHit(self, state):
        if state == QtCore.Qt.Checked:
            self.stop_event.clear()
            self.worker_thread = threading.Thread(target=self.aHit, args=(self.stop_event,))
            self.worker_thread.start()
        else:
            self.stop_event.set()

    def aHit(self, stop_event):
        activated = False
        while not stop_event.is_set():
            win32gui.SendMessage(troveHwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        
            if not activated:  
                print("Activé")
                activated = True  
        else:
            win32gui.SendMessage(troveHwnd, win32con.WM_LBUTTONUP)
            print("Désactivé")








    def cameraDistance(self, e):
        self.distanceLabel.setText(f"Camera Distance: {e}")

# ------------------- Move / Resize --------------------------

    def mousePressEvent(self, event):
        if event.button() != 1:
            return

        # bottom right corner
        if boxColl(self.property("width") - self.resizeSize*2, self.property("height") - self.resizeSize*2, self.resizeSize*2, self.resizeSize*2, event.localPos().x(), event.localPos().y()):
            self.startPos = event.globalPos()
            self.startHeight = self.property("height")
            self.startWidth = self.property("width")
            self.resizeMode = "xy"
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)

        # right side
        elif boxColl(self.property("width") - self.resizeSize, 0, self.resizeSize, self.property("height"), event.localPos().x(), event.localPos().y()):
            self.startPos = event.globalPos()
            self.startWidth = self.property("width")
            self.resizeMode = "x"
            self.setCursor(Qt.CursorShape.SizeHorCursor)

        # bottom
        elif boxColl(0, self.property("height") - self.resizeSize, self.property("width"), self.resizeSize, event.localPos().x(), event.localPos().y()):
            self.startPos = event.globalPos()
            self.startHeight = self.property("height")
            self.resizeMode = "y"
            self.setCursor(Qt.CursorShape.SizeVerCursor)

        # grabber (side bar + 30px top)
        elif boxColl(self.grabber.property("x"), self.grabber.property("y"), self.grabber.property("width"), self.grabber.property("height"), event.localPos().x(), event.localPos().y()):
            self.oldPos = event.globalPos()
        elif boxColl(0, 0, self.property("width"), self.grabSize, event.localPos().x(), event.localPos().y()):
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.startPos = None
        self.oldPos = None
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEvent(self, event):

        # move window
        if self.oldPos:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

        # resize width
        elif self.startPos and self.resizeMode == "x":
            delta = QPoint(event.globalPos() - self.startPos)
            self.setGeometry(QRect(self.property("x"), self.property("y"), self.startWidth + delta.x(), self.property("height")))

        # resize height
        elif self.startPos and self.resizeMode == "y":
            delta = QPoint(event.globalPos() - self.startPos)
            self.setGeometry(QRect(self.property("x"), self.property("y"), self.property("width"), self.startHeight + delta.y()))

        # resize both
        elif self.startPos and self.resizeMode == "xy":
            delta = QPoint(event.globalPos() - self.startPos)
            self.setGeometry(QRect(self.property("x"), self.property("y"), self.startWidth + delta.x(), self.startHeight + delta.y()))

# ------------------- Close ----------------------------------

    def Close(self):
        cfg.writeConfig(f"{self.size().width()},{self.size().height()}", f"{self.pos().x()},{self.pos().y()}")
        os.kill(pid, signal.SIGTERM)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

main()