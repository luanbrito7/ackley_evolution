import math
import random

from numpy.core.numeric import cross

def power(my_list):
  return [x**2 for x in my_list]

def cos_2_pi(my_list):
  return [math.cos(2 * math.pi * x) for x in my_list]

class Cromossomo():
  def __init__(self, genotipo, min=-15, max=15):
    self.tam = len(genotipo)
    self.min = min
    self.max = max
    self.genotipo = genotipo

  def calculate_fitness(self, base=21):
    # min value is 1 and max is 21
    return base - self.ackley_function()

  def ackley_function(self):
    fenotipos = self.get_fenotipos()
    sum_1 = sum(power(fenotipos))
    sum_2 = sum(cos_2_pi(fenotipos))

    termo_1 = -20 * math.exp(-0.2 * math.sqrt(sum_1/30))
    termo_2 = -math.exp(sum_2/30)

    return termo_1 + termo_2 + 20 + math.e

  def get_fenotipos(self):
    fenotipos = []
    for i in range(30):
      fenotipos.append(self.pegar_valor(i))
    return fenotipos

  def pegar_valor(self, index):
    tam_parcial_gen = int(self.tam/30)
    return self.valor_de_fenotipo(self.genotipo[index * tam_parcial_gen : (index * tam_parcial_gen) + tam_parcial_gen])

  def valor_de_fenotipo(self, gen_list):
    raw_value = 0
    for i, gen in enumerate(gen_list):
      raw_value += gen * (2 ** i)
    return (raw_value * ((self.max - self.min) / ((2 ** len(gen_list)) - 1)) + self.min)

  @classmethod
  def random(cls, tam, min=-15, max=15):
      if tam % 30 != 0:
        print("tamanho do genotipo precisa ser multiplo de 30, aumentando até ficar assim...")
        while tam % 30 != 0:
          tam += 1
        print("novo tamanho: ", tam)
      genotype = []
      for _ in range(tam):
          genotype.append(bool(random.getrandbits(1)))
      return cls(genotype, min, max)
  
  def crossover(self,second_parent,method):
    if(method == 'single_point'):
      return self.single_point_crossover(second_parent)
    elif(method == 'uniform'):
      return self.uniform_crossover(second_parent)
    elif(method == 'arithmetic'):
      return self.arithmetic_crossover(second_parent)

    return False
  
  def single_point_crossover(self,second_parent):
    crossover_point = random.randint(0, 30) * 8
    child1 = self.genotipo[0:crossover_point] + second_parent.genotipo[crossover_point:]
    child2 = second_parent.genotipo[0:crossover_point] + self.genotipo[crossover_point:]
    
    return [Cromossomo(child1),Cromossomo(child2)]
  
  def uniform_crossover(self,second_parent):
    child1 = []
    child2 = []
    for n in range(self.tam):
      prob = random.random()
      if (prob >= 0.5):
        child1.append(self.genotipo[n])
        child2.append(second_parent.genotipo[n])
      else:
        child1.append(second_parent.genotipo[n])
        child2.append(self.genotipo[n])

    return [Cromossomo(child1), Cromossomo(child2)]
  
  def arithmetic_crossover(self,second_parent):
    #XNOR and XOR operators
    child1 = Cromossomo([(self.genotipo[i] == second_parent.genotipo[i]) for i in range(self.tam)])
    child2 = Cromossomo([(not child1.genotipo[i]) for i in range(child1.tam)])

    return [child1,child2]
  
  def mutation(self,probability, method):
    mutation_prob = random.random()
    if(mutation_prob > probability):
      return False
    
    if(method == 'invert_bits'):
      self.mutation_invert_bits()
      return True

    return False
  
  def mutation_invert_bits(self):
    intern_prob = (1/self.tam)
    for n in range(self.tam):
      if random.random() <= intern_prob:
        self.genotipo[n] = not self.genotipo[n]  