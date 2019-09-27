#!/usr/bin/python
# ----------------------------------------------------------------------------------------
# pumpControl: A wrapper class for the a generic pump
# ----------------------------------------------------------------------------------------
# Jeff Moffitt
# 2/15/14
# jeffmoffitt@gmail.com
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Import
# ----------------------------------------------------------------------------------------
import importlib
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets

# ----------------------------------------------------------------------------------------
# PumpControl Class Definition
# ----------------------------------------------------------------------------------------
class PumpControl(QtWidgets.QWidget):
    def __init__(self,
                 parameters = False,
                 parent = None):

        #Initialize parent class
        QtWidgets.QWidget.__init__(self, parent)

        # Define internal attributes
        self.com_port = parameters.get("pump_com_port")
        self.pump_ID = parameters.get("pump_id", 30)
        self.simulate = parameters.get("simulate_pump", True)
        self.verbose = parameters.get("verbose", True)
        self.status_repeat_time = 2000
        self.speed_units = "rpm"

        # Dynamic import of pump class
        pump_module = importlib.import_module(parameters.get("pump_class", "storm_control.fluidics.pumps.rainin_rp1"))

        # Create Instance of Pump
        self.pump = pump_module.APump(parameters = parameters)

        # Create GUI Elements
        self.createGUI()
        self.pollPumpStatus()
        
        # Define timer for periodic polling of pump status
        self.status_timer = QtCore.QTimer()        
        self.status_timer.setInterval(self.status_repeat_time)
        self.status_timer.timeout.connect(self.pollPumpStatus)
        self.status_timer.start()

    # ------------------------------------------------------------------------------------
    # Close class
    # ------------------------------------------------------------------------------------
    def close(self):
        if self.verbose: "Print closing pump"
        self.pump.close()

    # ------------------------------------------------------------------------------------
    # Coerce Speed Entry to Acceptable Range
    # ------------------------------------------------------------------------------------
    def coerceSpeed(self):
        current_speed_text = self.speed_control_entry_box.displayText()
        try:
            speed_value = float(current_speed_text)
            if speed_value < 0.01:
                self.speed_control_entry_box.setText("0.01")
            elif speed_value > 48.00:
                self.speed_control_entry_box.setText("48.00")
            else:
                self.speed_control_entry_box.setText("{0:.2f}".format(speed_value))
        except:
            self.speed_control_entry_box.setText("10.00")

    # ------------------------------------------------------------------------------------
    # Create GUI Elements
    # ------------------------------------------------------------------------------------ 
    def createGUI(self):
        # Define main widget
        self.mainWidget = QtWidgets.QGroupBox()
        self.mainWidget.setTitle("Pump Controls")
        self.mainWidgetLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        
        # Add individual widgets
        self.pump_identification_label = QtWidgets.QLabel()
        self.pump_identification_label.setText("No Pump Attached")

        self.flow_status_label= QtWidgets.QLabel()
        self.flow_status_label.setText("Flow Status:")
        self.flow_status_display = QtWidgets.QLabel()
        self.flow_status_display.setText("Unknown")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.flow_status_display.setFont(font)

        self.speed_label = QtWidgets.QLabel()
        self.speed_label.setText("Flow Rate:")
        self.speed_display = QtWidgets.QLabel()
        self.speed_display.setText("Unknown")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.speed_display.setFont(font)

        self.speed_control_label = QtWidgets.QLabel()
        self.speed_control_label.setText("Desired Speed")
        self.speed_control_entry_box = QtWidgets.QLineEdit()
        self.speed_control_entry_box.setText("10.00")
        self.speed_control_entry_box.editingFinished.connect(self.coerceSpeed)
               
        self.direction_control_label = QtWidgets.QLabel()
        self.direction_control_label.setText("Desired Direction")
        self.direction_control = QtWidgets.QComboBox()
        self.direction_control.addItem("Forward")
        self.direction_control.addItem("Reverse")

        self.start_flow_button = QtWidgets.QPushButton()
        self.start_flow_button.setText("Start Flow")
        self.start_flow_button.clicked.connect(self.handleStartFlow)

        self.stop_flow_button = QtWidgets.QPushButton()
        self.stop_flow_button.setText("Stop Flow")
        self.stop_flow_button.clicked.connect(self.handleStopFlow)
        
        self.mainWidgetLayout.addWidget(self.flow_status_display)
        self.mainWidgetLayout.addWidget(self.speed_display)
        self.mainWidgetLayout.addWidget(self.speed_control_label)
        self.mainWidgetLayout.addWidget(self.speed_control_entry_box)
        self.mainWidgetLayout.addWidget(self.direction_control_label)
        self.mainWidgetLayout.addWidget(self.direction_control)
        self.mainWidgetLayout.addWidget(self.start_flow_button)
        self.mainWidgetLayout.addWidget(self.stop_flow_button)
        self.mainWidgetLayout.addStretch(1)

    # ----------------------------------------------------------------------------------------
    # Display Status
    # ----------------------------------------------------------------------------------------
    def updateStatus(self, status):
        # Pump identification
        self.pump_identification_label.setText(self.pump.identification)
        
        # Flow status
        if status[0] == "Flowing":
            self.flow_status_display.setText(status[2])
            self.flow_status_display.setStyleSheet("QLabel { color: green}")
            self.stop_flow_button.setEnabled(True)
            self.start_flow_button.setText("Change Flow")
        elif status[0] == "Stopped":
            self.flow_status_display.setText(status[0])
            self.flow_status_display.setStyleSheet("QLabel { color: red}")
            self.stop_flow_button.setEnabled(False)
            self.start_flow_button.setText("Start Flow")
        else: # Unknown status
            self.flow_status_display.setText(status[0])
            self.flow_status_display.setStyleSheet("QLabel { color: red}")
            self.stop_flow_button.setEnabled(False)
            self.start_flow_button.setEnabled(False)

        # Speed
        self.speed_display.setText("%0.2f" % status[1] + " " + self.speed_units)
            
    # ----------------------------------------------------------------------------------------
    # Poll Pump Status
    # ----------------------------------------------------------------------------------------
    def pollPumpStatus(self):
        self.updateStatus(self.pump.getStatus())

    # ----------------------------------------------------------------------------------------
    # Handle Change Flow Request
    # ----------------------------------------------------------------------------------------
    def handleStartFlow(self):
        self.pump.startFlow(float(self.speed_control_entry_box.displayText()),
                            direction = self.direction_control.currentText())
        time.sleep(0.1)
        self.pollPumpStatus()
        
    # ----------------------------------------------------------------------------------------
    # Handle Change Flow Request
    # ----------------------------------------------------------------------------------------
    def handleStopFlow(self):
        self.pump.stopFlow()
        time.sleep(0.1)
        self.pollPumpStatus()

    # ------------------------------------------------------------------------------------
    # Change pump based on sent command: [direction, speed]
    # ------------------------------------------------------------------------------------          
    def receiveCommand(self, command):
        speed = command[1]
        direction = command[0]
        if speed < 0.01:
            self.pump.stopFlow()
        else:
            self.pump.startFlow(speed, direction)

    # ------------------------------------------------------------------------------------
    # Determine Enabled State
    # ------------------------------------------------------------------------------------          
    def setEnabled(self, enabled):
        # This control is always enabled to allow emergency control over the flow
        pass

# ----------------------------------------------------------------------------------------
# Stand Alone Test Class
# ----------------------------------------------------------------------------------------
class StandAlone(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(StandAlone, self).__init__(parent)

        # scroll area widget contents - layout
        self.pump = PumpControl(com_port = 4,
                                pump_ID = 30,
                                simulate = False,
                                verbose = False)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.mainLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.mainLayout.addWidget(self.pump.mainWidget)
        
        # set central widget
        self.setCentralWidget(self.centralWidget)

        # set window title
        self.setWindowTitle("Pump Control")

        # set window geometry
        self.setGeometry(50, 50, 500, 300)

        # Create file menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.closeEvent)

        file_menu.addAction(exit_action)

    # ------------------------------------------------------------------------------------
    # Detect close event
    # ------------------------------------------------------------------------------------    
    def closeEvent(self, event):
        self.pump.close()
        self.close()

# ----------------------------------------------------------------------------------------
# Test/Demo of Classs
# ----------------------------------------------------------------------------------------        
if (__name__ == "__main__"):
    app = QtWidgets.QApplication(sys.argv)
    window = StandAlone()
    window.show()
    app.exec_()
