import opc
import time
import board
import busio

import mido

import adafruit_mpr121


def strobe():
    """ strobe effect """
    numLEDs = 512
    client = opc.Client('localhost:7890')

    black = [ (0,0,0) ] * numLEDs
    white = [ (255,255,255) ] * numLEDs

    while True:
	client.put_pixels(white)
	time.sleep(0.05) 
	client.put_pixels(black)
	time.sleep(0.05)


def game_mode():
    i2c = busio.I2C(board.SCL, board.SDA)
    mpr121 = adafruit_mpr121.MPR121(i2c)

    # NOTE you can optionally change the address of the device:
    #mpr121 = adafruit_mpr121.MPR121(i2c, address=0x91)

    # initial touch state
    last = mpr121.touched()

    # Loop forever testing each input and printing when they're touched.
    while True:
        current_touched = mpr121.touched()

	for i in range(12):
            # Each pin is represented by a bit in the touched value.  
            # A value of 1 means the pin is being touched, and 0 means 
            # it is not being touched.
            pin_bit = 1 << i

            # First check if transitioned from not touched to touched.
            if current_touched & pin_bit and not last_touched & pin_bit:
                print('{0} touched!'.format(i))
                if (sounds[i]):
                    sounds[i].play()

            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))

        # Update last state and wait a short period before repeating.
        last_touched = current_touched
        time.sleep(0.1)

        # for debugging
        print('\t\t\t\t\t\t\t\t\t\t\t\t\t 0x{0:0X}'.format(cap.touched()))
        filtered = [cap.filtered_data(i) for i in range(12)]

        print('Filt:', '\t'.join(map(str, filtered)))
        base = [cap.baseline_data(i) for i in range(12)]

        print('Base:', '\t'.join(map(str, base)))


def main():
    # TODO add option selection based on input mode
    game_mode()


if __name__ == '__main__':
    main()
