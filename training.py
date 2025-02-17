from canvas import Canvas
from racetrack import Track
from network import FirstNetwork
import os

# composing car image's paths
car_image_paths = [os.path.join('images', f'car{i}.png') for i in range(5)]
# passing the track and car images to the Canvas
canvas = Canvas(Track(), car_image_paths)

population_count = 3
networks = [FirstNetwork() for _ in range(population_count)]
canvas.simulate_generation(networks)
