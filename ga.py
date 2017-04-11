from brainfuck_me import *
import math
import random

class pop_member:
    def __init__(self):
        self.seq = ['+', '-', '.', ',', '[', ']', '>', '<']
        self.length = random.randint(2,100)
        self.code = ''.join([random.choice(self.seq) for i in range(self.length)])
        self.fitness = 0


class Life:
    def __init__(self):
        # Parameters for the genetic algorithm
        self.pop_size = 1000;
        self.mutation_rate = 0.03;
        self.num_gens = 10

        self.population = [None] * self.pop_size
        self.mating_pool = list()

    def random_population(self):
        # initial population (initialized all with length between 2 and 10)
        for i in range(self.pop_size):
            length = random.randint(2, 10)
            self.population[i] = pop_member()

    def evaluate_fitness(self, code_string, input = None):
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
        for i, j in zip(range(len(result)), range(len(desired_result))):
            # print('comparing: ', result[i], 'with', desired_result[j])
            fitness += 256 - math.fabs(ord(result[i]) - ord(desired_result[j]))

        # print('Fitness: ', fitness)

        return fitness


    def select(self): # Roulette wheel selection
        fitnesses = [self.population[i].fitness for i in range(self.pop_size)]
        # print(fitnesses)
        max_fitness = max(fitnesses)
        mean_fitness = sum(fitnesses) / max_fitness

        for i in range(self.pop_size):
            fitness_normal = fitnesses[i] / max_fitness; # Normalize fitness between 0 and 1
            n = int(fitness_normal * 100);  # Arbitrary multiplier
            for j in range(n):
                self.mating_pool.append(self.population[i]); # Based on fitness, probability of selection will be higher for higher fitness because that organism's genes will get added to the mating pool more number of times
        # print(len(self.mating_pool))

    def mate(self):
        # Randomly select 2 individuals from the mating pool
        for i in range(self.pop_size):
            mom_genome = self.mating_pool[random.randint(0, len(self.mating_pool))]
            dad_genome = self.mating_pool[random.randint(0, len(self.mating_pool))]

            child_genome = self.crossover(mom_genome, dad_genome) # Mating

            child_genome = self.mutate(child_genome) # Add mutation

            self.population[i] = child_genome # Add the child to the next generation population

    def mutate(self, gene): # Mutate strlen and str with prob = mutation rate
        return gene

    def crossover(self, mom, dad): # Single/Multi point crossover
        return mom
        pass


def main():
    print("Initializing ...")
    life = Life()

    life.evaluate_fitness('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[++++++++[++++.+++++++++++++++++++++++++++++.+++++[++..<>+++.>+++++++++++++++++++++++++++++<>++++-.[,.,.,.,.]].].][.,]-,-]][+.--+><<..>[+>[+.<+,]><<>]<><<.>.,--<>[<>-,,,><.>.<-,][-[-,-[.-[-+')
    life.evaluate_fitness('')

    life.random_population()

    for gen in range(life.num_gens):
        print('Gen: ', gen)
        for i in range(life.pop_size):
            # print('code: ', life.population[i][0])
            life.population[i].fitness = life.evaluate_fitness(life.population[i].code)
            # print('fitness: ', life.fitness[i])
            # print('--------------------------------------------')

        life.select()
        life.mate()
        print('----------------------------------------')


if __name__ == '__main__':
    main()
