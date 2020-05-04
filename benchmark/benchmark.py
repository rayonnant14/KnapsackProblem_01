import sys
sys.path.append('../')
from algorithms import common
from algorithms import bnb
from algorithms import dynamic
from algorithms import genetic
from algorithms import greedy
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
import requests

def get_ans(profits, knapsack):
  ans = 0
  for i in range(len(profits)):
    ans += profits[i] * knapsack[i]
  return ans

def benchmark():
  base_url = 'https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p'
  filenames = []
  test_info_num_items = []
  test_info_capacity = []
  medians = []
  std = []
  medians_solutions = []
  std_solutions = []
  optimal_solutions = []
  for i in range(1, 8):
    greedy_time = []
    dynamic_time = []
    genetic_time = []
    bnb_time = []
    greedy_solution = []
    dynamic_solution = []
    genetic_solution = []
    bnb_solution = []
    c = requests.get(base_url + '0' + str(i) + '_c.txt')
    w = requests.get(base_url + '0' + str(i) + '_w.txt')
    p = requests.get(base_url + '0' + str(i) + '_p.txt')
    s = requests.get(base_url + '0' + str(i) + '_s.txt')
    filenames.append('knapsack_0' + str(i))

    kdct = {'capacity': c.text,
            'weights':  w.text,
            'profits':  p.text,
            'optimal':  s.text}
    kdct = {k: v.split('\n') for k, v in kdct.items()}
    kdct = {k: [int(x) for x in v if len(x)>0] for k, v in kdct.items()}
    test_info_num_items.append(len(kdct['profits']))
    test_info_capacity.append(kdct['capacity'][0])
    optimal_solutions.append(get_ans(kdct['profits'], kdct['optimal']))

    for j in range(10):

      start = datetime.now()
      g = greedy.Greedy(kdct['weights'], kdct['profits'], kdct['capacity'][0])
      knapsack = g.solve()
      end = datetime.now()
      greedy_time.append((end - start).total_seconds() * 1000)
      greedy_solution.append(get_ans(kdct['profits'], knapsack))

      start = datetime.now()
      d = dynamic.Dynamic(kdct['weights'], kdct['profits'], kdct['capacity'][0])
      knapsack = d.solve()
      end = datetime.now()
      dynamic_time.append((end - start).total_seconds() * 1000)
      dynamic_solution.append(get_ans(kdct['profits'], knapsack))

      start = datetime.now()
      gen = genetic.Genetic(kdct['weights'], kdct['profits'], kdct['capacity'][0],
                    int(len(kdct['profits'] ) * 0.9), int(len(kdct['profits']) * 1.9))
      knapsack = gen.solve()
      end = datetime.now()
      genetic_time.append((end - start).total_seconds() * 1000)
      genetic_solution.append(get_ans(kdct['profits'], knapsack))

      start = datetime.now()
      b = bnb.BnB_solver(kdct['weights'], kdct['profits'], kdct['capacity'][0])
      knapsack = b.solve()
      end = datetime.now()
      bnb_time.append((end - start).total_seconds() * 1000)
      bnb_solution.append(get_ans(kdct['profits'], knapsack))



    medians.append([np.median(greedy_time), np.median(dynamic_time),
                np.median(genetic_time), np.median(bnb_time)])

    std.append([np.std(greedy_time), np.std(dynamic_time),
            np.std(genetic_time), np.std(bnb_time)])

    medians_solutions.append([np.median(greedy_solution), np.median(dynamic_solution),
                np.median(genetic_solution), np.median(bnb_solution)])

    std_solutions.append([np.std(greedy_solution), np.std(dynamic_solution),
            np.std(genetic_solution), np.std(bnb_solution)])

  return (filenames, test_info_num_items, test_info_capacity,
          medians, std, medians_solutions, std_solutions, optimal_solutions)

def benchmark2(directory_task, directory_answer):
  filenames = []
  test_info_num_items = []
  test_info_capacity = []
  medians = []
  std = []
  medians_solutions = []
  std_solutions = []
  optimal_solutions = []
  filenames = os.listdir(directory_task)
  for filename in filenames:

    task_path = directory_task + filename
    answer_path = directory_answer + filename
    handle_task = open(task_path, 'r')
    handle_answer = open(answer_path, 'r')

    weights = []
    profits = []
    greedy_time = []
    dynamic_time = []
    genetic_time = []
    bnb_time = []
    greedy_solution = []
    dynamic_solution = []
    genetic_solution = []
    bnb_solution = []

    main_info = [int(x) for x in handle_task.readline().split()]
    capacity = main_info[1]
    test_info_num_items.append(main_info[0])
    test_info_capacity.append(capacity)

    for i in range(1, main_info[0] + 1):
        tmp = [int(x) for x in handle_task.readline().split()]
        profits.append(tmp[0])
        weights.append(tmp[1])
    optimal_solutions.append(int(handle_answer.readline()))
    for j in range(5):
      start = datetime.now()
      g = greedy.Greedy(weights, profits, capacity)
      knapsack = g.solve()
      end = datetime.now()
      greedy_time.append((end - start).total_seconds() * 1000)
      greedy_solution.append(get_ans(profits, knapsack))

      start = datetime.now()
      d = dynamic.Dynamic(weights, profits, capacity)
      knapsack = d.solve()
      end = datetime.now()
      dynamic_time.append((end - start).total_seconds() * 1000)
      dynamic_solution.append(get_ans(profits, knapsack))

      start = datetime.now()
      gen = genetic.Genetic(weights, profits, capacity,
                    int(len(profits) * 0.9), int(len(kdct['profits']) * 1.9))
      knapsack = gen.solve()
      end = datetime.now()
      genetic_time.append((end - start).total_seconds() * 1000)
      genetic_solution.append(get_ans(profits, knapsack))

      start = datetime.now()
      b = bnb.BnB_solver(weights, profits, capacity)
      knapsack = b.solve()
      end = datetime.now()
      bnb_time.append((end - start).total_seconds() * 1000)
      bnb_solution.append(get_ans(profits, knapsack))



    medians.append([np.median(greedy_time), np.median(dynamic_time),
                np.median(genetic_time), np.median(bnb_time)])

    std.append([np.std(greedy_time), np.std(dynamic_time),
            np.std(genetic_time), np.std(bnb_time)])

    medians_solutions.append([np.median(greedy_solution), np.median(dynamic_solution),
                np.median(genetic_solution), np.median(bnb_solution)])

    std_solutions.append([np.std(greedy_solution), np.std(dynamic_solution),
            np.std(genetic_solution), np.std(bnb_solution)])

  return (filenames, test_info_num_items, test_info_capacity,
          medians, std, medians_solutions, std_solutions, optimal_solutions)

def summary_info(filenames, medians, std):
  medians = np.array(medians).T.tolist()
  std = np.array(std).T.tolist()

  fig, ax = plt.subplots(figsize=(13, 9))

  labels = filenames

  x = np.arange(len(labels))
  width = 0.2


  rects1 = ax.bar(x, medians[:][0], width, label='Greedy', color = 'PaleVioletRed')
  rects2 = ax.bar(x + width, medians[:][1], width, label='Dynamic', color = 'Aquamarine')
  rects3 = ax.bar(x + (width * 2), medians[:][2], width, label='Genetic', color = 'LimeGreen')
  #rects4 = ax.bar(x + (width * 3), medians[:][3], width, label='Branch-and-Bound', color = 'MediumBlue')

  ax.set_ylabel('Median time in milliseconds', fontsize = 14)
  ax.set_title('Tests ', fontsize = 20)
  ax.set_xticks(x + width + width/2)
  ax.set_xticklabels(labels, fontsize = 8)
  ax.legend(fontsize = 14)

def get_report(filenames, test_info_num_items, test_info_capacity, medians, std, medians_solutions, std_solutions, optimal_solutions):

  for i in range(len(filenames)):
    test_data = {
                  'test name' : [filenames[i]],
                  'number of items' : [test_info_num_items[i]],
                  'capacity of knapsack': [test_info_capacity[i]]
                }
    df_data = pd.DataFrame (test_data, columns = ['test name', 'number of items',
                                                       'capacity of knapsack'])
    display(df_data)


    data = {
            'algorithm' : ['Greedy', 'Dynamic', 'Genetic', 'Branch-and-bound'],
            'median time': medians[i],
            'std time': std[i],
            'median solution': medians_solutions[i],
            'std solution' : std_solutions[i],
            'optimal solution' : optimal_solutions[i]
           }

    df = pd.DataFrame (data, columns = ['algorithm', 'median time', 'std time',
                                        'median solution', 'std solution', 'optimal solution'])

    display(df)

    print("\n\n\n\n")

  summary_info(filenames, medians, std)
