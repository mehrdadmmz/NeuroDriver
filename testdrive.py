# import os
# from canvas import Canvas
# from racetrack import Track
# from network import Network
# from storage import Storage
#
#
# # Network configuration
# network_dimensions = 5, 4, 2  # input neurons, hidden layer neurons, output neurons
#
# car_images = [os.path.join('images', f'car{i}.png') for i in range(5)]
# canvas = Canvas(Track(4), car_images)  # I will be using track 4 which the cars have never seen before
# storage = Storage("brain.json")
# networks = [Network(network_dimensions) for _ in range(4)]  # I will be using 4 cars for this test drive
#
# # Load the brain and initialize the network with it
# best_chromosomes = storage.load()
# for c, n in zip(best_chromosomes, networks):
#     n.deserialize(c)
#
# # Letting the test drive run 5 times
# simulation_round = 1
# while canvas.is_simulating:
#     canvas.simulate_generation(networks, simulation_round)
#     simulation_round += 1
import os
from canvas import Canvas
from network import Network
from racetrack import Track
from storage import Storage

# Network configuration
network_dimensions = 5, 4, 2  # input neurons, hidden layer neurons, output neurons

# I will be using track 4 which the cars might not have seen before
car_image_paths = [os.path.join("images", f"car{i}.png") for i in range(5)]
canvas = Canvas(Track(4), car_image_paths)

storage = Storage("brain.json")

# I will be using 4 cars for this test drive
networks = [Network(network_dimensions) for _ in range(4)]

# Load the brain and initialize each network with it
best_chromosomes = storage.load()
for c, n in zip(best_chromosomes, networks):
    n.deserialize(c)

# Let the test drive run 5 times, or until the canvas is no longer simulating
simulation_round = 1
while simulation_round <= 5 and canvas.is_simulating:
    canvas.simulate_generation(networks, simulation_round)
    simulation_round += 1
