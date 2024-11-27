# wb/WB.py

class WB:
    def __init__(self, container_dimensions, cargo_list):
        self.container_length, self.container_width, self.container_height = container_dimensions
        self.cargo_list = cargo_list  # Danh sách hàng hóa cần xếp
        self.loaded_cargoes = []      # Danh sách hàng hóa đã xếp
        self.remaining_spaces = []    # Danh sách không gian còn lại (SubSpace)
        self.initialize_space()
    
    def initialize_space(self):
        # Khởi tạo không gian container ban đầu
        initial_space = SubSpace(
            length=self.container_length,
            width=self.container_width,
            height=self.container_height,
            x=0, y=0, z=0
        )
        self.remaining_spaces.append(initial_space)
    
    def load_cargo(self):
        # Chỉ xếp một đơn vị hàng hóa vào container
        if not self.cargo_list:
            return
        cargo = self.cargo_list[0]  # Chọn hàng hóa đầu tiên
        # Tìm không gian phù hợp để xếp hàng hóa
        for space in self.remaining_spaces:
            if self.can_fit(cargo, space):
                self.place_cargo(cargo, space)
                self.loaded_cargoes.append(cargo.copy())  # Sử dụng copy để tránh thay đổi gốc
                break
    
    def can_fit(self, cargo, space):
        # Kiểm tra hàng hóa có thể xếp vào không gian không
        return (cargo['length'] <= space.length and
                cargo['width'] <= space.width and
                cargo['height'] <= space.height)
    
    def place_cargo(self, cargo, space):
        # Xếp hàng hóa vào không gian và cập nhật không gian còn lại
        self.remaining_spaces.remove(space)
        # Tạo ba không gian con: bên phải, phía trước, phía trên
        right_space = SubSpace(
            length=space.length - cargo['length'],
            width=cargo['width'],
            height=cargo['height'],
            x=space.x + cargo['length'],
            y=space.y,
            z=space.z
        )
        front_space = SubSpace(
            length=cargo['length'],
            width=space.width - cargo['width'],
            height=cargo['height'],
            x=space.x,
            y=space.y + cargo['width'],
            z=space.z
        )
        upper_space = SubSpace(
            length=cargo['length'],
            width=cargo['width'],
            height=space.height - cargo['height'],
            x=space.x,
            y=space.y,
            z=space.z + cargo['height']
        )
        # Thêm các không gian con vào danh sách không gian còn lại nếu chúng hợp lệ
        for subspace in [right_space, front_space, upper_space]:
            if subspace.length > 0 and subspace.width > 0 and subspace.height > 0:
                self.remaining_spaces.append(subspace)
        # Hợp nhất không gian nếu có thể
        self.merge_spaces()
    
    def merge_spaces(self):
        # Hợp nhất các không gian liền kề theo trục Y
        spaces = self.remaining_spaces.copy()
        for i in range(len(spaces)):
            for j in range(i + 1, len(spaces)):
                s1 = spaces[i]
                s2 = spaces[j]
                if (s1.z == s2.z and s1.x == s2.x and
                    s1.y + s1.width == s2.y and s1.length == s2.length and s1.height == s2.height):
                    # Hợp nhất theo trục Y
                    new_space = SubSpace(
                        length=s1.length,
                        width=s1.width + s2.width,
                        height=s1.height,
                        x=s1.x,
                        y=s1.y,
                        z=s1.z
                    )
                    self.remaining_spaces.remove(s1)
                    self.remaining_spaces.remove(s2)
                    self.remaining_spaces.append(new_space)
                    return  # Thực hiện hợp nhất từng cặp một
        # Hợp nhất không gian liền kề theo trục X
        spaces = self.remaining_spaces.copy()
        for i in range(len(spaces)):
            for j in range(i + 1, len(spaces)):
                s1 = spaces[i]
                s2 = spaces[j]
                if (s1.z == s2.z and s1.y == s2.y and
                    s1.x + s1.length == s2.x and s1.width == s2.width and s1.height == s2.height):
                    # Hợp nhất theo trục X
                    new_space = SubSpace(
                        length=s1.length + s2.length,
                        width=s1.width,
                        height=s1.height,
                        x=s1.x,
                        y=s1.y,
                        z=s1.z
                    )
                    self.remaining_spaces.remove(s1)
                    self.remaining_spaces.remove(s2)
                    self.remaining_spaces.append(new_space)
                    return  # Thực hiện hợp nhất từng cặp một
    
    def display_loaded_cargoes(self):
        print("Loaded cargoes:")
        for cargo in self.loaded_cargoes:
            print(cargo)
    
    def display_remaining_spaces(self):
        print("Remaining spaces:")
        for space in self.remaining_spaces:
            print(space)


class SubSpace:
    def __init__(self, length, width, height, x, y, z):
        self.length = length  # l_i
        self.width = width    # w_i
        self.height = height  # h_i
        self.x = x            # lX_i
        self.y = y            # lY_i
        self.z = z            # lZ_i

    def __repr__(self):
        return f"SubSpace(length={self.length}, width={self.width}, height={self.height}, x={self.x}, y={self.y}, z={self.z})"
