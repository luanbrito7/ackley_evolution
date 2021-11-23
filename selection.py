import random
from cromossomo import Cromossomo

# Call Functions
def parent_selection(population,method,n):
    if(method == 'best_random'):
        return best_two_of_random_parent(population,n)
    elif(method == 'roulette'):
        return roulette_parent(population)
    elif(method == 'tournament'):
        return tournament_parent(population,n)

    return False

def survivor_selection(population,method,tournament_len):
    if(method == 'elitist'):
        return elitist_selection(population)
    elif(method == 'roulette'):
        return roulette_selection(population)
    elif(method == 'tournament'):
        return tournament_selection(population,tournament_len)

    return False

# Parent_Selection Methods
def best_two_of_random_parent(population,n):
  chosen_ones = random.sample(range(len(population)),n)
  randon_ten = []
  for i in chosen_ones:
    randon_ten.append(population[i])
  
  parent1 = highest_fitness(randon_ten)
  randon_ten.pop(randon_ten.index(parent1[0]))
  parent2 = highest_fitness(randon_ten)

  return[parent1[0],parent2[0]]

def roulette_parent(population):
    parent1 = roulette(population)[0]
    parent2 = roulette(population)[0]

    return[parent1,parent2]

def tournament_parent(population, n):
    chosen_ones = random.sample(range(len(population)),n)
    competitors = [population[i] for i in chosen_ones]
    winner = roulette(competitors)
    competitors.pop(winner[1]) # Without Replacement
    parent1 = winner[0]
    parent2 = roulette(competitors)[0]
    
    return [parent1,parent2]

# Survivor_Selection Methods
def elitist_selection(population):
    population.pop(smallest_fitness(population)[0])
    return population

def roulette_selection(population):
    population.pop(roulette_invert(population)[1])
    return population

def tournament_selection(population, n):
    chosen_ones = random.sample(range(len(population)),n)
    competitors = [population[i] for i in chosen_ones]
    winner = roulette_invert(competitors)
    population.pop(chosen_ones[winner[1]])
    return population
    

# Other Help Functions
def highest_fitness(population):
  found, fitness = "", 0
  for p in population:
    actual_fit = p.calculate_fitness()
    if actual_fit > fitness:
      fitness = actual_fit
      found = p
  return [found, fitness]

def smallest_fitness(population):
    index, fitness = -1, 21
    for i in range(len(population)):
        actual_fit = population[i].calculate_fitness()
        if actual_fit <= fitness:
            fitness = actual_fit
            index = i
    return [index, fitness]

def fitness_sum(population):
    _sum = 0
    for p in population:
        _sum += p.calculate_fitness()
    
    return _sum

def fitness_invert_sum(population):
    _sum = 0
    for p in population:
        _sum += (21 - p.calculate_fitness())
    
    return _sum

def roulette(population):
    fit_sum = fitness_sum(population)
    rand_float = random.uniform(0,fit_sum)
    for n in range(len(population)):
        p = population[n]
        rand_float -= p.calculate_fitness()
        if(rand_float <= 0):
            return [p,n]
    
    return [population[-1],-1]

def roulette_invert(population):
    fit_sum = fitness_invert_sum(population)
    rand_float = random.uniform(0,fit_sum)
    for n in range(len(population)):
        p = population[n]
        rand_float -= (21 - p.calculate_fitness())
        if(rand_float <= 0):
            return [p,n]
    
    return[population[-1],-1]

def solution_found(population):
  for p in population:
    if (p.calculate_fitness() > 20.5):
      return True
  return False

def converged_number(population):
  total = 0
  for p in population:
    actual_fit = p.calculate_fitness()
    if actual_fit > 20.5:
      total += 1
  return total

def average_fitness(population):
  total = fitness_sum(population)
  return total/len(population)
