import time
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
        self._root = Tk()
        self._root.title("Maze Solver")
        self._canvas = Canvas(self._root, bg="white", height=height, width=width)
        self._canvas.pack(fill=BOTH, expand=1)
        self._is_running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._is_running = True
        while self._is_running:
            self.redraw()

    def close(self):
        self._is_running = False

    def draw_line(self, line: Line, color: str):
        line.draw(self._canvas, color)


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

    def draw_move(self, to_cell: 'Cell', undo=False):
        center1 = Point((self.top_left.x + self.bottom_right.x) // 2, (self.top_left.y + self.bottom_right.y) // 2)
        center2 = Point((to_cell.top_left.x + to_cell.bottom_right.x) // 2,
                        (to_cell.top_left.y + to_cell.bottom_right.y) // 2)
        line = Line(center1, center2)
        if not undo:
            self.win.draw_line(line, "red")
        else:
            self.win.draw_line(line, "gray")


class Maze:
    import time
    def __init__(self, maze_pos: Point, num_cols: int, num_rows: int, cell_size: Point, win: Window):
        self._maze_pos = maze_pos
        self._win = win
        self._cell_size = cell_size
        self._cells = self._create_cells(num_cols, num_rows)
        self._draw_cell()

    def _create_cells(self, num_cols: int, num_rows: int):
        cells = [[] for _ in range(num_rows+1)]
        cell_pos = Point(self._maze_pos.x, self._maze_pos.y)

        for row in cells:
            for _ in range(num_cols):
                br = Point((cell_pos.x + self._cell_size.x), cell_pos.y + self._cell_size.y)
                row.append(Cell(cell_pos, br, self._win))
                cell_pos.x += self._cell_size.x
            cell_pos.x = self._maze_pos.x
            cell_pos.y += self._cell_size.y
        return cells

    def _draw_cell(self):
        for row in self._cells:
            for cell in row:
                cell.draw_cell()
                self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(.05)
