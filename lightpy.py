import spidev
import time
 

DEBUG = 0

spi = spidev.SpiDev()
spi.open(0,0)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
	r = spi.xfer2([1,(8+adcnum)<<4,0])
	adcout = ((r[1]&3) << 8) + r[2]
	return adcout

# 10k trim pot connected to adc #0
lightsensor_adc = 0;

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

while True:
        # we'll assume that the pot didn't move
        trim_pot_changed = False

        # read the analog pin
        trim_pot = readadc(lightsensor_adc)
        # how much has it changed since the last read?
        pot_adjust = abs(trim_pot - last_read)

        if DEBUG:
                print "trim_pot:", trim_pot
                print "pot_adjust:", pot_adjust
                print "last_read", last_read

        if ( pot_adjust > tolerance ):
               trim_pot_changed = True

        if DEBUG:
                print "trim_pot_changed", trim_pot_changed

        if ( trim_pot_changed ):
            print 'Light = {light}%' .format(light = trim_pot)
 

        # save the potentiometer reading for the next loop
        last_read = trim_pot
        # hang out and do nothing for a half second
        time.sleep(0.5)