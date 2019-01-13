'''

    Solution for Eight Queens Problem Using the Genetic Algorithms
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    
    Copyright (C) 2012 Enes Ates
    Authors: Enes Ates - enes@enesates.com


'''

import random
from random import randint

class Chromosome():
    def __init__(self):
        self.queens = []
        self.fitness = 0

class GA_8Queens:
    def __init__(self):
        self.population = 10
        self.chromosomes = []
        self.prob_crossover = 0.9   # crossover possibility
        self.prob_mutation = 0.1   # mutation possibility
        self.fitness = 28           # successor value
        self.generation = 0
        self.max_generation = 50
        self.optimum = Chromosome()
        self.crossover_method = "two-point"
        
    def run(self):
        
        self.create_initial_chromosomes()
        
        while not self.success():
            self.next_gen()
            self.generation_info(self.chromosomes) 
            
        print "Result", self.optimum.queens, self.optimum.fitness
    
    def success(self):
        return self.generation >= self.max_generation or \
               self.fitness == self.optimum.fitness
  
    def next_gen(self):
        
        next_generation = []
        self.generation += 1
        success = False
        
        next_generation.append(self.optimum)
        while len(next_generation) < self.population  and  success == False:
            success = self.crossover(self.chromosomes, next_generation)
            
        self.chromosomes = next_generation
    
    def generation_info(self, chromosomes):
        
        i=0
        print "\n\n"
        print self.generation, ". generation"
        print "-----------------------------\n"
        
        for chrom in chromosomes:
            i += 1
            print i, ". chromosome: ", chrom.queens, ", fitness: ", chrom.fitness
            
            if (chrom.fitness > self.optimum.fitness):
                self.optimum = chrom
                print "Optimum:", self.optimum.queens, self.optimum.fitness
    
                     
    def create_initial_chromosomes(self):
        
        for i in range(0, self.population):
            chromosome = Chromosome()
            chromosome.queens = range(0, 8)
            
            random.shuffle(chromosome.queens)
            chromosome.fitness = self.calc_fitness(chromosome.queens)
                        
            self.chromosomes.append(chromosome)
            
        self.generation += 1
        self.generation_info(self.chromosomes)
            
    def calc_fitness(self, queens):
        
        fitness = self.fitness
        
        for i in range(0, 8):
            for j in range(i+1, 8):
                if((j-i) == abs(queens[i] - queens[j])):
                    fitness -= 1
                    
        return fitness       

    def crossover(self, chromosomes, next_generation):

        first_chrom = self.choose_chromosome(chromosomes)
        chromosomes.remove(first_chrom)
        second_chrom = self.choose_chromosome(chromosomes)
        chromosomes.append(first_chrom)
        
        if random.random() < self.prob_crossover:
    
            child_1 = Chromosome()
            child_2 = Chromosome()
            
            if self.crossover_method == "one-point":
                child_1.queens = first_chrom.queens[0:5] + second_chrom.queens[5:8]
                child_2.queens = second_chrom.queens[0:5] + first_chrom.queens[5:8]
            elif self.crossover_method == "two-point":
                child_1.queens = first_chrom.queens[0:3] + second_chrom.queens[3:6] + first_chrom.queens[6:8]
                child_2.queens = second_chrom.queens[0:3] + first_chrom.queens[3:6] + second_chrom.queens[6:8]
            elif self.crossover_method == "random-point":
                for i in range(0,8):
                    first, second = random.sample([first_chrom.queens[i], second_chrom.queens[i]], 2)
                    child_1.queens.append(first), child_2.queens.append(second)
                    
            child_1.fitness = self.calc_fitness(child_1.queens)
            child_2.fitness = self.calc_fitness(child_2.queens)
            
            if child_1.fitness == self.fitness or child_2.fitness == self.fitness:
                success = True
            
            print "Crossover result:", first_chrom.queens, "with", second_chrom.queens, "-->", child_1.queens, "fitness:", child_1.fitness
            success = self.mutation(child_1, next_generation)
            print "Crossover result:", first_chrom.queens, "with", second_chrom.queens, "-->", child_2.queens, "fitness:", child_2.fitness
            success = self.mutation(child_2, next_generation)
            
        else:
            success = self.mutation(first_chrom, next_generation)    
            success = self.mutation(second_chrom, next_generation)   
            
        return success 
            
    def mutation(self, chromosome, next_generation):
        
        for i in range(0,8):
            if random.random() < self.prob_mutation:
                chromosome.queens[i] = random.randint(0, 7)
                chromosome.fitness = self.calc_fitness(chromosome.queens)
                print "Mutation result:", chromosome.queens, "fitness:", chromosome.fitness
                
        next_generation.append(chromosome)
        if chromosome.fitness == self.fitness:
            return True
        else:
            return False
        
    def choose_chromosome(self, chromosomes):
        
        total_fitness = 0  
        for chrom in chromosomes:
            total_fitness += chrom.fitness

        rand  =  randint(1, total_fitness)
        
        roulette = 0
        for chrom in self.chromosomes:
            roulette += chrom.fitness
            if rand <= roulette:
                return chrom
                
               
if __name__ == "__main__":
    ga8 = GA_8Queens()
    ga8.run()