# processing_data/create_box.py

def create_boxes_from_file(filename):
    cargo_list = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) < 6:
                raise ValueError("Each line must have at least 6 values: id,length,width,height,weight,quantity")
            cargo = {
                'id': parts[0],
                'length': float(parts[1]),
                'width': float(parts[2]),
                'height': float(parts[3]),
                'weight': float(parts[4]),
                'quantity': int(parts[5])  # Thêm số lượng
            }
            cargo['volume'] = cargo['length'] * cargo['width'] * cargo['height']
            cargo_list.append(cargo)
    return cargo_list
