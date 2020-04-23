import puzzle as p
import constants as const
import random
import numpy as np
import torch
import torch.nn as nn

def chromosome2tensor(chromosome):
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    i = []
    out = []

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        a.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        b.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        c.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        d.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        e.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        f.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        last = 0
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        g.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        h.append(temp)

    for k in range(const.GRID_LEN * const.GRID_LEN):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        i.append(temp)

    for k in range(4):
        temp = []
        for j in range(const.GRID_LEN * const.GRID_LEN):
            temp.append(float(chromosome[k + j]))
        out.append(temp)

    if(torch.cuda.is_available()):
        a = torch.cuda.FloatTensor(a)
        b = torch.cuda.FloatTensor(b)
        c = torch.cuda.FloatTensor(c)
        d = torch.cuda.FloatTensor(d)
        e = torch.cuda.FloatTensor(e)
        f = torch.cuda.FloatTensor(f)
        g = torch.cuda.FloatTensor(g)
        h = torch.cuda.FloatTensor(h)
        i = torch.cuda.FloatTensor(i)
        out = torch.cuda.FloatTensor(out)
    else:
        a = torch.FloatTensor(a)
        b = torch.FloatTensor(b)
        c = torch.FloatTensor(c)
        d = torch.FloatTensor(d)
        e = torch.FloatTensor(e)
        f = torch.FloatTensor(f)
        g = torch.FloatTensor(g)
        h = torch.FloatTensor(h)
        i = torch.FloatTensor(i)
        out = torch.FloatTensor(out)
    return a,b,c,d,e,f,g,h,i,out

class Chromosome:
    def __init__(self):
        self.genes = np.random.rand(const.CHROMOSOME_LEN)
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
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, const.GRID_LEN * const.GRID_LEN))
            layers.append(nn.Sigmoid())
            layers.append(nn.Linear(const.GRID_LEN * const.GRID_LEN, 4))
            layers.append(nn.Sigmoid())

            net = nn.Sequential(*layers)
            if (torch.cuda.is_available()):
                net = net.cuda()

            with torch.no_grad():
                a, b, c, d, e, f, g, h, i, out = chromosome2tensor(self.genes)
                net[0].weight = nn.Parameter(a)
                net[2].weight = nn.Parameter(b)
                net[4].weight = nn.Parameter(c)
                net[6].weight = nn.Parameter(d)
                net[8].weight = nn.Parameter(e)
                net[10].weight = nn.Parameter(f)
                net[12].weight = nn.Parameter(g)
                net[14].weight = nn.Parameter(h)
                net[16].weight = nn.Parameter(i)
                net[18].weight = nn.Parameter(out)

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
              const.END_SCORE)
        print("\n----------------------------------------------------")
        i = 0
        for x in self.getChromosomes():
            print("Chromosome #", i, " :", x, "| Fitness:", x.getFitness())
            i += 1

    def appendChromosome(self, chromosome):
        self.chromosomes.append(chromosome)
        return self.getChromosomes()


class GeneticAlgorithm:
    @staticmethod
    def evolve(pop):
        return GeneticAlgorithm.mutatePopulation(GeneticAlgorithm.crossoverPopulation(pop))

    @staticmethod
    def mutatePopulation(pop):
        for i in range(const.NUMBER_OF_ELITE_CHROMOSOMES, const.POPULATION_SIZE):
            GeneticAlgorithm.mutateChromosome(pop.getChromosomes()[i])
        return pop

    @staticmethod
    def crossoverPopulation(pop):
        crossoverPopulation = Population(0)
        for i in range(const.NUMBER_OF_ELITE_CHROMOSOMES):
            crossoverPopulation.appendChromosome(pop.getChromosomes()[i])
        i = const.NUMBER_OF_ELITE_CHROMOSOMES
        while i < const.POPULATION_SIZE:
            chromosome1 = GeneticAlgorithm.selectTournamentPopulation(pop).getChromosomes()[0]
            chromosome2 = GeneticAlgorithm.selectTournamentPopulation(pop).getChromosomes()[0]
            crossoverPopulation.appendChromosome(GeneticAlgorithm.crossoverChromosomes(chromosome1, chromosome2))
            i += 1
        return crossoverPopulation

    @staticmethod
    def crossoverChromosomes(chromosome1, chromosome2):
        crossoverChromosome = Chromosome()
        for i in range(const.CHROMOSOME_LEN):
            if random.random() > 0.5:
                crossoverChromosome.getGenes()[i] = chromosome1.getGenes()[i]
            else:
                crossoverChromosome.getGenes()[i] = chromosome2.getGenes()[i]
        return crossoverChromosome

    @staticmethod
    def mutateChromosome(chromosome):
        for i in range(const.CHROMOSOME_LEN):
            if random.random() < const.MUTATION_RATE:
                chromosome.getGenes()[i] = random.random()

    @staticmethod
    def selectTournamentPopulation(pop):
        tournamentPop = Population(0)
        i = 0
        while i < const.TOURNAMENT_SELECTION_SIZE:
            tournamentPop.appendChromosome(pop.getChromosomes()[random.randrange(0, const.POPULATION_SIZE)])
            i += 1
        tournamentPop.getChromosomes().sort(key=lambda x: x.getFitness(), reverse=True)
        return tournamentPop

population = Population(const.POPULATION_SIZE)
genNumber = 0
population.getChromosomes()

while genNumber < const.GEN_MAX and population.getChromosomes()[0].getFitness() < const.CHROMOSOME_LEN:
    population = GeneticAlgorithm.evolve(population)
    population.getChromosomes()
    if(genNumber % 100 == 0):
        population.printPopulation(genNumber)
    genNumber += 1

population.printPopulation(genNumber)