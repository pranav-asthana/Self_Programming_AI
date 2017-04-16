from brainfuck_me import *
import math
import random
from numba import vectorize

mean_fitness_list = list()
max_fitness_list = list()

def evaluate_fitness(code_string, input = None):
    # Determine fitness of a population member

    # First, sanitize the code string. That is, make sure openign and closing brackets match
    end = len(code_string)
    while 1:
        try:
            prepare_code(code_string)
            break
        except:
            end -= 1
            if end == -2:
                break
            code_string = code_string[:end]
    # print("Evaluating: ", code_string)

    # Call to interpreter
    evaluate_code(read(code_string)) # This takes input from 'input.txt' stores the result in 'output.txt'

    result = open('output.txt', 'r').read()

    # if len(result) > 0:
    #     print('Result: ', result)

    fitness = 0

    desired_result = open('desired.txt', 'r').read()

    # Compute fitness (Here, the aim is to print a known string so the fitness fucction is based on the goal.)
    for i in range(min(len(result), len(desired_result))):
        fitness += 256 - math.fabs(ord(result[i]) - ord(desired_result[i]))

    # print('Fitness: ', fitness)

    return fitness

class pop_member:
    def __init__(self, length = random.randint(2,100), code = ''):
        self.seq = ['+', '-', '.', ',', '[', ']', '>', '<']
        self.length = length
        if code == '':
            self.code = ''.join([random.choice(self.seq) for i in range(self.length)])
        else:
            self.code = code
        self.fitness = 0

    def mutate(self, prob): # Mutate strlen and str with prob = mutation rate
        temp_code = list(self.code)
        for i in range(self.length):
            if prob > random.random():
                d = random.random()
                if d <= 0.25: # Replacement mutation
                    temp_code[i] = random.choice(self.seq)

                elif d <= 0.5: # insertion mutation
                    shiftBit = temp_code[i]
                    temp_code[i] = random.choice(self.seq)

                    up = random.random() >= 0.5
                    if up: # last bit is lost
                        j = i + 1
                        while j < self.length:
                            nextShiftBit = temp_code[j]
                            temp_code[j] = shiftBit
                            shiftBit = nextShiftBit
                            j += 1
                    else: # first bit is lost
                        j = i - 1
                        while j >= 0:
                            nextShiftBit = temp_code[j]
                            temp_code[j] = shiftBit
                            shiftBit = nextShiftBit
                            j -= 1
                elif d <= 0.75: # Deletion mutation
                    up = random.random() >= 0.5
                    if up:
                        j = i
                        while j > 0:
                            temp_code[j] = temp_code[j - 1]
                            j -= 1
                        temp_code[0] = random.choice(self.seq)
                    else:
                        j = i
                        while j < self.length - 1:
                            temp_code[j] = temp_code[j + 1]
                            j += 1
                        temp_code[-1] = random.choice(self.seq)
                else: # Rotation mutation
                    up = random.random() >= 0.5
                    if up:
                        shiftBit = temp_code[0]
                        for j in range(self.length):
                            if j > 0:
                                temp = temp_code[j]
                                temp_code[j] = shiftBit
                                shiftBit = temp
                            else:
                                temp_code[j] = temp_code[-1]
                    else:
                        shiftBit = temp_code[-1]
                        j = self.length - 1
                        while j >= 0:
                            if j < self.length - 1:
                                temp = temp_code[j]
                                temp_code[j] = shiftBit
                                shiftBit = temp
                            else:
                                temp_code[j] = temp_code[0]
                            j -= 1

        self.code = ''.join(temp_code)

    def crossover(self, mom, dad): # Single point crossover
        self.length = 0
        self.code = ''
        x = random.randint(0,len(mom) - 1)
        y = random.randint(0,len(dad) - 1)
        child1 = dad[:y] + mom[x:]
        child2 = mom[:x] + dad[y:]
        self.length = len(child1)
        self.code = child1
        return pop_member(len(child2), child2)

class Life:
    def __init__(self):
        # Parameters for the genetic algorithm
        self.pop_size = 1000
        self.mutation_rate = 0.05
        self.crossover_rate = 0.8
        self.num_gens = 30

        self.population = [None] * self.pop_size
        self.mating_pool = list()

    def random_population(self):
        # initial population (initialized all with length between 2 and 10)
        for i in range(self.pop_size):
            length = random.randint(2, 10)
            self.population[i] = pop_member()

    def select(self): # Roulette wheel selection
        fitnesses = [self.population[i].fitness for i in range(self.pop_size)]
        # print(fitnesses)
        max_fitness = max(fitnesses)
        mean_fitness = sum(fitnesses) / len(fitnesses)

        if max_fitness == 0: max_fitness = 1

        print("max fitness = ", max_fitness)
        print("mean fitness = ", mean_fitness)

        mean_fitness_list.append(mean_fitness)
        max_fitness_list.append(max_fitness)

        for i in range(self.pop_size):
            fitness_normal = fitnesses[i] / max_fitness; # Normalize fitness between 0 and 1
            n = int(fitness_normal * 100);  # Arbitrary multiplier
            for j in range(n):
                self.mating_pool.append(self.population[i]); # Based on fitness, probability of selection will be higher for higher fitness because that organism's genes will get added to the mating pool more number of times
        # print(len(self.mating_pool))

    def mate(self):
        # Randomly select 2 individuals from the mating pool
        new_population = [None] * self.pop_size
        i = 0
        while i < self.pop_size:
            mom_genome = self.mating_pool[random.randint(0, len(self.mating_pool) - 1)]
            dad_genome = self.mating_pool[random.randint(0, len(self.mating_pool) - 1)]

            if random.random() < self.crossover_rate:
                child_genome1 = pop_member()
                child_genome2 = pop_member()
                child_genome2 = child_genome1.crossover(mom_genome.code, dad_genome.code) # Mating
            else:
                child_genome1 = mom_genome
                child_genome2 = dad_genome

            child_genome1.mutate(self.mutation_rate) # Mutation
            child_genome2.mutate(self.mutation_rate)

            new_population[i] = child_genome1 # Add the child to the next generation population
            new_population[i + 1] = child_genome2
            i += 2

        for i in range(self.pop_size):
            self.population[i] = new_population[i]

def plot_stats():
    import matplotlib.pyplot as plt
    import numpy as np
    l = len(mean_fitness_list)
    x = np.linspace(0, l-1, l)
    plt.plot(x, mean_fitness_list)
    plt.plot(x, max_fitness_list)
    plt.show()


def main():
    print("Initializing ...")
    life = Life()

    # life.evaluate_fitness('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[++++++++[++++.+++++++++++++++++++++++++++++.+++++[++..<>+++.>+++++++++++++++++++++++++++++<>++++-.[,.,.,.,.]].].][.,]-,-]][+.--+><<..>[+>[+.<+,]><<>]<><<.>.,--<>[<>-,,,><.>.<-,][-[-,-[.-[-+')
    # life.evaluate_fitness('')

    life.random_population()

    best_fitness = 0
    best_code = ''

    for gen in range(life.num_gens):
        print('Gen: ', gen)
        for i in range(life.pop_size):
            # print('code: ', life.population[i][0])
            life.population[i].fitness = evaluate_fitness(life.population[i].code)
            if life.population[i].fitness > best_fitness:
                best_fitness = life.population[i].fitness
                best_code = life.population[i].code
                print("So far best: ", best_code)
            # print('fitness: ', life.fitness[i])
            # print('--------------------------------------------')

        life.select()
        life.mate()
        print('----------------------------------------')
    plot_stats()

if __name__ == '__main__':
    import cProfile
    cProfile.run('main()')
