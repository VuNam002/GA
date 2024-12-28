import random
from typing import List

# Lớp Item biểu diễn một vật phẩm với tên, trọng lượng và giá trị
class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

# Lớp Individual biểu diễn một cá thể trong thuật toán di truyền
class Individual:
    def __init__(self, bits: List[int]):
        self.bits = bits
    
    def __str__(self):
        return repr(self.bits)

    def __hash__(self):
        return hash(str(self.bits))
    
    # Hàm fitness tính toán giá trị tổng và kiểm tra trọng lượng
    def fitness(self) -> float:
        total_value = sum([
            bit * item.value
            for item, bit in zip(items, self.bits)
        ])

        total_weight = sum([
            bit * item.weight
            for item, bit in zip(items, self.bits)
        ])

        # Nếu trọng lượng không vượt quá giới hạn, trả về giá trị tổng
        if total_weight <= MAX_KNAPSACK_WEIGHT:
            return total_value
        
        # Nếu trọng lượng vượt quá giới hạn, trả về 0
        return 0

# Các hằng số cho bài toán
MAX_KNAPSACK_WEIGHT = 15 #giá trị max trong lượng của cái túi
CROSSOVER_RATE = 0.53   #Bắt đầu cho giá trị trung bình trong lai ghép
MUTATION_RATE = 0.013   #Giá trị nhỏ nhất cho đột biến
REPRODUCTION_RATE = 0.15  #Giá trị trung bình cho tái tạo

# Danh sách các vật phẩm
items = [
    Item("A", 7, 5),
    Item("B", 2, 4),
    Item("C", 1, 7),
    Item("D", 9, 2)
]

# Tạo dân số ban đầu
def generate_initial_population(count=6) -> List[Individual]:
    population = set()

    # Tạo dân số ban đầu với số lượng cá thể là `count`
    while len(population) != count:
        # Chọn ngẫu nhiên các bit cho từng vật phẩm và tạo cá thể mới
        bits = [
            random.choice([0, 1])
            for _ in items
        ]
        population.add(Individual(bits))

    return list(population)

# Chọn lọc các cá thể có fitness cao nhất
def selection(population: List[Individual]) -> List[Individual]:
    parents = []
    
    # Xáo trộn ngẫu nhiên dân số
    random.shuffle(population)

    # Sử dụng 4 cá thể đầu tiên để tìm 2 cha mẹ phù hợp nhất
    # Thực hiện giải đấu giữa các cặp cá thể
    if population[0].fitness() > population[1].fitness():
        parents.append(population[0])
    else:
        parents.append(population[1])
    
    if population[2].fitness() > population[3].fitness():
        parents.append(population[2])
    else:
        parents.append(population[3])

    return parents

# Thực hiện lai ghép (crossover) giữa hai cha mẹ
def crossover(parents: List[Individual]) -> List[Individual]:
    N = len(items)

    child1 = parents[0].bits[:N//2] + parents[1].bits[N//2:]
    child2 = parents[0].bits[N//2:] + parents[1].bits[:N//2]

    return [Individual(child1), Individual(child2)]

# Thực hiện đột biến (mutation) trên các cá thể
def mutate(individuals: List[Individual]) -> List[Individual]:
    for individual in individuals:
        for i in range(len(individual.bits)):
            if random.random() < MUTATION_RATE:
                # Lật bit (flip the bit)
                individual.bits[i] = 1 - individual.bits[i]

# Tạo thế hệ tiếp theo
def next_generation(population: List[Individual]) -> List[Individual]:
    next_gen = []
    while len(next_gen) < len(population):
        children = []

        # Chọn lọc và lấy cha mẹ
        parents = selection(population)

        # Tái tạo (reproduction)
        if random.random() < REPRODUCTION_RATE:
            children = parents
        else:
            # Thực hiện lai ghép (crossover)
            if random.random() < CROSSOVER_RATE:
                children = crossover(parents)
            
            # Thực hiện đột biến (mutation)
            if random.random() < MUTATION_RATE:
                mutate(children)

        next_gen.extend(children)

    return next_gen[:len(population)]

# In thông tin thế hệ
def print_generation(population: List[Individual]):
    for individual in population:
        print(individual.bits, individual.fitness())
    print()
    print("Độ thích nghi trung bình:", sum([x.fitness() for x in population])/len(population))
    print("-" * 32)

# Tính độ thích nghi trung bình của dân số
def average_fitness(population: List[Individual]) -> float:
    return sum([i.fitness() for i in population]) / len(population)

# Giải bài toán knapsack
def solve_knapsack() -> Individual:
    population = generate_initial_population()

    avg_fitnesses = []

    for _ in range(500):
        avg_fitnesses.append(average_fitness(population))
        population = next_generation(population)

    population = sorted(population, key=lambda i: i.fitness(), reverse=True)
    return population[0]

# Chạy chương trình
if __name__ == '__main__':
    solution = solve_knapsack()
    print(solution, solution.fitness())
