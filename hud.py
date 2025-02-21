from pyglet.text import Label
from pyglet.shapes import Circle

class NeuronSprite:
    def __init__ (self, x, y, batch):
        self.node_border = Circle(x, y, 22, color=(0, 0, 0, 255), batch=batch)
        self.node_fill = Circle(x, y, 20, color=(255, 255, 255, 255), batch=batch)
        self.node_value = Label(x=x, y=y, color=(255, 255, 255, 255), font_size=12,
                                anchor_x='center', anchor_y='center', batch=batch)

    # update the value of the neuron, make it green if positive, red if negative, Values range from -1 to 1
    def update(self, value):
        self.node_value.text = f"{value:.2f}"
        if value > 0:
            self.node_fill.color = 0, int(value * 255), 0, 255
        else:
            self.node_fill.color = int(value * 200), 0, 0, 255


# HUD: heads up display
# The HUD class is responsible for displaying the current round, population, and speed of the cars.
class Hud:
    def __init__(self, simulation_round, dimensions, batch):
        self.round_label = Label(f"Round: {simulation_round}", x=20, y=520, color=(0, 0, 0, 255), batch=batch)
        self.population_label = Label(x=120, y=520, color=(0, 0, 0, 255), batch=batch)
        self.speed_label = Label(x=280, y=520, color=(0, 0, 0, 255), batch=batch)
        self.neurons = []
        x = 40
        for neuron_count in dimensions:
            total_height = neuron_count * 50 - 10
            y = 480 - (540 - total_height) / 2
            for _ in range(neuron_count):
                self.neurons.append(NeuronSprite(x, y, batch))
                y -= 50
            x += 50

    def update(self, network, alive, population, speed):
        self.population_label.text = f"Population: {alive}/{population}"
        self.speed_label.text = f"Speed: {speed:.2f}"
        index = 0
        for input in network.inputs:  # starting from the input neurons
            self.neurons[index].update(input)
            index += 1
        for layer in network.layers:  # continue with the hidden layers
            for value in layer.outputs:
                self.neurons[index].update(value)
                index += 1
