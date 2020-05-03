class Greedy:
  def __init__(self, weights, profits, capacity):
    if (len(weights) != len(profits)):
      raise TypeError("Error! Size of weights not equal size of profits!")
    self.weights = weights
    self.profits = profits
    self.capacity = capacity
    self.num_items = len(weights)
    self.knapsack = [0] * self.num_items

  def solve(self):
    quality = [p / w for p, w in zip(self.profits, self.weights)]
    sorted_quality_ind = sorted(range(self.num_items), key=lambda k:quality[k], reverse=True)
    total_sum = 0
    while((total_sum < self.capacity) and (sorted_quality_ind != [])):
      best_ind = sorted_quality_ind.pop(0)
      if((total_sum + self.weights[best_ind]) <= self.capacity):
        self.knapsack[best_ind] = 1
        total_sum += self.weights[best_ind]
      else:
        break
    return self.knapsack
