from pyglet import image
import os
import json
import itertools
# to keep track of the track file name and also having a binary matrix with 0s and 1s --> 1 when we are on the road
# and 0 when we are off the road


class Track():
    def __init__(self, index):
        self.track_image = image.load(os.path.join('images', f'track{index}.png'))
        self.track_overlay_image = image.load(os.path.join('images', f'track{index}-overlay.png'))
        with open(os.path.join('images', f'track{index}.json')) as file:
            data = json.load(file)
        # the "checkpoints": [[550, 140]] in the json file
        self.checkpoints = data['checkpoints']
        pitch = self.track_image.width * len("RGBA")
        # getting pixels as groups of 'RGBA' bytes
        pixels = self.track_image.get_data("RGBA", pitch)
        # r, g, b = 75: gray colour, 255 fully opaque (not transparent at all),itertools to iterate in chunks of 4 bytes
        map = [1 if b == (75, 75, 75, 255) else 0 for b in itertools.batched(pixels, 4)]
        # map_matrix represents the track in a binary format, it is 540 lines high
        self.map_matrix = [map[n:n + self.track_image.width]
                           for n in range(0, self.track_image.width * self.track_image.height, self.track_image.width)]

    def is_road(self, x, y):
        if x < 0 or x > 960 or y < 0 or y > 540:
            return False
        # return true if the coordinate represent the road
        return self.map_matrix[int(y)][int(x)] == 1
