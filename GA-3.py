import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import ga1

class KnapsackProblem(QWidget):
    def __init__(self):
        super().__init__()

        # Tạo các phần tử giao diện người dùng
        self.items_label = QLabel('Số lượng vật phẩm:')
        self.items_input = QLineEdit()
        self.values_label = QLabel('Giá trị (cách nhau bằng dấu phẩy):')
        self.values_input = QLineEdit()
        self.weights_label = QLabel('Trọng lượng (cách nhau bằng dấu phẩy):')
        self.weights_input = QLineEdit()
        self.max_weight_label = QLabel('Trọng lượng tối đa:')
        self.max_weight_input = QLineEdit()
        self.run_button = QPushButton('Chạy')
        self.solution_label = QLabel()

        # Sắp xếp các phần tử giao diện người dùng
        layout = QVBoxLayout()
        layout.addWidget(self.items_label)
        layout.addWidget(self.items_input)
        layout.addWidget(self.values_label)
        layout.addWidget(self.values_input)
        layout.addWidget(self.weights_label)
        layout.addWidget(self.weights_input)
        layout.addWidget(self.max_weight_label)
        layout.addWidget(self.max_weight_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.solution_label)
        self.setLayout(layout)

        # Kết nối nút chạy với thuật toán di truyền
        self.run_button.clicked.connect(self.run_genetic_algorithm)

    def run_genetic_algorithm(self):
        try:
            # Lấy dữ liệu đầu vào từ giao diện người dùng
            n_items = int(self.items_input.text())
            values = [int(val) for val in self.values_input.text().split(',')]
            weights = [int(wt) for wt in self.weights_input.text().split(',')]
            max_weight = int(self.max_weight_input.text())

            # Kiểm tra tính hợp lệ của đầu vào
            if len(values) != n_items or len(weights) != n_items:
                self.solution_label.setText('Số lượng giá trị và trọng lượng phải khớp với số lượng vật phẩm.')
                return

            # Chạy thuật toán di truyền
            solution = ga1.genetic_algorithm(n_items, values, weights, max_weight)

            # Hiển thị giải pháp
            self.solution_label.setText('Các vật phẩm được chọn: {}\nTổng giá trị: {}\nTổng trọng lượng: {}'.format(solution['items'], solution['value'], solution['weight']))

        except Exception as e:
            self.solution_label.setText(f'Lỗi: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    knapsack_problem = KnapsackProblem()
    knapsack_problem.show()
    sys.exit(app.exec_())
