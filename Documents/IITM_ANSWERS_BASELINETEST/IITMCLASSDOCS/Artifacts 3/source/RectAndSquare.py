class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def get_area(self):
        return self.length * self.width

    def get_perimeter(self):
        return 2 * (self.length + self.width)

    def set_length(self, new_length):
        self.length = new_length

    def set_width(self, new_width):
        self.width = new_width


class Square(Rectangle):
    def __init__(self, side_length):
        super().__init__(side_length, side_length)


class NewSquare(Rectangle):
    def __init__(self, side_length):
        super().__init__(side_length, side_length)

    def set_length(self, new_length):
        self.length = new_length
        self.width = new_length

    def set_width(self, new_width):
        self.length = new_width
        self.width = new_width


class NewSquare_2:
    def __init__(self, side_length):
        self.rect = Rectangle(side_length, side_length)

    def set_length(self, new_length):
        self.rect.length = new_length
        self.rect.width = new_length

    def set_width(self, new_width):
        self.rect.length = new_width
        self.rect.width = new_width


class Square3:
    def __init__(self, side_length):
        self.side = side_length

    def set_side(self, new_side):
        self.side = new_side

    def get_area(self):
        return self.side * self.side
