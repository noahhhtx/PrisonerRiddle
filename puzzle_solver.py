import random
import numpy as np
import matplotlib.pyplot as plt

def computeSuboptimalProbability(n):
    return 100 * np.power(0.5,n)
def computeOptimalProbability(n):
    max_attempts = int(1.0 * n / 2)
    sum = 0
    for i in range(max_attempts+1, n+1):
        sum += (1.0 / i)
    probability = 100 * (1 - sum)
    return round(probability, 4)

def createGraph(n):
    nums = [x for x in range(1, n+1)]
    random.shuffle(nums)
    graph = {}
    for i in range(1, n+1):
        graph[i] = nums[i-1]
    return graph

def prisonerAttempt(graph, i, n):
    max_attempts = int(1.0 * n / 2)
    num = i
    for k in range(max_attempts):
        num = graph[num]
        if num == i:
            return True
    return False

def solve(graph, n):
    for i in range(1, n+1):
        attempt = prisonerAttempt(graph, i, n)
        if not attempt:
            return False
    return True

def simulation(n, x):
    results = []
    cumulative_sum = 0
    for i in range(x):
        graph = createGraph(n)
        if solve(graph, n):
            cumulative_sum += 1
        results.append(round(100.0 * cumulative_sum / (i+1), 4))
    return results
'''
n = 100
k = 10000
suboptimal_prob = computeSuboptimalProbability(n)
print(suboptimal_prob)
prob = computeOptimalProbability(n)
print(prob)

simulations = [x for x in range(1,k+1)]
results = simulation(n, k)
print(results[-1])

plt.axhline(prob, color="red")
plt.plot(simulations, results)
plt.xlabel("Number of Simulations")
plt.ylabel("Success Rate")
plt.show()
'''