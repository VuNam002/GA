import random
import sys
import operator

class Knapsack(object): 

    # Khởi tạo các biến và danh sách
    def __init__(self): 

        self.C = 0
        self.weights = []
        self.profits = []
        self.opt = []
        self.parents = []
        self.newparents = []
        self.bests = []
        self.best_p = [] 
        self.iterated = 1
        self.population = 0

        # Tăng giới hạn đệ quy tối đa để tránh lỗi stack overflow
        iMaxStackSize = 15000
        sys.setrecursionlimit(iMaxStackSize)

    # Tạo dân số ban đầu 
    def initialize(self):
        for i in range(self.population):
            parent = []
            for _ in range(5):
                k = random.randint(0, 1)
                parent.append(k)
            self.parents.append(parent)

    # Đặt các thuộc tính của vấn đề
    def properties(self, weights, profits, opt, C, population):
        self.weights = weights
        self.profits = profits
        self.opt = opt
        self.C = C
        self.population = population
        self.initialize()

    # Tính hàm fitness của mỗi danh sách (balo)
    def fitness(self, item):
        sum_w = 0
        sum_p = 0

        # Lấy trọng lượng và lợi nhuận
        for index, i in enumerate(item):
            if i == 1:
                sum_w += self.weights[index]
                sum_p += self.profits[index]

        # Nếu tổng trọng lượng vượt quá giới hạn, trả về -1, ngược lại trả về tổng lợi nhuận
        if sum_w > self.C:
            return -1
        else: 
            return sum_p

    # Chạy các thế hệ của GA
    def evaluation(self):
        # Lặp qua các bậc cha mẹ và tính toán fitness
        best_pop = self.population // 2
        for parent in self.parents:
            ft = self.fitness(parent)
            self.bests.append((ft, parent))

        # Sắp xếp danh sách fitness theo giá trị
        self.bests.sort(key=operator.itemgetter(0), reverse=True)
        self.best_p = self.bests[:best_pop]
        self.best_p = [x[1] for x in self.best_p]

    # Đột biến các con sau một điều kiện nhất định
    def mutation(self, ch):
        for i in range(len(ch)):        
            k = random.uniform(0, 1)
            if k > 0.5:
                # Nếu số ngẫu nhiên lớn hơn 0.5, lật 0 thành 1 và ngược lại
                ch[i] = 1 - ch[i]
        return ch

    # Crossover hai cha mẹ để tạo ra hai con bằng cách trộn chúng
    def crossover(self, ch1, ch2):
        threshold = random.randint(1, len(ch1)-1)
        tmp1 = ch1[threshold:]
        tmp2 = ch2[threshold:]
        ch1 = ch1[:threshold]
        ch2 = ch2[:threshold]
        ch1.extend(tmp2)
        ch2.extend(tmp1)
        return ch1, ch2

    # Chạy thuật toán GA
    def run(self):
        # Chạy đánh giá một lần
        self.evaluation()
        newparents = []
        pop = len(self.best_p)

        # Tạo danh sách với các số nguyên ngẫu nhiên duy nhất
        sample = random.sample(range(pop), pop)
        for i in range(pop):
            # Chọn chỉ số ngẫu nhiên của các con tốt nhất để ngẫu nhiên hóa quá trình
            r1 = self.best_p[sample[i]]
            r2 = self.best_p[sample[(i+1) % pop]]
            nchild1, nchild2 = self.crossover(r1, r2)
            newparents.append(nchild1)
            newparents.append(nchild2)

        # Đột biến các con mới và các cha mẹ tiềm năng để đảm bảo tìm thấy giá trị toàn cục
        for i in range(len(newparents)):
            newparents[i] = self.mutation(newparents[i])

        if self.opt in newparents:
            print("Giải pháp tối ưu được tìm thấy sau {} thế hệ.".format(self.iterated))
        else:
            self.iterated += 1
            print("Tạo lại các thế hệ lần thứ {}.".format(self.iterated))
            self.parents = newparents
            self.bests = []
            self.best_p = []
            self.run()  

# Thuộc tính cho vấn đề cụ thể này
weights = [12,  7, 11, 8, 9]
profits = [24, 13, 23, 15, 16]
opt     = [0, 1, 1, 1, 0]
C = 26
population = 10

k = Knapsack()
k.properties(weights, profits, opt, C, population)
k.run()
