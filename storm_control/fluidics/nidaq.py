from PyQt5.QtCore import QThread, pyqtSignal
import PyQt5.QtGui as QtGui
import storm_control.sc_hardware.nationalInstruments.nicontrol as nidaq
from time import sleep
import datetime


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
    # Define a signal called 'update_me' that takes an argument of type int.
    update_me = pyqtSignal(int)

    def __init__(self, obj):
        QThread.__init__(self)
        # self.stopped = event
        self.gui = obj
        self.alive = True
        self.port_reading = None
        self.emit_counter = 0
        self.source = 'Dev1/port0/line0'

    def run(self):
        while self.alive:
            if nidaq.readDigitalLine(source = self.source):
                self.port_reading = True
                self.gui.nidaq_checkbox.setText('NI-DAQ 6008 connection established to %s' % self.source)
                print('%s: reading input at %s, value is True' % (datetime.datetime.now(), self.source))
            else:
                # self.alive = False
                print('reading input at %s, value is False' % self.source)
                self.gui.nidaq_checkbox.setText('NI-DAQ 6008 connection established to %s' % self.source)
                # If the previous reading is True and now is False run a Kilroy protocol
                if self.port_reading:
                    print('chatting to Kilroy')
                    sleep(3)
                    # emit an "update_me" signal passing-in the appropriate int parameter, emit_counter
                    self.update_me.emit(self.emit_counter)
                    self.port_reading = False
                    self.emit_counter = self.emit_counter + 1
        else:
            print('%s: NI-DAQ 6008 connection paused' % (datetime.datetime.now()))
            self.gui.nidaq_checkbox.setText('NI-DAQ 6008 connection paused')

