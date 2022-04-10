"""

Crookes Radiometer for CircuitPython on CPB TFT Gizmo
Jean Paul Lorrain - 4/10/22
MIT License...

"""

import board
import time
import displayio
import vectorio
import analogio
import simpleio
from adafruit_gizmo import tft_gizmo

displayio.release_displays()  # does the gizmo initialization include a display release?

display = tft_gizmo.TFT_Gizmo()

main_group = displayio.Group()
display.show(main_group)

bg_pal = displayio.Palette(1)
bg_pal[0] = 0x99ffff  # light blue
bg_circle = vectorio.Circle(pixel_shader=bg_pal, radius=70, x=120, y=120)

stick_pal = displayio.Palette(1)
stick_pal[0] = 0xc0c0c0  # silver
center_stick = vectorio.Rectangle(pixel_shader=stick_pal, width=2, height=70, x=119, y=120)

base_pal = displayio.Palette(1)
base_pal[0] = 0x964b00  # brown
base_points = [(0, 0), (20, -40), (100, -40), (120, 0)]
base_poly = vectorio.Polygon(pixel_shader=base_pal, points=base_points, x=60, y=220)

black_pal = displayio.Palette(1)
black_pal[0] = 0x000000
black_points = [(-50, 0), (-25, 25), (0, 0), (-25, -25)]
black_vane = vectorio.Polygon(pixel_shader=black_pal, points=black_points, x=120, y=120)

white_pal = displayio.Palette(1)
white_pal[0] = 0xffffff
white_points = [(0, 0), (25, 25), (50, 0), (25, -25)]
white_vane = vectorio.Polygon(pixel_shader=white_pal, points=white_points, x=120, y=120)

main_group.append(bg_circle)
main_group.append(center_stick)
main_group.append(base_poly)
main_group.append(black_vane)
main_group.append(white_vane)

light_sensor = analogio.AnalogIn(board.LIGHT)

# mapping the light_sensor.value's low to the time value delay_high seems to work ok

# It took me a while to settle on a value for delay_high.  I still wanted
# to see the animation run at a reasonable speed in lower light levels, but
# the actual Crookes Radiometer on my windowsill only spins in direct sunlight.
# A lower value for delay_high increases animation speed in low light.

delay_low = (0.001)
delay_high = (0.5)

while True:

    for i in range(25, 0, -1):
        black_vane.points = [(-(2*i), 0), (-(i), 25), (0, 0), (-(i), -25)]
        white_vane.points = [(0, 0), ((i), 25), ((2*i), 0), ((i), -25)]
        # print(i)
        time.sleep(simpleio.map_range(light_sensor.value, 0, 62500, delay_high, delay_low))

    for i in range(0, 25, 1):
        black_vane.points = [(-(2*i), 0), (-(i), 25), (0, 0), (-(i), -25)]
        white_vane.points = [(0, 0), ((i), 25), ((2*i), 0), ((i), -25)]
        # print(i)
        time.sleep(simpleio.map_range(light_sensor.value, 0, 62500, delay_high, delay_low))