# algorithms/aco.py

import random
import math
from wb.wb import WB  # type: ignore # Import lớp WB từ WB.py

class Ant:
    def __init__(self, cargo_list):
        # Deep copy để tránh thay đổi dữ liệu gốc
        self.cargo_list = [cargo.copy() for cargo in cargo_list]
        self.loaded_cargoes = []             # Danh sách hàng hóa đã xếp
        self.current_solution = []           # Kế hoạch xếp hàng hiện tại

    def load_cargo(self, cargo, wb):
        for c in self.cargo_list:
            if c['id'] == cargo['id']:
                self.loaded_cargoes.append(c.copy())
                wb.loaded_cargoes.append(c.copy())  # Thêm hàng hóa vào danh sách đã xếp của WB
                self.cargo_list.remove(c)  # Xóa hàng hóa khỏi danh sách của kiến
                break
            
    def remove_cargo(self, cargo):
        for c in self.cargo_list:
            if c['id'] == cargo['id']:
                self.cargo_list.remove(c)  # Xóa hàng hóa khỏi danh sách của kiến
                break

class ACO:
    def __init__(self, cargo_list, container_dimensions, params):
        self.original_cargo_list = cargo_list  # Giữ nguyên danh sách hàng hóa ban đầu
        self.cargo_list = cargo_list.copy()    # Danh sách hàng hóa hiện tại
        self.container_dimensions = container_dimensions  # Kích thước container
        self.num_ants = params['num_ants']    # Số lượng kiến
        self.num_iterations = params['num_iterations']  # Số lần lặp
        self.alpha_values = params['alpha_values']  # Giá trị alpha
        self.beta_values = params['beta_values']    # Giá trị beta
        self.rho = params['rho']              # Hệ số bay hơi pheromone
        self.Q = params['Q']                  # Hệ số tăng cường pheromone
        self.tau = {}                         # Lượng pheromone
        self.best_solution = None
        self.best_utilization = 0
        self.load_capacity = params['load_capacity']    # Trọng tải tối đa
        self.volume_capacity = params['volume_capacity']  # Thể tích container
        self.initialize_pheromones()
    
    def initialize_pheromones(self):
        # Khởi tạo lượng pheromone giữa các hàng hóa
        for cargo_i in self.original_cargo_list:
            for cargo_j in self.original_cargo_list:
                if (cargo_i['id'] != cargo_j['id']):
                    self.tau[(cargo_i['id'], cargo_j['id'])] = 1.0  # Pheromone ban đầu
    
    def run(self):
        number_cagos_loaded = 0
        for iteration in range(self.num_iterations):
            ants = [Ant(self.original_cargo_list) for _ in range(self.num_ants)]
            # Lấy giá trị alpha và beta cho lần lặp hiện tại
            idx = iteration % len(self.alpha_values)
            alpha = self.alpha_values[idx]
            beta = self.beta_values[idx]
            for ant in ants:
                self.construct_solution(ant, alpha, beta)
                utilization, num_cargo = self.evaluate_solution(ant)
                if utilization > self.best_utilization:
                    number_cagos_loaded = num_cargo
                    self.best_utilization = utilization
                    self.best_solution = ant.current_solution.copy()
            self.update_pheromones()
            print(f"Iteration {iteration+1}/{self.num_iterations}, Best Utilization: {self.best_utilization:.3f}")
        return self.best_solution, self.best_utilization, number_cagos_loaded
    
    def construct_solution(self, ant, alpha, beta):
        wb = WB(self.container_dimensions, [])
        # Chọn hàng hóa tham chiếu ngẫu nhiên từ cargo_list
        if not ant.cargo_list:
            return
        current_cargo = random.choice(ant.cargo_list)
        # Thiết lập vị trí ban đầu của hàng hóa
        current_cargo['x'], current_cargo['y'], current_cargo['z'] = 0, 0, 0  # Vị trí ban đầu là (0, 0, 0)

        while ant.cargo_list:
            next_cargo = self.select_next_cargo(ant, current_cargo, alpha, beta)
            if next_cargo is None:
                break
            # Kiểm tra ràng buộc trước khi xếp
            if self.can_load(ant, next_cargo):
                wb.cargo_list = [next_cargo]
                wb.load_cargo()
                if wb.loaded_cargoes:
                    # Cập nhật cho kế hoạch của 'kiến'
                    ant.current_solution.append(next_cargo)
                    # Tải và cập nhật hàng hóa 
                    ant.load_cargo(next_cargo, wb) # vị trí của hàng hóa sẽ gián tiếp được cập nhật ở đây
                    current_cargo = next_cargo
                else:
                    ant.remove_cargo(next_cargo)
            else:
                ant.remove_cargo(next_cargo)

    
    def select_next_cargo(self, ant, current_cargo, alpha, beta):
        probabilities = []
        denom = 0.0
        for cargo in ant.cargo_list:
            tau = self.tau.get((current_cargo['id'], cargo['id']), 1.0)
            eta = self.calculate_eta(current_cargo, cargo)
            prob = (tau ** alpha) * (eta ** beta)
            probabilities.append((cargo, prob))
            denom += prob
        if denom == 0:
            return None
        # Chuẩn hóa xác suất
        probabilities = [(cargo, prob / denom) for cargo, prob in probabilities]
        # Lựa chọn dựa trên xác suất
        rand = random.random()
        cumulative = 0.0
        for cargo, prob in probabilities:
            cumulative += prob
            if rand <= cumulative:
                return cargo
        return None
    
    def calculate_eta(self, current_cargo, next_cargo):
        # Hàm heuristic, có thể điều chỉnh theo bài toán
        # Dựa trên bài báo: đặt trọng lượng, thể tích và kích thước nhỏ nhất
        v_j = next_cargo['volume']
        g_j = next_cargo['weight']
        min_size_j = min(next_cargo['length'], next_cargo['width'], next_cargo['height'])
        dz_j = next_cargo['height']  # Giả định dz(j) là chiều cao
        eta = (v_j * g_j * min_size_j) / (dz_j ** 2)
        return eta
    
    def can_load(self, ant, cargo):
        # Kiểm tra ràng buộc trọng lượng và thể tích
        total_weight = sum(c['weight'] for c in ant.loaded_cargoes) + cargo['weight']
        total_volume = sum(c['volume'] for c in ant.loaded_cargoes) + cargo['volume']
        if total_weight > self.load_capacity or total_volume > self.volume_capacity:
            return False
        return True
    
    def evaluate_solution(self, ant):
        total_volume = 0
        count_cago = 0
        for c in ant.current_solution:
            if c['x'] == 0  and c['y'] == 0 and c['z'] == 0:
                continue
            else:
                if total_volume + c['volume'] <= self.volume_capacity:
                    total_volume += c['volume']
                    count_cago += 1
                else:
                    break
        utilization = total_volume / self.volume_capacity
        return [utilization * 100, count_cago]

    
    def update_pheromones(self):
        # Bay hơi pheromone
        for key in self.tau:
            self.tau[key] *= (1 - self.rho)
            if self.tau[key] < 1e-6:
                self.tau[key] = 1e-6  # Giới hạn pheromone nhỏ nhất
        # Tăng cường pheromone dựa trên giải pháp tốt nhất
        if self.best_solution:
            delta_tau = self.Q * self.best_utilization
            for i in range(len(self.best_solution) - 1):
                cargo_i = self.best_solution[i]
                cargo_j = self.best_solution[i + 1]
                key = (cargo_i['id'], cargo_j['id'])
                if key in self.tau:
                    self.tau[key] += delta_tau
                else:
                    # Nếu key chưa tồn tại, tạo nó
                    self.tau[key] = delta_tau

