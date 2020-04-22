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
        self.genes = np.random.rand(c.CHROMOSOME_LEN)
        self.fitness = 0
        self.gotFitness = False

    def getGenes(self):
        return self.genes

    def getFitness(self):
        if self.gotFitness:
            return self.fitness
        else:
            self.fitness = 0
            layers = []
            layers.append(nn.Linear(c.GRID_LEN * c.GRID_LEN, 2 * c.GRID_LEN * c.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(2 * c.GRID_LEN * c.GRID_LEN, 4))
            layers.append(nn.Sigmoid())

            net = nn.Sequential(*layers)

            with torch.no_grad():
                print(net[0].weight)
                print(net[2].weight)
                x, y = chromosome2tensor(self.genes)
                net[0].weight = nn.Parameter(x)
                net[2].weight = nn.Parameter(y)

            game = p.GameGrid(net) #runs the game with neural network controlling it
            self.fitness = game.EXITCODE
            self.gotFitness = True
            return self.fitness


class Population:
    def __init__(self, size):
        self.chromosomes = []
        for i in range(size):
            self.chromosomes.append(Chromosome())

    def getChromosomes(self):
        return sorted(self.chromosomes, key = lambda x: x.getFitness(), reverse=True)


    def printPopulation(self, genNumber):
        print("\n----------------------------------------------------")
        print("Generation:", genNumber, " Fittest:", self.getChromosomes()[0].getFitness(), " Goal:",
              c.CHROMOSOME_LEN)
        print("\n----------------------------------------------------")
        i = 0
        for x in self.getChromosomes():
            print("Chromosome #", i, " :", x, "| Fitness:", x.getFitness())
            i += 1


class GeneticAlgorithm:
    @staticmethod
    def evolve(pop):
        return GeneticAlgorithm.mutatePopulation(GeneticAlgorithm.crossoverPopulation(pop))

    @staticmethod
    def mutatePopulation(pop):
        for i in range(c.NUMBER_OF_ELITE_CHROMOSOMES, c.POPULATION_SIZE):
            GeneticAlgorithm.mutateChromosome(pop.getChromosomes()[i])
        return pop

    @staticmethod
    def crossoverPopulation(pop):
        crossoverPopulation = Population(0)
        for i in range(c.NUMBER_OF_ELITE_CHROMOSOMES):
            crossoverPopulation.getChromosomes().append(pop.getChromosomes()[i])
        i = c.NUMBER_OF_ELITE_CHROMOSOMES
        while i < c.POPULATION_SIZE:
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
            if random.random() < c.MUTATION_RATE:
                if chromosome.getGenes()[i] == 0:
                    chromosome.getGenes()[i] = 1
                else:
                    chromosome.getGenes()[i] = 0

    @staticmethod
    def selectTournamentPopulation(pop):
        tournamentPop = Population(0)
        i = 0
        while i < c.TOURNAMENT_SELECTION_SIZE:
            tournamentPop.getChromosomes().append(pop.getChromosomes()[random.randrange(0, c.POPULATION_SIZE)])
            i += 1
        tournamentPop.getChromosomes().sort(key=lambda x: x.getFitness(), reverse=True)
        return tournamentPop

population = Population(c.POPULATION_SIZE)
genNumber = 0
population.getChromosomes().sort(key = lambda x: x.getFitness(), reverse = True)

while genNumber < c.GEN_MAX and population.getChromosomes()[0].getFitness() < c.CHROMOSOME_LEN:
    population = GeneticAlgorithm.evolve(population)
    population.getChromosomes().sort(key = lambda x: x.getFitness(), reverse = True)
    if(genNumber % 100 == 0):
        population.printPopulation(genNumber)
    genNumber += 1

population.printPopulation(genNumber)