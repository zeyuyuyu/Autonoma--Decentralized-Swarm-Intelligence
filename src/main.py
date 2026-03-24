import numpy as np
import random

class SwarmOptimizer:
    def __init__(self, population_size, dim, bounds, max_iterations):
        self.population_size = population_size
        self.dim = dim
        self.bounds = bounds
        self.max_iterations = max_iterations
        self.population = self.initialize_population()
        self.pbest = self.population.copy()
        self.gbest = self.population[0].copy()
        self.fitness = self.evaluate_fitness()

    def initialize_population(self):
        population = np.random.uniform(self.bounds[:, 0], self.bounds[:, 1], (self.population_size, self.dim))
        return population

    def evaluate_fitness(self):
        fitness = np.apply_along_axis(self.objective_function, axis=1, arr=self.population)
        return fitness

    def objective_function(self, x):
        # Define your objective function here
        return np.sum(x ** 2)

    def update_positions(self, w, c1, c2):
        r1 = np.random.rand(self.population_size, self.dim)
        r2 = np.random.rand(self.population_size, self.dim)

        velocity = w * self.population + c1 * r1 * (self.pbest - self.population) + c2 * r2 * (self.gbest - self.population)
        self.population = self.population + velocity
        self.population = np.clip(self.population, self.bounds[:, 0], self.bounds[:, 1])

    def update_personal_best(self):
        new_fitness = self.evaluate_fitness()
        self.pbest[new_fitness < self.fitness] = self.population[new_fitness < self.fitness]
        self.fitness = new_fitness

    def update_global_best(self):
        best_idx = np.argmin(self.fitness)
        self.gbest = self.population[best_idx].copy()

    def optimize(self):
        for i in range(self.max_iterations):
            self.update_positions(0.8, 2, 2)
            self.update_personal_best()
            self.update_global_best()

        return self.gbest

# Example usage
bounds = np.array([[-10, 10], [-10, 10]])
optimizer = SwarmOptimizer(population_size=50, dim=2, bounds=bounds, max_iterations=1000)
best_solution = optimizer.optimize()
print(f'Best solution: {best_solution}')