class Genetic:
  def __init__(self, weights, profits, capacity, start_num_chromosomes, num_chromosomes):
    if (len(weights) != len(profits)):
      raise TypeError("Error! Size of weights not equal size of profits!")
    self.weights = weights
    self.profits = profits
    self.capacity = capacity
    self.start_num_chromosomes = start_num_chromosomes
    self.num_chromosomes = num_chromosomes
    self.num_items = len(weights)
    self.knapsack = []
    self.population = []

  def solve(self):
    self.generate_population(self.start_num_chromosomes)
    while(1):
      value_population, fit_population = self.fit_fun()
      flag, max_ind = self.check_population(value_population, fit_population)
      if(flag):
        self.knapsack = self.population[max_ind]
        return self.knapsack
      else:
        new_population = self.group_selection(fit_population, self.num_chromosomes)
        self.population = self.mutation(new_population)

  def generate_population(self, num_chromosomes):
    self.population = [random.choices([0,1], k = self.num_items) for i in range(num_chromosomes )]
    return self.population

  def fit_fun(self):
    fit_population = []
    value_population = []
    for chromosomes in self.population:
      total_value = sum([chromosomes[i] * self.weights[i] for i in range(self.num_items)])
      while (total_value > self.capacity):
        indexes = [i for i, v in enumerate(chromosomes) if v == 1]
        ind_for_change = random.choices(indexes)[0]
        chromosomes[ind_for_change] = 0
        total_value = sum([chromosomes[i] * self.weights[i] for i in range(self.num_items)])
      value_population.append(total_value)
      fit_population.append(sum([chromosomes[i] * self.profits[i] for i in range(self.num_items)]))
    return (value_population, fit_population)

  def check_population(self, value_population, fit_population):
    max_value = max(fit_population)
    max_ind = fit_population.index(max_value)
    max_count = fit_population.count(max_value)
    if(max_count >= (0.6 * self.num_items)):
      return (True, max_ind)
    else:
      return (False, max_ind)

  def single_point_crossover(self, chromosome_x, chromosome_y):
      crossover_ind = random.randint(0, len(chromosome_x)-1)
      return chromosome_x[:crossover_ind] + chromosome_y[crossover_ind:]

  def group_selection(self, fit_population, generation_size):
    sorted_population = sorted(range(len(fit_population)), key=lambda k:fit_population[k], reverse=True)
    group_size = int(len(sorted_population) // 4)
    random_weights = [0.5] * group_size + [0.3] * group_size + [0.15] * group_size + [0.05] * group_size
    diff = len(sorted_population) - len(random_weights)
    for i in range(diff):
      random_weights.append(0.05)
    new_population = []
    for i in range(generation_size):
      x, y = random.choices(sorted_population, weights=random_weights, k = 2)
      new_chromosome = self.single_point_crossover(self.population[x], self.population[y])
      new_population.append(new_chromosome)
    return new_population

  def mutation(self, new_population):
    for chromosomes in new_population:
      choice = random.choices([0,1], weights=[0.9, 0.1], k = 1)
      if(choice == 1):
        ind = random.randint(0, len(chromosomes)-1)
        if(chromosomes[ind] == 0):
          chromosomes[ind] = 1
        else:
          chromosomes[ind] = 0
    return new_population
