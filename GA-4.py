import random

# Hàm sinh giá trị ngẫu nhiên (0 hoặc 1)
def generate_random_value():
    return random.randint(0, 1)

# Hàm tạo cá thể (chromosome) với số lượng vật phẩm n_items
def create_individual(n_items):
    return [generate_random_value() for _ in range(n_items)]

# Hàm tính toán độ thích nghi (fitness) của một cá thể
def compute_fitness(chromosome, values, weights, max_weight):
    value = sum([chromosome[i] * values[i] for i in range(len(chromosome))])
    weight = sum([chromosome[i] * weights[i] for i in range(len(chromosome))])
    if weight > max_weight:
        return 0
    else:
        return value

# Hàm tính toán tổng trọng lượng của một cá thể
def compute_weight(chromosome, weights):
    return sum([chromosome[i] * weights[i] for i in range(len(chromosome))])

# Hàm chọn lọc các cá thể tốt nhất (phụ thuộc vào độ thích nghi)
def selection(population, fitness_scores):
    selected_chromosomes = []
    population_size = len(population)
    for i in range(population_size // 2):
        max_fitness_index = fitness_scores.index(max(fitness_scores))
        selected_chromosomes.append(population[max_fitness_index])
        fitness_scores[max_fitness_index] = 0
    return selected_chromosomes

# Hàm lai ghép (crossover) giữa hai cá thể cha mẹ
def crossover(parent1, parent2):
    split_index = random.randint(1, len(parent1)-1)
    child1 = parent1[:split_index] + parent2[split_index:]
    child2 = parent2[:split_index] + parent1[split_index:]
    return child1, child2

# Hàm đột biến (mutation) trên một cá thể với tỉ lệ đột biến mutation_rate
def mutate(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.uniform(0, 1) < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# Hàm thuật toán di truyền để giải bài toán knapsack
def genetic_algorithm(n_items, values, weights, max_weight, population_size=100, generations=100, mutation_rate=0.1):
    # Tạo dân số ban đầu
    population = [create_individual(n_items) for i in range(population_size)]

    # Chạy thuật toán di truyền qua các thế hệ
    for generation in range(generations):
        # Tính toán độ thích nghi của mỗi cá thể trong dân số
        fitness_scores = [compute_fitness(chromosome, values, weights, max_weight) for chromosome in population]

        # Chọn lọc các cá thể tốt nhất để sinh sản
        selected_chromosomes = selection(population, fitness_scores)

        # Lai ghép các cá thể đã chọn để tạo ra thế hệ con mới
        offspring = []
        for i in range(population_size // 2):
            parent1 = selected_chromosomes[random.randint(0, len(selected_chromosomes)-1)]
            parent2 = selected_chromosomes[random.randint(0, len(selected_chromosomes)-1)]
            child1, child2 = crossover(parent1, parent2)
            offspring.extend([child1, child2])

        # Đột biến thế hệ con
        for i in range(len(offspring)):
            offspring[i] = mutate(offspring[i], mutation_rate)

        # Thay thế dân số cũ bằng thế hệ con mới
        population = offspring

    # Tìm cá thể có độ thích nghi cao nhất
    best_chromosome = population[0]
    best_fitness_score = compute_fitness(best_chromosome, values, weights, max_weight)
    for chromosome in population:
        fitness_score = compute_fitness(chromosome, values, weights, max_weight)
        if fitness_score > best_fitness_score:
            best_chromosome = chromosome
            best_fitness_score = fitness_score

    # Trả về kết quả
    selected_items = [i+1 for i in range(n_items) if best_chromosome[i] == 1]
    solution = {
        'items': selected_items,
        'value': best_fitness_score,
        'weight': compute_weight(best_chromosome, weights)
    }
    return solution

# Hàm nhập dữ liệu từ bàn phím
def input_data():
    n_items = int(input("Nhập số lượng vật phẩm: "))
    values = [int(x) for x in input("Nhập giá trị của từng vật phẩm (cách nhau bằng dấu phẩy): ").split(',')]
    weights = [int(x) for x in input("Nhập trọng lượng của từng vật phẩm (cách nhau bằng dấu phẩy): ").split(',')]
    max_weight = int(input("Nhập trọng lượng tối đa của balo: "))
    return n_items, values, weights, max_weight

# Chạy chương trình với dữ liệu nhập từ bàn phím
if __name__ == '__main__':
    n_items, values, weights, max_weight = input_data()
    solution = genetic_algorithm(n_items, values, weights, max_weight)
    print("Các vật phẩm được chọn:", solution['items'])
    print("Tổng giá trị:", solution['value'])
    print("Tổng trọng lượng:", solution['weight'])
