class BnB_solver:
  def __init__(self, weights, profits, capacity):
    if (len(weights) != len(profits)):
      raise TypeError("Error! Size of weights not equal size of profits!")
    self.weights = weights
    self.profits = profits
    self.capacity = capacity
    self.num_items = len(weights)
    self.knapsack = []

  def solve(self):
    bounds = [[0, 1]] * (self.num_items)
    z, solution = self.BnB(bounds)
    self.knapsack = solution
    return self.knapsack

  def BnB(self, bounds, low_bound = 0.0, optimal_solution = []):
    z = [-i for i in self.profits]
    solution = linprog(z, A_ub = [self.weights], b_ub = [self.capacity],
                      bounds = bounds,
                      method = 'revised simplex')
    x = solution.x
    ans = -solution.fun
    if((not solution.success) or (low_bound >= ans)):
      return (0, [])

    sorted_x = sorted(range(self.num_items),  key=lambda i:x[i], reverse=True)
    find_int_solution = True

    for i in sorted_x:
      if((x[i] < 1.0) and (x[i] > 0.0)):
        find_int_solution = False
        bounds[i] = [0, 0]
        new_bound, new_solution = self.BnB(bounds, low_bound, optimal_solution)
        if(new_bound):
          low_bound = new_bound
          optimal_solution = new_solution

        bounds[i] = [1, 1]
        new_bound, new_solution = self.BnB(bounds, low_bound, optimal_solution)
        if(new_bound):
          low_bound = new_bound
          optimal_solution = new_solution

        bounds[i] = [0, 1]

    if(find_int_solution):
      low_bound = ans
      optimal_solution = x

    return (low_bound, optimal_solution)
