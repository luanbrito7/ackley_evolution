import math
import random
import numpy as np
import matplotlib.pyplot as plt
from cromossomo import Cromossomo
from selection import parent_selection, survivor_selection, solution_found, converged_number, average_fitness, highest_fitness

def run_evolution():
  population = []

  # 100 pais na populaçao
  n_population = 200
  for _ in range(n_population):
    # cada pai tem cromossomo de tam 240 (isso pode variar pra qualquer multiplo de 30)
    # enquanto maior, mais valores entre -15 e 15 o cromossomo pode representar
    population.append(Cromossomo.random(240))

  iterations = 0
  while(iterations <= 10000 and not solution_found(population)):
    #Crossover
    crossover_prob = random.random()
    if(crossover_prob <= 0.9):
      for _ in range(10):
        parents = parent_selection(population,'best_random',10)
        childs = parents[0].crossover(parents[1],'uniform')
        population.extend(childs)

    #Mutation
    for p in population:
      p.mutation(0.1,'invert_bits')

    #Selection
    for _ in range(len(population)-n_population):
      population = survivor_selection(population,'elitist',10)
    
    iterations += 1
  
  return {
    "iterations": iterations,
    "converged_number": converged_number(population),
    "average_fitness": average_fitness(population),
    "best_fitness": highest_fitness(population)
  }

def dp(iterations, mean):
  _sum = 0
  for i in iterations:
    _sum += pow((i - mean), 2)
  return math.sqrt(_sum/len(iterations))

def avaliate(iterations):
  total_generations = []
  average_fitness = []
  converged_iterations = 0
  for i in range(iterations):
    res = run_evolution()
    generations = res["iterations"]
    converged_number = res["converged_number"]
    a_f= res["average_fitness"]
    best_fit = res["best_fitness"]
    average_fitness.append(a_f)
    print("Iteration: ", i + 1)
    print("Average fitness: ", a_f)
    print("Best fitness: ", best_fit)
    print("Number of individuals converged: ", converged_number)
    total_generations.append(generations)
    if converged_number > 0:
      converged_iterations += 1
  mean = sum(total_generations) / iterations
  res_dp = dp(total_generations, mean)
  print("Generations mean: ", mean)
  print("Generations DP: ", res_dp)
  print("Converged in %", converged_iterations/iterations)
  x = np.arange(iterations)
  plt.bar(x, height=average_fitness)
  plt.xticks(x, list(range(iterations)))
  plt.show()

def main():
  avaliate(5)

if __name__ == "__main__":
  main()