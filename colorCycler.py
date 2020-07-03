"""Color Cycler for TP-Link LB130 bulb using the library available on:
        https://github.com/briandorey/tp-link-LB130-Smart-Wi-Fi-Bulb
    
Implemented:
- Color cycling which is almost perfectly non-stuttery, error free (from failed transmissions) 

TODO:
- Random Color changer
- check for on/off state, put in on state and then start the color cycling
- play with light.transition, range() and step in range to see how fast/smoothly color changing occurs
- Auto on/off detection
- Add code for retrying rather than try/except
- Auto detect current color
"""


from tplight import LB130
import time

# some constants
YOUR_IP = "192.168.68.110"  # change this
BRIGHTNESS = 30  # an int as a percentage
STEP = 10
TRANSITION_PERIOD = 600  # in ms

# Time taken to cycle through all colors = (360/STEP)*(TRANSITION_PERIOD+100ms)
"""
NOTE #1: STEP value must be low enough for trasnition_period to function properly (without colors going out of the cycle) but not too low, as it would result in
too many transmissions, and hence many failed transmission. This could cause network clogging or erratic color cycling
NOTE #2: TRANSITION_PERIOD must be chosen in accordance with step value. This makes sure colors cycle decently fast but not too fast"
"""


def colorCycler(light):
    """
    Takes a light object and cycles color
    :param light: Light object from tplight library
    :param brightness: Brightness of bulb to set
    """
    hue = light.hue

    while hue <= 360:
        try:  # try/except needed here incase transmission fails
            light.hue = hue  # start from currently set color
            hue += STEP
            if hue > 360:
                hue = 0
        except:
            continue

        time.sleep(
            (TRANSITION_PERIOD + 100) / 1000
        )  # adding 100ms to give enough time for transition completion.


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

    print("Now cycling")

    while True:
        colorCycler(light)
