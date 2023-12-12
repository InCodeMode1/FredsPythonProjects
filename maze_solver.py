import time
import random
from tkinter import Tk, BOTH, Canvas


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str = "black"):
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

    def draw_line(self, line: Line, color: str = "black"):
        line.draw(self._canvas, color)


class Cell:

    def __init__(self, win: Window = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.visited = False
        self.win = win

    def draw_cell(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        if self.has_left_wall:
            p1 = Point(x1, self.y1)
            p2 = Point(x1, self.y2)
            self.win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x1, y1)
            p2 = Point(x1, y2)
            self.win.draw_line(Line(p1, p2), "white")
        if self.has_right_wall:
            p1 = Point(x2, y1)
            p2 = Point(x2, y2)
            self.win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x2, y1)
            p2 = Point(x2, y2)
            self.win.draw_line(Line(p1, p2), "white")
        if self.has_top_wall:
            p1 = Point(x1, y1)
            p2 = Point(x2, y1)
            self.win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x1, y1)
            p2 = Point(x2, y1)
            self.win.draw_line(Line(p1, p2), "white")
        if self.has_bottom_wall:
            p1 = Point(x1, y2)
            p2 = Point(x2, y2)
            self.win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x1, y2)
            p2 = Point(x2, y2)
            self.win.draw_line(Line(p1, p2), "white")

    def draw_move(self, to_cell: 'Cell', undo=False):
        center1 = Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        center2 = Point((to_cell.x1 + to_cell.x2) // 2,
                        (to_cell.y1 + to_cell.y2) // 2)
        line = Line(center1, center2)
        if self.win is None:
            return
        if not undo:
            self.win.draw_line(line, "red")
        else:
            self.win.draw_line(line, "gray")



class Maze:

    def __init__(self, x1, y1, num_cols: int, num_rows: int, cell_size_x, cell_size_y, win: Window = None, seed = None):
        self._x1 = x1
        self._y1 = y1

        self._win = win
        self._num_cols = num_cols
        self._num_rows = num_rows
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []

        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for _ in range(self._num_cols):
            cells = []
            for _ in range(self._num_rows):
                cells.append(Cell(self._win))
            self._cells.append(cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw_cell(x1, y1, x2, y2)
        self._animate()

    def _break_entrance_and_exit(self):

        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)

        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(.05)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

