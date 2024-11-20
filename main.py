from random import sample, randint
from math import ceil, pi


class Map:
    planets_data = []

    def __init__(self, size_mode: str, planets_amount_mode: str):
        match  size_mode:
            case 'small':
                self.size = 1000
                match planets_amount_mode:
                    case 'small':
                        self.number_planets = 15
                    case 'medium':
                        self.number_planets = 20
                    case 'large':
                        self.number_planets = 28
            case 'medium':
                self.size = 5000
                match planets_amount_mode:
                    case 'small':
                        self.number_planets = 75
                    case 'medium':
                        self.number_planets = 100
                    case 'large':
                        self.number_planets = 140
            case 'large':
                self.size = 10000
                match planets_amount_mode:
                    case 'small':
                        self.number_planets = 150
                    case 'medium':
                        self.number_planets = 200
                    case 'large':
                        self.number_planets = 280
        self.map = [[0 for _ in range(self.size)] for _ in range(self.size)]

        self.planet_generation(self.number_planets)

    def print_map(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.map[i][j], end='  ')
            print()

    def print_map_clear(self):
        for i in range(self.size):
            for j in range(self.size):
                if i == 0 or j == 0 or i == self.size - 1 or j == self.size - 1:
                    print(self.map[i][j], end='  ')
                elif self.map[i][j] == 0 or self.map[i][j] == 10:
                    print(' ', end='  ')
                else:
                    print(self.map[i][j], end='  ')
            print()

    def get_planets_info(self):
        for data in self.planets_data:
            print(f"Center Cords: ({data[0]}, {data[1]}), Min Radius: {data[2]}")

    def get_map(self):
        return self.map

    def clear(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 10:
                    self.map[i][j] = 0

    def planet_generation(self, num):
        # Размещаем области для генерации планет, а так же сохраняем их центры
        k = 0

        while k < num:
            if ceil(self.size / 100 * 10) > 49:
                red_zone = int(49 * 1.5)
            else:
                red_zone = int(ceil(self.size / 100 * 10) * 1.5)
            x, y = sample(range(2, self.size - 3), 2)

            if self.map[x][y] == 0:
                x0, y0, x1, y1 = max(x - red_zone, 1), max(y - red_zone, 1), min(x + red_zone, self.size - 2), min(
                    y + red_zone, self.size - 2)

                intersects = any(self.map[i][j] != 0 for i in range(x0, x1 + 1) for j in range(y0, y1 + 1))

                if not intersects:
                    for i in range(x0, x1 + 1):
                        for j in range(y0, y1 + 1):
                            self.map[i][j] = 10
                    # self.map[x][y] = 9                                               # Возможно удалить
                    self.planets_data.append([x, y])
                    k += 1
        self.find_planets_radius()
        self.planet_placement()

    def find_planets_radius(self):
        # Находим максимальные вписанные радиусы планет
        arr = []
        for i in self.planets_data:
            k = 0
            for j in range(i[1] + 1, self.size):
                if self.map[i[0]][j] == 0:
                    arr.append(k)
                    break
                else:
                    k += 1

            k = 0
            for j in range(i[1] - 1, -1, -1):
                if self.map[i[0]][j] == 0:
                    arr.append(k)
                    break
                else:
                    k += 1

            k = 0
            for j in range(i[0] + 1, self.size):
                if self.map[j][i[1]] == 0:
                    arr.append(k)
                    break
                else:
                    k += 1

            k = 0
            for j in range(i[0] - 1, -1, -1):
                if self.map[j][i[1]] == 0:
                    arr.append(k)
                    break
                else:
                    k += 1
            minimum = min(arr)
            arr = []
            if minimum > ceil(self.size / 100 * 10):
                minimum = ceil(self.size / 100 * 10)
            i.append(minimum)

    def planet_placement(self):
        # Создаем планеты из полученных данных
        self.clear()
        for center_cords in self.planets_data:
            if (center_cords[2] * 2 + 1) < 49:
                size = randint(3, center_cords[2] * 2 + 1)
            else:
                size = 49
            if size % 2 == 0:
                size -= 1

            cut_size = int(size // pi)
            center_x = center_cords[0]
            center_y = center_cords[1]
            start_x = center_x - size // 2
            start_y = center_y - size // 2

            for i in range(size):
                for j in range(size):
                    x = start_x + i
                    y = start_y + j

                    if i < cut_size and j < cut_size:
                        if i + j >= cut_size:
                            self.map[x][y] = 9
                    elif i < cut_size and j >= size - cut_size:
                        if i + (size - j - 1) >= cut_size:
                            self.map[x][y] = 9
                    elif i >= size - cut_size and j < cut_size:
                        if (size - i - 1) + j >= cut_size:
                            self.map[x][y] = 9
                    elif i >= size - cut_size and j >= size - cut_size:
                        if (size - i - 1) + (size - j - 1) >= cut_size:
                            self.map[x][y] = 9
                    else:
                        self.map[x][y] = 9

            for i in range(size):
                for j in range(size):
                    x = start_x + i
                    y = start_y + j

                    if self.map[x][y] == 9:
                        if x > 0 and y > 0 and self.map[x - 1][y] == 0 and self.map[x][y - 1] == 0:
                            self.map[x][y] = 1  # верхний левый угол
                        elif x > 0 and y < self.size - 1 and self.map[x - 1][y] == 0 and self.map[x][y + 1] == 0:
                            self.map[x][y] = 3  # нижний левый угол
                        elif x < self.size - 1 and y > 0 and self.map[x + 1][y] == 0 and self.map[x][y - 1] == 0:
                            self.map[x][y] = 7  # верхний правый угол
                        elif (x < self.size - 1 and y < self.size - 1 and self.map[x + 1][y] == 0 and
                              self.map[x][y + 1] == 0):
                            self.map[x][y] = 5  # нижний правый угол
                        elif x > 0 and self.map[x - 1][y] == 0:
                            self.map[x][y] = 2  # левая сторона
                        elif x < self.size - 1 and self.map[x + 1][y] == 0:
                            self.map[x][y] = 6  # правая сторона
                        elif y > 0 and self.map[x][y - 1] == 0:
                            self.map[x][y] = 8  # верхняя сторона
                        elif y < self.size - 1 and self.map[x][y + 1] == 0:
                            self.map[x][y] = 4  # нижняя сторона


game_map = Map('small', 'large')
map_array = game_map.get_map()
