import puzzle as p
import constants as c
import random
import numpy as np
import torch
import torch.nn as nn


def chromosome2tensor(chromosome):
    x = []
    y = []

    for i in range(2 * c.GRID_LEN * c.GRID_LEN):
        temp = []
        last = 0
        for j in range(c.GRID_LEN * c.GRID_LEN):
            temp.append(float(chromosome[i + j]))
            last += 1
        x.append(temp)

    for i in range(4):
        temp = []
        for j in range(2*c.GRID_LEN * c.GRID_LEN):
            temp.append(float(chromosome[last + i + j]))
        y.append(temp)
    x = torch.FloatTensor(x)
    y = torch.FloatTensor(y)
    print(x)
    print(y)
    return x, y

class Chromosome:
    def __init__(self):
        self.genes = []
        self.fitness = 0
        for i in range(CHROMOSOME_LEN):
            if random.random() >= 0.5:
                self.genes.append(1)
            else:
                self.genes.append(0)

    def getGenes(self):
        return self.genes

    def getFitness(self):
        self.fitness = 0
        for i in range(c.CHROMOSOME_LEN):
            if self.genes[i] == TARGET_CHROMOSOME[i]:
                self.fitness += 1
        return self.fitness


class Population:
    def __init__(self, size):
        self.chromosomes = []
        for i in range(size):
            self.chromosomes.append(Chromosome())

    def getChromosomes(self): return self.chromosomes


class GeneticAlgorithm:
    @staticmethod
    def evolve(pop):
        return GeneticAlgorithm.mutatePopulation(GeneticAlgorithm.crossoverPopulation(pop))

    @staticmethod
    def mutatePopulation(pop):
        for i in range(NUMBER_OF_ELITE_CHROMOSOMES, POPULATION_SIZE):
            GeneticAlgorithm.mutateChromosome(pop.getChromosomes()[i])
        return pop

    @staticmethod
    def crossoverPopulation(pop):
        crossoverPopulation = Population(0)
        for i in range(NUMBER_OF_ELITE_CHROMOSOMES):
            crossoverPopulation.getChromosomes().append(pop.getChromosomes()[i])
        i = NUMBER_OF_ELITE_CHROMOSOMES
        while i < POPULATION_SIZE:
            chromosome1 = GeneticAlgorithm.selectTournamentPopulation(pop).getChromosomes()[0]
            chromosome2 = GeneticAlgorithm.selectTournamentPopulation(pop).getChromosomes()[0]
            crossoverPopulation.getChromosomes().append(GeneticAlgorithm.crossoverChromosomes(chromosome1, chromosome2))
            i += 1
        return crossoverPopulation

    @staticmethod
    def crossoverChromosomes(chromosome1, chromosome2):
        crossoverChromosome = Chromosome()
        for i in range(c.CHROMOSOME_LEN):
            if random.random() > 0.5:
                crossoverChromosome.getGenes()[i] = chromosome1.getGenes()[i]
            else:
                crossoverChromosome.getGenes()[i] = chromosome2.getGenes()[i]
        return crossoverChromosome

    @staticmethod
    def mutateChromosome(chromosome):
        for i in range(c.CHROMOSOME_LEN):
            if random.random() < MUTATION_RATE:
                if chromosome.getGenes()[i] == 0:
                    chromosome.getGenes()[i] = 1
                else:
                    chromosome.getGenes()[i] = 0

    @staticmethod
    def selectTournamentPopulation(pop):
        tournamentPop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournamentPop.getChromosomes().append(pop.getChromosomes()[random.randrange(0, POPULATION_SIZE)])
            i += 1
        tournamentPop.getChromosomes().sort(key=lambda x: x.getFitness(), reverse=True)
        return tournamentPop


chromosome = np.random.rand(c.CHROMOSOME_LEN)

while(str(p.EXITCODE) != str(c.END_SCORE)):
    layers = []
    layers.append(nn.Linear(c.GRID_LEN * c.GRID_LEN, 2*c.GRID_LEN * c.GRID_LEN))
    layers.append(nn.Sigmoid())
    layers.append(nn.Linear(2*c.GRID_LEN * c.GRID_LEN, 4))
    layers.append(nn.Sigmoid())

    net = nn.Sequential(*layers)

    with torch.no_grad():
        print(net[0].weight)
        print(net[2].weight)
        x,y = chromosome2tensor(chromosome)
        net[0].weight = nn.Parameter(x)
        net[2].weight = nn.Parameter(y)

    OBJ = p.GameGrid(net)
    print(p.EXITCODE)

    print(net)