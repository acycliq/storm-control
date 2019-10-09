from PyQt5.QtCore import QThread, pyqtSignal
import storm_control.sc_hardware.nationalInstruments.nicontrol as nidaq
from time import sleep


class TTL_Pulse(QThread):

    def __init__(self, kilroyProtocols):
        QThread.__init__(self)
        self.kilroyProtocols = kilroyProtocols
        self.alive = True
        self.current_port_reading = None

    def __del__(self):
        self.wait()

    def run(self):
        while self.alive:
            # x = nidaq.readDigitalLine(source = "Dev1/port0/line0")
            if nidaq.readDigitalLine(source = "Dev1/port0/line0"):
                self.current_port_reading = True
                print('ok')
            else:
                # self.alive = False
                print('now is false')
                # If the previous reading is True and now is False run a Kilroy protocol
                if self.current_port_reading:
                    print('chat to Kilroy')
                    self.kilroyProtocols.startProtocolLocally()
                    sleep(1)
                    print('one...')
                    sleep(1)
                    print('two...')
                    sleep(1)
                    print('three...')
                    sleep(1)
                    self.current_port_reading = False



class TTL_Thread(QThread):
    update_me = pyqtSignal()

    def __init__(self, event=None):
        QThread.__init__(self)
        self.stopped = event
        self.alive = True
        self.current_port_reading = None

    def run(self):
        while self.alive:
            if nidaq.readDigitalLine(source = "Dev1/port0/line0"):
                self.current_port_reading = True
                print('ok')
            else:
                # self.alive = False
                print('now is false')
                # If the previous reading is True and now is False run a Kilroy protocol
                if self.current_port_reading:
                    print('chat to Kilroy')
                    sleep(3)
                    self.update_me.emit()
                    self.current_port_reading = False

