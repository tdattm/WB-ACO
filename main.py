# main.py

from algorithms.aco import ACO
from processing_data.create_box import create_boxes_from_file
import matplotlib.pyplot as plt
import random
import pandas as pd

# Dữ liệu tối ưu được lưu lại sau nhiều lần chạy
data = {(5, 2): 77.7, (10, 2): 77.56, (15, 2): 78.36 , (25, 2): 77.65, (50,2):78.16, (100, 2): 78.75, 
        (5, 5): 77.71, (10, 5): 78.04,(15, 5): 78.3, (25, 5): 78.5, (50, 5): 78.8, (100, 5): 79.21}

def plot_container(container_dimensions, loaded_cargos, best_utilization, number_cagos_loaded, num_ants, num_iterations):
    # Tạo figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Kích thước container
    container_length, container_width, container_height = container_dimensions

    # Vẽ hình hộp 3D thể hiện container
    ax.bar3d(0, 0, 0, container_length, container_width, container_height, color='lightgrey', alpha=0.5, linewidth=0.5)

    # Vẽ hàng hóa đã xếp vào container
    for cargo in loaded_cargos:
        x_pos = cargo['x']
        y_pos = cargo['y']
        z_pos = cargo['z']
        length = cargo['length']
        width = cargo['width']
        height = cargo['height']
        color = (random.random(), random.random(), random.random())  # Màu ngẫu nhiên cho mỗi hàng hóa

        # Vẽ hộp 3D cho mỗi hàng hóa
        ax.bar3d(x_pos, y_pos, z_pos, length, width, height, color=color, alpha=0.7)

        # Vẽ các cạnh màu đỏ cho hàng hóa (thêm chi tiết)
        edges = [
            # Cạnh đáy (z = 0)
            [(x_pos, y_pos, z_pos), (x_pos + length, y_pos, z_pos)],
            [(x_pos + length, y_pos, z_pos), (x_pos + length, y_pos + width, z_pos)],
            [(x_pos + length, y_pos + width, z_pos), (x_pos, y_pos + width, z_pos)],
            [(x_pos, y_pos + width, z_pos), (x_pos, y_pos, z_pos)],

            # Cạnh trên (z = height)
            [(x_pos, y_pos, z_pos + height), (x_pos + length, y_pos, z_pos + height)],
            [(x_pos + length, y_pos, z_pos + height), (x_pos + length, y_pos + width, z_pos + height)],
            [(x_pos + length, y_pos + width, z_pos + height), (x_pos, y_pos + width, z_pos + height)],
            [(x_pos, y_pos + width, z_pos + height), (x_pos, y_pos, z_pos + height)],

            # Cạnh nối giữa đáy và trên
            [(x_pos, y_pos, z_pos), (x_pos, y_pos, z_pos + height)],
            [(x_pos + length, y_pos, z_pos), (x_pos + length, y_pos, z_pos + height)],
            [(x_pos + length, y_pos + width, z_pos), (x_pos + length, y_pos + width, z_pos + height)],
            [(x_pos, y_pos + width, z_pos), (x_pos, y_pos + width, z_pos + height)]
        ]

        # Vẽ các cạnh đỏ
        for edge in edges:
            x_vals = [edge[0][0], edge[1][0]]
            y_vals = [edge[0][1], edge[1][1]]
            z_vals = [edge[0][2], edge[1][2]]
            ax.plot(x_vals, y_vals, z_vals, color='red', linewidth=2)

    # Cài đặt các trục và nhãn
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'***\nCONTAINER LOADING PLAN\nBest Volume Utilization: {best_utilization:.2f}%\n'
                 f'Total Loaded: {number_cagos_loaded}/600\n'
                 f'Ants: {num_ants}, Iterations: {num_iterations}')

    # Hiển thị
    plt.show()

def plot_data(data, num_iterations):
    # Tạo danh sách để chứa các giá trị tương ứng với số vòng lặp
    ants_values = []
    optimal_values = []

    # Lọc ra những cặp có số vòng lặp tương ứng
    for (ants, iterations), value in data.items():
        if iterations == num_iterations:
            ants_values.append(ants)
            optimal_values.append(value)

    # Vẽ đồ thị đường
    plt.figure(figsize=(8, 6))
    plt.plot(ants_values, optimal_values, marker='o', linestyle='-', color='b', label=f'Iterations = {num_iterations}')
    plt.xlabel('Number of Ants')
    plt.ylabel('Optimal Value')
    plt.title(f'Optimal Value for Number of Ants with {num_iterations} Iterations')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    # Đọc dữ liệu hàng hóa từ file
    cargo_list = create_boxes_from_file('data/boxes.txt')

    # Kích thước container (chiều dài, chiều rộng, chiều cao)
    container_dimensions = (12.025, 2.34, 2.67) 

    # Tham số cho ACO
    params = {
        'num_ants': 2,  # Số lượng kiến
        'num_iterations': 1,  # Số lần lặp
        'alpha_values': [1, 2, 4, 6, 8, 9, 4, 2, 1],  # Giá trị alpha
        'beta_values': [9, 8, 6, 4, 2, 1, 6, 8, 9],   # Giá trị beta
        'rho': 0.6,          # Hệ số bay hơi pheromone
        'Q': 10,             # Hệ số tăng cường pheromone
        'load_capacity': 22000, # Trọng tải tối đa
        'volume_capacity': 75
    }

    # Khởi tạo thuật toán ACO
    aco = ACO(cargo_list, container_dimensions, params)

    # Chạy thuật toán ACO
    best_solution, best_utilization, number_cagos_loaded = aco.run()

    # Hiển thị kết quả
    print(f"Best volume utilization: {best_utilization:.1f}%")
    print("Best loading plan:")
    loaded_cargos = []
    total_volume_cargos = 0

    # Tạo dữ liệu cho bảng
    cargo_data = []

    for i in range(number_cagos_loaded):
        cargo = best_solution[i]
        cargo_data.append({
            'Cargo ID': cargo['id'],
            'Volume': cargo['volume'],
            'Weight': cargo['weight'],
            'X': cargo['x'],
            'Y': cargo['y'],
            'Z': cargo['z'],
            'Length': cargo['length'],
            'Width': cargo['width'],
            'Height': cargo['height']
        })

        # Thêm thông tin vị trí và kích thước hàng hóa để trực quan hóa
        loaded_cargos.append({
            'id': cargo['id'],
            'x': cargo['x'],  # Vị trí X của hàng hóa
            'y': cargo['y'],  # Vị trí Y của hàng hóa
            'z': cargo['z'],  # Vị trí Z của hàng hóa
            'length': cargo['length'],
            'width': cargo['width'],
            'height': cargo['height']
        })

    print(f"Total loaded cargoes: {number_cagos_loaded}/600 ")

    # Tạo bảng trực quan
    cargo_df = pd.DataFrame(cargo_data)
    print(cargo_df)

    # Lần 1: Hiển thị biểu đồ đường cho key[0] = 2 (số vòng lặp = 2)
    plot_data(data, num_iterations=2)
    
    # Lần 2: Hiển thị biểu đồ đường cho key[1] = 5 (số vòng lặp = 5)
    plot_data(data, num_iterations=5)
    
    # Lần 3: Trực quan hóa kế hoạch xếp hàng hóa vào container
    plot_container(container_dimensions, loaded_cargos, best_utilization, number_cagos_loaded, params['num_ants'], params['num_iterations'])

if __name__ == '__main__':
    main()
