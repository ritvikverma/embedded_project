from sense_hat import SenseHat
import time

# initializing the sense_hat object to 's'
s = SenseHat()
s.low_light = True

# setting the color codes for the colors that are used in this program
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
magenta = (255, 0, 144)
nothing = (0, 0, 0)


# defining a function to display "OK" on the LED matrix
def ohkay():
    G = green
    O = nothing
    logo = [
        O, O, O, O, O, O, O, O,
        O, G, G, O, O, G, O, G,
        G, O, O, G, O, G, G, O,
        G, O, O, G, O, G, O, O,
        G, O, O, G, O, G, O, O,
        G, O, O, G, O, G, G, O,
        O, G, G, O, O, G, O, G,
        O, O, O, O, O, O, O, O,
    ]
    return logo


# defining a function to display "X" on the LED matrix
def ehks():
    R = red
    O = nothing
    logo = [
        R, R, O, O, O, O, O, R,
        O, R, R, O, O, O, R, R,
        O, O, R, R, O, R, R, O,
        O, O, O, R, R, R, O, O,
        O, O, O, R, R, R, O, O,
        O, O, R, R, O, R, R, O,
        O, R, R, O, O, O, R, R,
        R, R, O, O, O, O, O, R,
    ]
    return logo


# defining a function to display the live reading of the temperature
def temp():
    temp = s.temp
    logo = [red if i < temp else blue for i in range(64)]
    # setting threshholds for the temperature
    if temp >= 32:
        nextlogo = ehks()
    else:
        nextlogo = ohkay()
    # returns logo(Tempretrure display) and nextlogo("OK" or "X")
    return logo, nextlogo


# defining a function to display the live reading of the humidity
def humidity_display():
    humidity = s.humidity
    humidity_value = 64 * humidity / 100
    logo = [green if i < humidity_value else magenta for i in range(64)]
    # setting threshholds for the humidity
    if humidity >= 85:
        nextlogo = ehks()
    else:
        nextlogo = ohkay()
    # returns logo(Tempretrure display) and nextlogo("OK" or "X")
    return logo, nextlogo


# entering the main loop
while True:
    # display the live(dynamic) temperature for 10 seconds
    start = time.time()
    while (time.time() - start) < 10:
        curr_logo, next_logo = temp()
        s.set_pixels(curr_logo)

    # at the end of the 10 seconds display "OK" or "X" depending on the reading
    s.set_pixels(next_logo)
    time.sleep(10)  # hold this display for 10 seconds and then move onto show the humidity

    # display the live(dynamic) humidity for 10 seconds
    start = time.time()
    while (time.time() - start) < 10:
        curr_logo, next_logo = humidity_display()
        s.set_pixels(curr_logo)

    # at the end of the 10 seconds display "OK" or "X" depending on the reading
    s.set_pixels(next_logo)
    time.sleep(10)  # hold this display for 10 seconds and then move onto show the humidity
