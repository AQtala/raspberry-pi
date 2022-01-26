import curses
import RPi.GPIO as GPIO   # Import the GPIO library.
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
dc_max=int(input("enter the maximum value of duty cycle: " ))
dc_min=int(input("enter the minimum value of duty cycle: " ))
DC=0
freq_max=int(input("enter the maximum value of frequency: " ))
freq_min=int(input("enter the maximum value of frequency: " ))
frequency=10
pwm = GPIO.PWM(12, frequency)
pwm.start(DC)

# get the curses screen window
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to  the keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)


try:
    while True:
        char = screen.getch()
        if char == ord('e'):
            break
        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            DC+=5
            if DC>dc_max:
                DC=dc_max
            pwm.ChangeDutyCycle(DC)
            screen.addstr(0, 0,str(DC))
            int(DC)
            screen.clrtoeol()

        elif char == curses.KEY_LEFT:
            DC -= 5
            if DC < dc_min:
                DC = dc_min
            pwm.ChangeDutyCycle(DC)
            screen.addstr(0, 0,str(DC))
            int(DC)
            screen.clrtoeol()

        elif char == curses.KEY_UP:
            frequency += 10
            if frequency > freq_max:
                frequency=freq_max
            pwm.ChangeFrequency(frequency)
            screen.addstr(1, 0, str(frequency))
            int(frequency)
            screen.clrtoeol()

        elif char == curses.KEY_DOWN:
            frequency -= 10
            if frequency < freq_min:
                frequency = freq_min
            pwm.ChangeFrequency(frequency)
            screen.addstr(1, 0,str(frequency))
            int(frequency)
            screen.clrtoeol()
finally:
    # shut down cleanly
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    pwm.stop()                         # stop PWM
    GPIO.cleanup()
    print("---------------------------")
    print("the Duty cycle is:", DC)
    print("the frequency is:", frequency)
