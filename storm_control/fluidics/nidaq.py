from PyQt5.QtCore import QThread
import storm_control.sc_hardware.nationalInstruments.nicontrol as nidaq


class TTL_Pulse(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.alive = True

    def __del__(self):
        self.wait()

    def run(self):
        while self.alive:
            # x = nidaq.readDigitalLine(source = "Dev1/port0/line0")
            if nidaq.readDigitalLine(source = "Dev1/port0/line0"):
                print('ok')
            else:
                # self.alive = False
                print('now is false')

        # your logic here

        # def run(self):
        #     while True:
        #         x = nidaq.readDigitalLine(source="Dev1/port0/line0")
        #         if x:
        #             print('ok')
        #         else:
        #             print('now is false')