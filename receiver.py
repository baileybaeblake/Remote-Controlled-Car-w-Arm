
from microbit import *
import radio

# Radio setup
radio.config(group=88)
radio.on()

display.show("R")

# Drive motors
MOTOR_1 = pin1
MOTOR_2 = pin2

# Additional servos
# These pins are placeholders until wiring is confirmed.
SERVO_1 = pin13
SERVO_2 = pin14

# Configure servo PWM
for motor in [MOTOR_1, MOTOR_2, SERVO_1, SERVO_2]:
    motor.set_analog_period(20)


def write_servo(pin, angle):
    # Convert 0-180 degrees into a PWM signal.
    # Assumes a typical 1000-2000 microsecond range.
    angle = max(0, min(180, angle))
    pulse = 1000 + (angle / 180) * 1000
    pin.write_analog(round(pulse * 1023 / 20000))


def run_motor(pin, speed):
    # Convert -100 to +100 speed into servo control.
    speed = max(-100, min(100, speed))
    angle = 90 + speed * 0.9
    write_servo(pin, angle)


def stop_motors():
    run_motor(MOTOR_1, 0)
    run_motor(MOTOR_2, 0)


def process_command(command):
    if command == 1:
        run_motor(MOTOR_1, -100)
        run_motor(MOTOR_2, 100)

    elif command == 2:
        run_motor(MOTOR_1, 100)
        run_motor(MOTOR_2, -100)

    elif command == 3:
        stop_motors()

    elif command == 4:
        run_motor(MOTOR_1, -100)
        run_motor(MOTOR_2, -25)

    elif command == 5:
        run_motor(MOTOR_1, 25)
        run_motor(MOTOR_2, 100)

    elif command == 6:
        stop_motors()

    elif command == 7:
        write_servo(SERVO_1, 0)

    elif command == 10:
        write_servo(SERVO_1, 90)

    elif command == 8:
        write_servo(SERVO_2, 3)

    elif command == 9:
        write_servo(SERVO_2, 90)


# Start stopped
stop_motors()

last_message_time = running_time()

while True:
    message = radio.receive()

    if message is not None:
        try:
            command = int(message)
            process_command(command)

            if command in (1, 2, 3, 4, 5, 6):
                last_message_time = running_time()

        except ValueError:
            pass

    # Stop driving if communication is lost
    if running_time() - last_message_time > 500:
        stop_motors()

    sleep(20)
