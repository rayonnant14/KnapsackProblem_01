class Dynamic:
  def __init__(self, weights, profits, capacity):
    if (len(weights) != len(profits)):
      raise TypeError("Error! Size of weights not equal size of profits!")
    self.weights = weights
    self.profits = profits
    self.capacity = capacity
    self.num_items = len(weights)
    self.knapsack = [0] * self.num_items

  def solve(self):
    m = self.dynamic()
    k = self.capacity
    for i in range(self.num_items, 0, -1):
        if m[i][k] != m[i - 1][k]:
            self.knapsack[i - 1] = 1
            k -= self.weights[i - 1]
    return self.knapsack

  def dynamic(self):
    m = [[0] * (self.capacity + 1) for i in range(self.num_items + 1)]
    for i in range(1, (self.num_items + 1)):
        for j in range(0, (self.capacity + 1)):
            if (self.weights[i - 1] > j):
                m[i][j] = m[i - 1][j]
            else:
                m[i][j] = max(m[i - 1][j], (m[i - 1][j - self.weights[i - 1]] + self.profits[i - 1]))

    return m
