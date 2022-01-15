import numpy as np
import math

class led_object:
    def __init__(self, height, width):
        self.picture = np.zeros(height,width)
        self.dimensions = (height, width)
        self.position = self.init_positions(self)
        
    def init_positions(self):
        positions = np.zeros(self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                positions[i][j] = (i, j)
        return positions
        
    def update_positions(self, radians):
        a, b = map(lambda x: (x-1)/2.0, board.shape)
        for i in range(height):
            for j in range(width):
                x, y = self.positions[i][j]
                x, y = ((x-a)*math.cos(radians)-(y-b)*math.sin(radians) + a , (x-a)*math.sin(radians) + (y-b)*math.cos(radians) + b)
                self.positions[i][j] = (x, y)

        
        
    def rotate_center(self, radians):
        board_width, board_height = self.dimensions
        rotated = np.zeros(board.shape)
        center = (np.array([[board.shape[1]],
                           [board.shape[0]]]) + 1 ) / 2
        
        rot_mat = np.array([[math.cos(radians), -math.sin(radians)],
                            [math.sin(radians), math.cos(radians)]])
        for i in range(board_height):
            for j in range(board_width):
                new_pos = np.round(np.matmul(rot_mat, (np.array([[i],[j]]) - center)) + center)
                if new_pos[0] < 12 and new_pos[1] < 12:
                    rotated[int(new_pos[0])][int(new_pos[1])] = board[i][j]
        return rotated
