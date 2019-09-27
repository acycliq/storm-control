#!/usr/bin/python
#
# Handles the plotting window
#
# Hazen 02/13
#

from PyQt5 import QtCore, QtGui
import pyqtgraph

import numpy

pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'k')

def saveData(filename, x, y, z):
    numpy.savetxt(filename, numpy.concatenate((x[:,None], y[:,None], z[:,None]), axis = 1))

class PlotWindow(pyqtgraph.PlotWidget):

    def __init__(self, x_label, x_range, y_label, y_range, qt_parent):
        pyqtgraph.PlotWidget.__init__(self)

        self.viewbox = self.getPlotItem().getViewBox()
        self.viewbox.disableAutoRange()
        self.viewbox.setMouseEnabled(x = False, y = False)
        self.viewbox.setRange(xRange = (x_range[0], x_range[1]),
                              yRange = (y_range[0], y_range[1]))

        self.setLabel('left', y_label)
        self.setLabel('bottom', x_label)

        self.static_text = False

    def paintEvent(self, event):
        pyqtgraph.PlotWidget.paintEvent(self, event)
        
        if self.static_text:
            painter = QtGui.QPainter(self.viewport())
            painter.drawStaticText(70, 10, self.static_text)

    def plotBinnedData(self, b_sz, b_wx, b_wy):
        a_pen = pyqtgraph.mkPen(0,0,0)
        a_pen.setWidth(1)
        a_brush = pyqtgraph.mkBrush(255,255,255)
        self.plot(b_sz, b_wx, 
                  pen = None,
                  symbol = 'o',
                  symbolPen = a_pen,
                  symbolBrush = a_brush,
                  symbolSize = 12)

        self.plot(b_sz, b_wy,
                  pen = None,
                  symbol = 'o',
                  symbolPen = a_pen,
                  symbolBrush = a_brush,
                  symbolSize = 12)
        saveData("binned.txt", b_sz, b_wx, b_wy)

    def plotData(self, sz, wx, wy):
        self.plot(sz, wx, 
                  pen = None,
                  symbol = 'o',
                  symbolPen = pyqtgraph.mkPen(255,0,0),
                  symbolBrush = pyqtgraph.mkBrush(0,0,255),
                  symbolSize = 6)

        self.plot(sz, wy, 
                  pen = None,
                  symbol = 'o',
                  symbolPen = pyqtgraph.mkPen(0,255,0),
                  symbolBrush = pyqtgraph.mkBrush(0,0,255),
                  symbolSize = 6)

    def plotFit(self, sz, xfit, yfit):
        a_pen = pyqtgraph.mkPen(0,0,0)
        self.plot(sz, xfit, pen = a_pen)
        self.plot(sz, yfit, pen = a_pen)
        saveData("fit.txt", sz, xfit, yfit)

    def plotStageQPD(self, stage, qpd, slope, offset):
        qpd_min = numpy.min(qpd)
        qpd_max = numpy.max(qpd)
        self.viewbox.setRange(yRange = (1.1*qpd_min, 1.1*qpd_max))
        self.plot(stage, qpd,
                  pen = None,
                  symbol = 'o',
                  symbolPen = pyqtgraph.mkPen(0,0,0),
                  symbolBrush = pyqtgraph.mkBrush(255,255,255),
                  symbolSize = 6)

        x_vals = numpy.array([-1.0, 1.0])
        y_vals = (x_vals - offset)/slope
        self.plot(x_vals, y_vals, pen = pyqtgraph.mkPen(0,0,0))

        self.static_text = QtGui.QStaticText("slope = {0:.3f} au/um".format(-1.0/slope))

    def plotWxWyData(self, wx, wy, cat):
        self.plot(wx, wy,
                  pen = None,
                  symbol = 'o',
                  symbolPen = pyqtgraph.mkPen(255,0,0),
                  symbolBrush = pyqtgraph.mkBrush(0,0,255),
                  symbolSize = 6)

    def plotWxWyFit(self, wxfit, wyfit):
        a_pen = pyqtgraph.mkPen(0,0,0)
        self.plot(wxfit, wyfit, pen = a_pen)


class SquarePlotWindow(PlotWindow):

    def __init__(self, x_label, x_range, y_label, y_range, parent):
        PlotWindow.__init__(self, x_label, x_range, y_label, y_range, parent)

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        #policy = QtGui.QSizePolicy()
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

    def heightForWidth(self, w):
        #print "hFW:", w
        return w

#
# The MIT License
#
# Copyright (c) 2013 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


