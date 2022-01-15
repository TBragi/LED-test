import math
import numpy as np
import time
from PIL import Image
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def extractROI(image, windowSize, filter=Image.LANCZOS, degree=0):
	return np.array(image.rotate(degree).resize((windowSize[0], windowSize[1]), resample = filter))[:,:,0:3]

def discretizeImage(roiImage,noLevels):

	normalizedImage = roiImage / float(roiImage.max())
	discretizedImage = np.floor( normalizedImage * noLevels ).astype( int )
	multiplier = 255 / noLevels
	discretizedImage = np.floor( discretizedImage * multiplier ).astype( np.uint8 ) #Rescale to range 0-255
	return discretizedImage

def map_led(board,strip):
    board_width, board_height, board_depth = board.shape
    for i in range(board_height):
        for j in range(board_width):
            if (i % 2) == 0:
                strip.setPixelColor(i*12+j, Color(*board[i,j]) )
            else:
                strip.setPixelColor(i*12+j, Color(*np.fliplr(board)[i,j]) )
    return strip


pixel_x = 12
pixel_y = 12
windowSize = (pixel_x, pixel_y)
noLevels = 255 #Brightness levels of LED
max_loop = 12*12
time_loop = 0.05
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

with Image.open('poke.png') as newImage:
	while True:
		for i in range(0,max_loop):
			degree = i * 360 / max_loop
			roi = extractROI(newImage, windowSize, Image.ANTIALIAS, degree)
			discRoi = discretizeImage( roi, noLevels )
			strip = map_led( np.fliplr(discRoi), strip )
			#strip = map_led( np.fliplr(roi), strip )
			strip.show()
			time.sleep(time_loop)
