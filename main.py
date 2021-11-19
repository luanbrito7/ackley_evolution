from cromossomo import Cromossomo

def main():
  population = []

  # 100 pais na populaçao
  for _ in range(100):
    # cada pai tem cromossomo de tam 240 (isso pode variar pra qualquer multiplo de 30)
    # enquanto maior, mais valores entre -15 e 15 o cromossomo pode representar
    population.append(Cromossomo.random(240))

  for p in population:
    print(p.calculate_fitness())

if __name__ == "__main__":
  main()