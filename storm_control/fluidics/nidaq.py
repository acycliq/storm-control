from PyQt5.QtCore import QThread
import PyQt5.QtCore
from storm_control.sc_hardware.nationalInstruments import nicontrol


class TTL_Pulse(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.task = None

    def __del__(self):
        self.wait()

    def stop(self):
        self.terminate()

    def stop_task(self):
        self.task.stopTask()
        self.task.clearTask()
        # self.task = None

    def run(self):
        print('run was called')
        # your logic here
        while nicontrol.DigitalInput(source="Dev1/port0/line0"):
            self.task = nicontrol.DigitalInput(source="Dev1/port0/line0")
            while self.task.input():
                print('self.task is: ' + str(self.task.input()))
            else:
                print('Now is zero')
        else:
            print('Why am I here?')

        print('Checked')
