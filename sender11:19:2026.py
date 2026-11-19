
from microbit import *
import radio

# Radio setup
radio.config(group=88)
radio.on()

display.show("S")

# Joystick connections (verify for your board)
JOYSTICK_X = pin1
JOYSTICK_Y = pin2

# Joystick buttons
BUTTON_7 = pin12
BUTTON_8 = pin14
BUTTON_9 = pin15
BUTTON_10 = pin13

# Track previous button states
last_buttons = [1, 1, 1, 1]


def send_command(number):
    radio.send(str(number))


while True:
    # Read the joystick
    x = JOYSTICK_X.read_analog()
    y = JOYSTICK_Y.read_analog()

    # Preserve the original movement conditions
    if y > 540:
        send_command(1)

    elif y < 500:
        send_command(2)

    elif x < 520:
        send_command(5)

    elif x > 530:
        send_command(4)

    else:
        send_command(6)

    # Read buttons (assumes active-low buttons)
    buttons = [
        BUTTON_7.read_digital(),
        BUTTON_8.read_digital(),
        BUTTON_9.read_digital(),
        BUTTON_10.read_digital()
    ]

    commands = [7, 8, 9, 10]

    for i in range(4):
        # Send only when the button is first pressed
        if buttons[i] == 0 and last_buttons[i] == 1:
            send_command(commands[i])

    last_buttons = buttons

    sleep(50)
