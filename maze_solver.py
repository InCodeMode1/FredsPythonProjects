from tkinter import Tk, BOTH, Canvas


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)


class Window:

    def __init__(self, height, width):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def close(self):
        self.__is_running = False

    def draw_line(self, line: Line, color: str):
        line.draw(self.__canvas, color)


class Cell:

    def __init__(self, top_left: Point, bottom_right: Point, win: Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.win = win

    def draw_cell(self):
        if self.has_left_wall:
            p1 = Point(self.top_left.x, self.top_left.y)
            p2 = Point(self.top_left.x, self.bottom_right.y)
            self.win.draw_line(Line(p1, p2), "black")
        if self.has_right_wall:
            p1 = Point(self.bottom_right.x, self.top_left.y)
            p2 = Point(self.bottom_right.x, self.bottom_right.y)
            self.win.draw_line(Line(p1, p2), "black")
        if self.has_top_wall:
            p1 = Point(self.top_left.x, self.top_left.y)
            p2 = Point(self.bottom_right.x, self.top_left.y)
            self.win.draw_line(Line(p1, p2), "black")
        if self.has_bottom_wall:
            p1 = Point(self.top_left.x, self.bottom_right.y)
            p2 = Point(self.bottom_right.x, self.bottom_right.y)
            self.win.draw_line(Line(p1, p2), "black")
