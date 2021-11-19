import math
import random

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
    