from canvas import Canvas
from racetrack import Track
from network import Network
from evolution import Evolution
import os

# composing car image's paths
car_image_paths = [os.path.join('images', f'car{i}.png') for i in range(5)]
# passing the track and car images to the Canvas
canvas = Canvas(Track(1), car_image_paths)


# Network and genetic algorithm configuration
network_dimensions = 5, 4, 2  # input neurons, hidden layer neurons, output neurons
population_count = 40
max_generation_iterations = 5  # number of generations to simulate
keep_count = 4  # number of chromosomes to keep in each generation

networks = [Network(network_dimensions) for _ in range(population_count)]
evolution = Evolution(population_count, keep_count)

simulation_round = 1
while simulation_round <= max_generation_iterations and canvas.is_simulating:
    print(f"=== Round {simulation_round} ===")
    canvas.simulate_generation(networks, simulation_round)
    simulation_round += 1
    if canvas.is_simulating:
        print(f"-- Average checkpoint reached: {sum(n.highest_checkpoint for n in networks) / len(networks):.2f} --")

        serialized = [network.serialize() for network in networks]
        offspring = evolution.execute(serialized)

        # create new networks from the offspring
        networks = []
        for chromosome in offspring:
            network = Network(network_dimensions)
            network.deserialize(chromosome)
            networks.append(network)
