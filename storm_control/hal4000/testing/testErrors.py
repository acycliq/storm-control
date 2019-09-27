#!/usr/bin/env python
"""
These are for testing HAL's handling of errors.

Hazen 03/18
"""
import time

import storm_control.hal4000.halLib.halMessage as halMessage
import storm_control.hal4000.halLib.halModule as halModule


class TestSimpleError(halModule.HalModule):

    def __init__(self, module_params = None, qt_settings = None, **kwds):
        super().__init__(**kwds)
        
    def processMessage(self, message):
        if message.isType("start"):
            raise halMessage.HalMessageException("Failed!")

        
class TestWorkerError(halModule.HalModule):

    def __init__(self, module_params = None, qt_settings = None, **kwds):
        super().__init__(**kwds)
        
    def processMessage(self, message):
        if message.isType("start"):
            halModule.runWorkerTask(self, message, self.throwError)

    def throwError(self):
        raise halMessage.HalMessageException("Failed!")


# FIXME: We need an actual test for this. I tried but could not figure
#        out how to do this with qtbot.
#
class TestWorkerTimeout(halModule.HalModule):

    def __init__(self, module_params = None, qt_settings = None, **kwds):
        super().__init__(**kwds)

    def infiniteLoop(self):
        while True:
            time.sleep(1)

    def processMessage(self, message):
        if message.isType("start"):
            halModule.runWorkerTask(self, message, self.infiniteLoop, job_time_ms = 100)
