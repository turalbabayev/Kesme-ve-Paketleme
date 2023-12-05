import random
import matplotlib.pyplot as plt
import math

class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height
        self.x = -1
        self.y = -1
        self.rotated = False

class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.triangles = []
        self.fitness = 0

    def add_triangle(self, triangle):
        self.triangles.append(triangle)
        self.fitness += 0.5 * triangle.base * triangle.height

def is_valid_location(bin, tri, x, y):
    if x + tri.base > bin.width or y + tri.height > bin.height:
        return False
    for t in bin.triangles:
        if (x < t.x + t.base and x + tri.base > t.x and
            y < t.y + t.height and y + tri.height > t.y):
            return False
    return True

def pack_triangles(triangles, bin_width, bin_height):
    bins = [Bin(bin_width, bin_height)]

    for tri in triangles:
        fitted = False
        for bin in bins:
            for y in range(bin.height):
                for x in range(bin.width):
                    if is_valid_location(bin, tri, x, y):
                        tri.x = x
                        tri.y = y
                        bin.add_triangle(tri)
                        fitted = True
                        break
                if fitted:
                    break
            if fitted:
                break

    return bins

def visualize_packing(bins):
    plt.figure()
    colors = ['#FF5733', '#33FF57', '#5733FF', '#FF57D5', '#33A6FF', "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFA500", "#FFC0CB", "#800080", "#40E0D0", "#808080", "#A52A2A", "#FFD700", "#E6E6FA"]

    for i, bin in enumerate(bins):
        plt.subplot(1, len(bins), i + 1)
        plt.title(f'Bin {i + 1}')
        for j, tri in enumerate(bin.triangles):
            color = colors[j % len(colors)]
            plt.gca().add_patch(plt.Polygon([(tri.x, tri.y), (tri.x + tri.base, tri.y), (tri.x + tri.base, tri.y + tri.height)], fill=True, color=color))

        for x in range(bin.width):
            for y in range(bin.height):
                is_empty = True
                for tri in bin.triangles:
                    if x >= tri.x and x < tri.x + tri.base and y >= tri.y and y < tri.y + tri.height:
                        is_empty = False
                        break
                if is_empty:
                    plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='black'))

        plt.xlim(0, bin.width)
        plt.ylim(0, bin.height)

    plt.show()

def create_chromosome(triangles):
    chromosome = []
    for i in range(len(triangles)):
        chromosome.append(i)
    random.shuffle(chromosome)
    for i in range(len(triangles)):
        chromosome.append(random.randint(0, 1))
    return chromosome

def create_population(triangles, population_size):
    population = []
    for i in range(population_size):
        population.append(create_chromosome(triangles))
    return population

def decode_chromosome(chromosome, triangles):
    decoded_triangles = []
    for i in range(len(triangles)):
        index = chromosome[i]
        rotation = chromosome[i + len(triangles)]
        base = triangles[index].base
        height = triangles[index].height
        decoded_triangles.append(Triangle(base, height))
        decoded_triangles[i].rotated = rotation
    return decoded_triangles

def evaluate_population(population, triangles, bin_width, bin_height):
    evaluated_population = []
    for chromosome in population:
        decoded_triangles = decode_chromosome(chromosome, triangles)
        bins = pack_triangles(decoded_triangles, bin_width, bin_height)
        fitness = bins[0].fitness
        evaluated_population.append((chromosome, fitness))
    return evaluated_population

def select_population(evaluated_population, population_size):
    selected_population = []
    total_fitness = sum(fitness for chromosome, fitness in evaluated_population)
    probabilities = [fitness / total_fitness for chromosome, fitness in evaluated_population]
    for i in range(population_size):
        r = random.random()
        s = 0
        for j in range(len(evaluated_population)):
            s += probabilities[j]
            if r < s:
                selected_population.append(evaluated_population[j][0])
                break
    return selected_population

def crossover_population(population, crossover_rate):
    crossed_population = []
    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i + 1]
        child1 = parent1.copy()
        child2 = parent2.copy()
        r = random.random()
        if r < crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            child1[:point] = parent2[:point]
            child2[:point] = parent1[:point]
        crossed_population.append(child1)
        crossed_population.append(child2)
    return crossed_population

def mutate_population(population, mutation_rate):
    mutated_population = []
    for chromosome in population:
        mutated_chromosome = chromosome.copy()
        r = random.random()
        if r < mutation_rate:
            point = random.randint(0, len(chromosome) - 1)
            if point < len(chromosome) // 2:
                swap = random.randint(0, len(chromosome) // 2 - 1)
                mutated_chromosome[point], mutated_chromosome[swap] = mutated_chromosome[swap], mutated_chromosome[point]
            else:
                mutated_chromosome[point] = 1 - mutated_chromosome[point]
        mutated_population.append(mutated_chromosome)
    return mutated_population

def genetic_algorithm(triangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate):
    population = create_population(triangles, population_size)
    best_chromosome = None
    best_fitness = 0
    for i in range(iteration):
        evaluated_population = evaluate_population(population, triangles, bin_width, bin_height)
        for chromosome, fitness in evaluated_population:
            if fitness > best_fitness:
                best_chromosome = chromosome
                best_fitness = fitness
        selected_population = select_population(evaluated_population, population_size)
        crossed_population = crossover_population(selected_population, crossover_rate)
        mutated_population = mutate_population(crossed_population, mutation_rate)
        population = mutated_population

        print(f"Iteration {i + 1} - Best fitness: {best_fitness}")
    print("Best chromosome:", best_chromosome)
    print("Best fitness value:", best_fitness)
    return best_chromosome, best_fitness

if __name__ == "__main__":
    triangles = []
    with open("Data/C2_1_triangles.txt", "r") as file:
        num_triangles = int(file.readline().strip())
        bin_width, bin_height = map(int, file.readline().strip().split())

        for _ in range(num_triangles):
            base, height = map(int, file.readline().strip().split())
            triangles.append(Triangle(base, height))

    population_size = 10
    iteration = 50
    crossover_rate = 0.8
    mutation_rate = 0.1

    best_chromosome, best_fitness = genetic_algorithm(triangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate)
    best_triangles = decode_chromosome(best_chromosome, triangles)
    best_bins = pack_triangles(best_triangles, bin_width, bin_height)

    total_triangles_area = sum(0.5 * tri.base * tri.height for tri in triangles)
    total_packing_area = bin_width * bin_height
    total_fitted_area = sum(0.5 * tri.base * tri.height for bin in best_bins for tri in bin.triangles)
    success_rate = (total_fitted_area / total_triangles_area) * 100
    plt.suptitle(f'Triangle Data\nSuccess Rate: {success_rate}%', fontsize=14)
    visualize_packing(best_bins)
