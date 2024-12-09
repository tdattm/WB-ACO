# processing_data/create_box.py

def create_boxes_from_file(filename):
    cargo_list = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) < 5:
                raise ValueError("Each line must have at least 5 values: id,length,width,height,weight")
            cargo = {
                'id': parts[0],
                'length': float(parts[1]),
                'width': float(parts[2]),
                'height': float(parts[3]),
                'weight': float(parts[4])
            }
            cargo['volume'] = cargo['length'] * cargo['width'] * cargo['height']

            # Khởi tạo các vị trí x, y, z mặc định là 0
            cargo['x'] = 0
            cargo['y'] = 0
            cargo['z'] = 0

            cargo_list.append(cargo)
    return cargo_list
