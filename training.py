from canvas import Canvas
from racetrack import Track
from network import FirstNetwork
import os

car_image_paths = [os.path.join('images', f'car{i}.png') for i in range(5)]  # composing car image's paths
canvas = Canvas(Track(), car_image_paths)  # passing the track and car images to the Canvas

population_count = 3
networks = [FirstNetwork() for _ in range(population_count)]
canvas.simulate_generation(networks)