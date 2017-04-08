from brainfuck_me import *
import math
import random

class pop_member:
    def __init__(self, length):
        self.seq = ['+', '-', '.', ',', '[', ']', '>', '<']
        self.code = ''.join([random.choice(self.seq) for i in range(length)])


class Life:
    def __init__(self):
        self.pop_size = 1000;
        self.mutation_rate = 0.03;
        self.population = [None] * self.pop_size
        self.fitness = [0] * self.pop_size
        self.mating_pool = list()

    def random_population(self):
        for i in range(self.pop_size):
            length = random.randint(2, 10)
            self.population[i] = [pop_member(length).code]
            self.population[i].append(length)

    def evaluate_fitness(self, code_string, input = None):
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

        evaluate_code(read(code_string))

        result = open('output.txt', 'r').read()

        # if len(result) > 0:
        #     print('Result: ', result)

        fitness = 0

        desired_result = open('desired.txt', 'r').read()

        for i, j in zip(range(len(result)), range(len(desired_result))):
            # print('comparing: ', result[i], 'with', desired_result[j])
            fitness += 256 - math.fabs(ord(result[i]) - ord(desired_result[j]))

        # print('Fitness: ', fitness)

        return fitness


    def select(self): # Roulette wheel selection
        max_fitness = max(self.fitness)
        mean_fitness = sum(self.fitness) / max_fitness

        for i in range(self.pop_size):
            fitness_normal = self.fitness[i]/max_fitness; # Normalize fitness between 0 and 1
            n = int(fitness_normal * 100);  # Arbitrary multiplier
            for j in range(n):
                self.mating_pool.append(self.population[i]); # Based on fitness, probability of selection will be higher for higher fitness because that organism's genes will get added to the mating pool more number of times
        # print(len(self.mating_pool))

    def mate(self):
        for i in range(self.pop_size):
            mom_genome = self.mating_pool[random.randint(0, len(self.mating_pool))]
            dad_genome = self.mating_pool[random.randint(0, len(self.mating_pool))]

            child_genome = self.crossover(mom_genome, dad_genome) # Mating

            child_genome = self.mutate(child_genome)

            self.population[i] = child_genome

    def mutate(): # Mutate strlen and str with prob = mutation rate
        pass

    def crossover(): # Single/Multi point crossover
        pass


def main():
    print("Initializing ...")
    life = Life()

    life.evaluate_fitness('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[++++++++[++++.+++++++++++++++++++++++++++++.+++++[++..<>+++.>+++++++++++++++++++++++++++++<>++++-.[,.,.,.,.]].].][.,]-,-]][+.--+><<..>[+>[+.<+,]><<>]<><<.>.,--<>[<>-,,,><.>.<-,][-[-,-[.-[-+')
    life.evaluate_fitness('')

    life.random_population()
    for i in range(life.pop_size):
        # print('code: ', life.population[i][0])
        life.fitness[i] = life.evaluate_fitness(life.population[i][0])
        # print('fitness: ', life.fitness[i])
        # print('--------------------------------------------')

    print('Max fitness: ', max(life.fitness))
    print('Fittest individual: ', life.population[life.fitness.index(max(life.fitness))][0])

    life.select()



if __name__ == '__main__':
    main()
