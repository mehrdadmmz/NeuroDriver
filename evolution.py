import itertools
import random


class Evolution:
    def __init__(self, population_count, keep_count):
        self.population_count = population_count
        self.keep_count = keep_count  # number of chromosomes to keep

    # performs a complete evolution to the next generation, we will have 3 generic operators
    def execute(self, rankable_chromosomes):
        # selection: we will take in the list of rankable chromosomes, sort them and take the best 4 chromosomes
        sorted_chromosomes = [w.chromosome for w in sorted(rankable_chromosomes)]
        keep_chromosomes = sorted_chromosomes[:self.keep_count]

        # cross over: selection took the best 4 parents, the cross-over operator takes 2 parents and creates a random
        # crossover point, and then creates 2 offsprings for it by swapping the genes
        # ex: parent1 = [1, 2, 3, 4, 5], parent2 = [6, 7, 8, 9, 10], crossover_point = 2
        # offspring1 = [1, 2, 8, 9, 10], offspring2 = [6, 7, 3, 4, 5]
        reproduction_times = (self.population_count - self.keep_count) // self.keep_count
        offspring = [c for c in keep_chromosomes]  # copy the best chromosomes to the offspring
        for _ in range(int(reproduction_times)):
            for c1, c2 in itertools.batched(keep_chromosomes, 2):  # take 2 parents at a time
                split_index = random.randint(0, len(c1) - 1)  # random split index for crossover
                offspring.append(c1[:split_index] + c2[split_index:])  # create offspring1 from c1 and c2
                offspring.append(c2[:split_index] + c1[split_index:])  # create offspring2 from c1 and c2

        # mutation
        assert len(offspring) == self.population_count, "Offspring count is not population count"
        return offspring
