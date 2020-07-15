from threading import Event, Thread, Timer
from tplight import LB130

# some constants
YOUR_IP = "192.168.68.108"  # change this
BRIGHTNESS = 1  # an int as a percentage
STEP = 10
TRANSITION_PERIOD = 600  # in ms
hue = 1

"""
NOTE #1: STEP value must be low enough for trasnition_period to function properly (without colors going out of the cycle) but not too low, as it would result in
too many transmissions, and hence many failed transmission. This could cause network clogging or erratic color cycling
NOTE #2: TRANSITION_PERIOD must be chosen in accordance with step value. This makes sure colors cycle decently fast but not too fast"
"""


class SimpleTimer:
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


def runCycler():
    global hue
    try:
        light.hue = hue
        hue += STEP
        if hue > 360:
            hue = 1
    except:
        pass


try:
    light = LB130(YOUR_IP)
    light.brightness = BRIGHTNESS
    light.saturation = 100
    light.transition_period = TRANSITION_PERIOD
except:
    print("Something went wrong")
else:
    if not light.isOn():  # Turn on the light if it isnt on
        light.on()


sleepTime = (TRANSITION_PERIOD + 100) / 1000
cycler = SimpleTimer(sleepTime, runCycler)
cycler.start()
