from brainfuck_me import *
import math
import random

mean_fitness_list = list()

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
    def __init__(self):
        self.seq = ['+', '-', '.', ',', '[', ']', '>', '<']
        self.length = random.randint(2,100)
        self.code = ''.join([random.choice(self.seq) for i in range(self.length)])
        self.fitness = 0

    def mutate(self, prob): # Mutate strlen and str with prob = mutation rate
        if prob > random.random():
            temp_code = list(self.code)
            temp_code[random.randint(0, len(self.code) - 1)] = random.choice(self.seq)
            self.code = ''.join(temp_code)
        pass

    def crossover(self, mom, dad): # Single/Multi point crossover
        self.length = 0
        self.code = ''
        for i in range(random.randint(1, 4)):
            x = random.randint(0,len(mom) - 1)
            y = random.randint(0,len(dad) - 1)
            temp = mom[:x]
            mom = dad[:y] + mom[x:]
            dad = temp + dad[y:]
        if(evaluate_fitness(mom) > evaluate_fitness(dad)):
            self.length = len(mom)
            self.code = mom
        else:
            self.length = len(dad)
            self.code = dad



class Life:
    def __init__(self):
        # Parameters for the genetic algorithm
        self.pop_size = 1000;
        self.mutation_rate = 0.03;
        self.num_gens = 100

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
        print("max fitness = ", max_fitness)
        print("mean fitness = ", mean_fitness)

        mean_fitness_list.append(mean_fitness)

        for i in range(self.pop_size):
            fitness_normal = fitnesses[i] / max_fitness; # Normalize fitness between 0 and 1
            n = int(fitness_normal * 100);  # Arbitrary multiplier
            for j in range(n):
                self.mating_pool.append(self.population[i]); # Based on fitness, probability of selection will be higher for higher fitness because that organism's genes will get added to the mating pool more number of times
        # print(len(self.mating_pool))

    def mate(self):
        # Randomly select 2 individuals from the mating pool
        new_population = [None] * self.pop_size
        for i in range(self.pop_size):
            mom_genome = self.mating_pool[random.randint(0, len(self.mating_pool))]
            dad_genome = self.mating_pool[random.randint(0, len(self.mating_pool))]

            child_genome = pop_member()
            child_genome.crossover(mom_genome.code, dad_genome.code) # Mating
            child_genome.mutate(self.mutation_rate) # Mutation

            new_population[i] = child_genome # Add the child to the next generation population
        for i in range(self.pop_size):
            self.population[i] = new_population[i]


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


if __name__ == '__main__':
    main()
