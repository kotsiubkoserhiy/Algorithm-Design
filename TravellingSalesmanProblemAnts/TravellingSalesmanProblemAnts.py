import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt


class TravellingSalesmanProblem:
    def __init__(self, num_vertices, alpha, beta, rho, ants, iterations, report_interval):
        self.num_vertices = num_vertices
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.ants = ants
        self.iterations = iterations
        self.report_interval = report_interval
        self.distance_matrix = self.generate_distance_matrix()
        self.Lmin, _ = self.greedy_algorithm()
        self.pheromone_matrix = self.initialize_pheromone_matrix(self.Lmin)

    def generate_distance_matrix(self):
        matrix = np.random.randint(1, 51, size=(self.num_vertices, self.num_vertices)).astype(float)
        np.fill_diagonal(matrix, np.inf)
        return matrix

    def greedy_algorithm(self, start=0):
        visited = np.zeros(self.num_vertices, dtype=bool)
        visited[start] = True
        path_length = 0
        path = [start]

        for _ in range(self.num_vertices - 1):
            last = path[-1]
            next_city = np.argmin(np.where(visited, np.inf, self.distance_matrix[last]))
            path_length += self.distance_matrix[last, next_city]
            path.append(next_city)
            visited[next_city] = True

        path_length += self.distance_matrix[path[-1], path[0]]
        return path_length, path

    def initialize_pheromone_matrix(self, Lmin):
        return np.ones((self.num_vertices, self.num_vertices)) / Lmin

    def update_pheromone(self, paths):
        self.pheromone_matrix *= (1 - self.rho)
        for path, path_length in paths:
            for i in range(self.num_vertices - 1):
                self.pheromone_matrix[path[i], path[i + 1]] += self.Lmin / path_length
            self.pheromone_matrix[path[-1], path[0]] += self.Lmin / path_length

    def select_next_city(self, current_city, visited):
        pheromones = self.pheromone_matrix[current_city][~visited] ** self.alpha
        visibility = (1. / (self.distance_matrix[current_city][~visited] + 1e-10)) ** self.beta
        probabilities = pheromones * visibility
        probabilities /= probabilities.sum()
        return choice(np.where(~visited)[0], p=probabilities)

    def get_iterations(self):
        while True:
            try:
                iterations = int(input("Enter the number of iterations (>1): "))
                if iterations > 1:
                    return iterations
                else:
                    print("Please enter a positive integer (>1).")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def run(self):
        quality_over_time = []

        for iteration in range(self.iterations):
            paths = []
            for ant in range(self.ants):
                start = np.random.randint(self.num_vertices)
                visited = np.zeros(self.num_vertices, dtype=bool)
                visited[start] = True
                path = [start]
                path_length = 0

                while not visited.all():
                    next_city = self.select_next_city(path[-1], visited)
                    path_length += self.distance_matrix[path[-1], next_city]
                    path.append(next_city)
                    visited[next_city] = True

                path_length += self.distance_matrix[path[-1], path[0]]
                paths.append((path, path_length))

            self.update_pheromone(paths)

            best_path_length = min(path_length for _, path_length in paths)
            if iteration % self.report_interval == 0 or iteration == self.iterations - 1:
                quality_over_time.append(best_path_length)
                print(f"Iteration {iteration}; Best path length = {best_path_length}")

        x_values = list(range(0, self.iterations, self.report_interval)) + [self.iterations]
        plt.plot(x_values, quality_over_time)
        plt.xlabel('Iteration')
        plt.ylabel('Best path length')
        plt.title('Dependence of the solution quality on the number of iterations')
        plt.grid(True)
        plt.show()

