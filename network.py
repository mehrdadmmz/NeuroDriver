import random
import math


class Layer:
    def __init__(self, inputs_count, outputs_count):
        self.outputs = [0.0 for _ in range(outputs_count)]
        # 2D matrix for connecting each input to each output, each weight has a value between -1 and 1
        self.weights = [[random.random() * 2 - 1 for _ in range(inputs_count)]
                        for _o in range(outputs_count)]

    def feed_forward(self, inputs):
        # For each output neuron, the code loops through all inputs, multiplies each by the corresponding weight,
        # and accumulates the sum in total. The total is then passed through the activation function, tanh.
        for output_index, output in enumerate(self.outputs):
            total = 0
            for weight_index, inp in enumerate(inputs):
                # total can have an arbitrarily large value
                total += inp * self.weights[output_index][weight_index]
            # for limiting the value between -1 and 1 --> activation func
            self.outputs[output_index] = math.tanh(total)


class Network:
    def __init__(self, dimensions):  # dimensions example: 5, 4, 2
        self.dimensions = dimensions
        self.highest_checkpoint = 0
        self.has_reached_goal = False
        self.layers = []
        for i in range(len(dimensions) - 1):
            self.layers.append(Layer(dimensions[i], dimensions[i + 1]))

    def feed_forward(self, inputs):
        # inputs in the feed_forward will be the radar sensors on the car
        for layer in self.layers:
            layer.feed_forward(inputs)
            # store the layer output back in the input variable to be used as the inputs for the next iteration
            inputs = [i for i in layer.outputs]
        # returning the outputs of the last layer
        return self.layers[-1].outputs

    def serialize(self):
        # serialize the network to a list of weights
        chromosome = []
        for layer in self.layers:
            for outputs in layer.weights:
                for weight in outputs:
                    # the weights matrices of all layers are flattened into a single list and together with the highest
                    # checkpoint, and now we can return them as an instance of RanbkableChromosome
                    chromosome.append(weight)
        return RankableChromosome(self.highest_checkpoint, chromosome)

    # deserialize the chromosome back to the network weights and highest checkpoint
    def deserialize(self, chromosome):
        layer_index = 0
        output_index = 0
        input_index = 0
        for gene in chromosome:  # gene is a weight value between -1 and 1
            self.layers[layer_index].weights[output_index][input_index] = gene  # assign the gene to the weight
            input_index += 1
            # if we have reached the end of the weights of the current output neuron, we move to the next output neuron
            if input_index > len(self.layers[layer_index].weights[output_index]) - 1:
                input_index = 0
                output_index += 1
                if output_index > len(self.layers[layer_index].weights) - 1:
                    output_index = 0
                    layer_index += 1



class RankableChromosome:
    def __init__(self, highest_checkpoint, chromosome):
        self.highest_checkpoint = highest_checkpoint
        self.chromosome = chromosome

    # fitness will determine how the population will be sorted, and we need a __lt__ method to compare two chromosomes
    def __lt__(self, other):
        """Allows sorting chromosomes for rank selection with the following rules:
           - highest checkpoint appears on top of the list"""
        return self.highest_checkpoint > other.highest_checkpoint


