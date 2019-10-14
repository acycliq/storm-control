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
    onReceiveTTL = pyqtSignal(int)

    def __init__(self, obj):
        QThread.__init__(self)
        # self.stopped = event
        self.gui = obj
        self.alive = True
        self.port_reading = False
        self.emit_counter = 0
        self.source = self.gui.nidaq_checkbox.line_in

    def run(self):
        while self.alive:
            # ok, that works but it is a bit too naive. The proper way is to do a callback on rising edge maybe?
            if nidaq.readDigitalLine(source = self.source):
                # self.alive = False
                # print('reading input at %s, value is True' % self.source)
                self.gui.nidaq_checkbox.setText('NI-DAQ 6008 connection established. Line in: %s. Line out: %s' % (self.source, self.gui.nidaq_checkbox.line_out) )
                # If the previous reading is False and now is True then run a Kilroy protocol
                if not self.port_reading:
                    print('chatting to Kilroy')
                    sleep(3)
                    # emit an "onReceiveTTL" signal passing-in the appropriate int parameter, emit_counter
                    self.onReceiveTTL.emit(self.emit_counter)
                    self.port_reading = True
                    self.emit_counter = self.emit_counter + 1
            else:
                self.port_reading = False
                self.gui.nidaq_checkbox.setText('NI-DAQ 6008 connection established. Line in: %s. Line out: %s' % (self.source, self.gui.nidaq_checkbox.line_out) )
                # print('%s: reading input at %s, value is False' % (datetime.datetime.now(), self.source))

        else:
            print('%s: NI-DAQ 6008 connection paused' % (datetime.datetime.now()))
            self.gui.nidaq_checkbox.setText('NI-DAQ 6008 connection paused')

