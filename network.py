import random
import math


class Layer:
    def __init__(self, inputs_count, outputs_count):
        self.outputs = [0.0 for _ in range(outputs_count)]
        # 2D matrix for connecting each input to each output, each weight has a value between -1 and 1
        self.weights = [[random.random() * 2 - 1 for _ in range(inputs_count)] for _o in range(outputs_count)]

    def feed_forward(self, inputs):
        # For each output neuron, the code loops through all inputs, multiplies each by the corresponding weight,
        # and accumulates the sum in total. The total is then passed through the activation function, tanh.
        for output_index, output in enumerate(self.outputs):
            total = 0
            for weight_index, inp in enumerate(inputs):
                total += inp * self.weights[output_index][weight_index]  # total can have an arbitrarily large value
            self.outputs[output_index] = math.tanh(total)  # for limiting the value between -1 and 1 --> activation func


class Network:
    def __init__(self, dimensions):  # dimensions example: 5, 4, 2
        self.dimensions = dimensions
        self.layers = []
        for i in range(len(dimensions) - 1):
            self.layers.append(Layer(dimensions[i], dimensions[i + 1]))

    def feed_forward(self, inputs):
        # inputs in the feed_forward will be the radar sensors on the car
        for layer in self.layers:
            layer.feed_forward(inputs)
            # store the layer output back in the input variable to be used as the inputs for the next iteration
            inputs = [i for i in layer.outputs]
        return self.layers[-1].outputs  # returning the outputs of the last layer



