# main.py

from algorithms.aco import ACO
from processing_data.create_box import create_boxes_from_file

def main():
    # Đọc dữ liệu hàng hóa từ file
    cargo_list = create_boxes_from_file('data/boxes.txt')

    # Kích thước container (chiều dài, chiều rộng, chiều cao)
    container_dimensions = (8.025, 1.34, 2.67) 

    # Tham số cho ACO
    params = {
        'num_ants': 10,  # Số lượng kiến
        'num_iterations': 10,  # Số lần lặp
        'alpha_values': [1, 2, 4, 6, 8, 9, 4, 2, 1],  # Giá trị alpha
        'beta_values': [9, 8, 6, 4, 2, 1, 6, 8, 9],   # Giá trị beta
        'rho': 0.6,          # Hệ số bay hơi pheromone
        'Q': 10,             # Hệ số tăng cường pheromone
        'load_capacity': 1000  # Trọng tải tối đa
    }

    # Khởi tạo thuật toán ACO
    aco = ACO(cargo_list, container_dimensions, params)

    # Chạy thuật toán ACO
    best_solution, best_utilization = aco.run()

    # Hiển thị kết quả
    print(f"Best volume utilization: {best_utilization:.4f}")
    print("Best loading plan:")
    for cargo in best_solution:
        print(f"Cargo ID: {cargo['id']}, Volume: {cargo['volume']}, Weight: {cargo['weight']}")

if __name__ == '__main__':
    main()
