import math
import time
from rpi_ws281x import *
import numpy as np

# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 15     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def update_mat(board, r, line):
    board_width, board_height = board.shape
    a, b = map(lambda x: (x-1)/2.0, board.shape)
    for i in range(board_height):
        for j in range(board_width):
            distance = abs((i-b)**2 + (j-a)**2)**0.5
            if distance <= r and distance >= r-line:
                board[i][j] = Color(int(255/(distance+1)), int(255/(distance+1)**3) , int(225/(distance+1)**2))
            elif distance < r-line:
                board[i][j] = Color(int(255/(distance+1)**3), int(255/(distance+1)**2) , int(255/(distance+1)))
            else:
                board[i][j] = Color(int(255/(distance+1)**2), int(255/(distance+1)) , int(255/(distance+1))**3)
    return board

def map_led(board,strip):
    board_width, board_height = board.shape
    for i in range(board_height):
        for j in range(board_width):
            if (i % 2) == 0:
                strip.setPixelColor(i*12+j, int(board[i][j]) )
            else:
                strip.setPixelColor(i*12+j, int(np.fliplr(board)[i][j]) )


def rotate_center(board, radians):
    board_width, board_height = board.shape
    rotated = np.zeros(board.shape)
    center = (np.array([[board.shape[1]],
                       [board.shape[0]]]) + 1 ) / 2

    rot_mat = np.array([[math.cos(radians), -math.sin(radians)],
                        [math.sin(radians), math.cos(radians)]])
    for i in range(board_height):
        for j in range(board_width):
            new_pos = np.round(np.matmul(rot_mat, (np.array([[i],[j]]) - center)) + center)
            print(new_pos,i,j)
            if new_pos[0] < 12 and new_pos[1] < 12:
                rotated[int(new_pos[0])][int(new_pos[1])] = board[i][j]
    return rotated


board = np.zeros( (12,12) )



line = 4


# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

for i in range(board.shape[1]):
        for j in range(board.shape[0]):
            if i == j:
                board[i][j] = Color(int(255/(i+1)), int(255/(j+1)) , int(255/(i+j+1)))
phi = 0.0
while True:
    r = 12*math.cos(phi)**2
    update_mat(board,r,line)
    map_led(board,strip)
    strip.show()
#    time.sleep(0.01)
#    board = rotate_center(board, phi)
    phi = phi + 0.01

