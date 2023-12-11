from maze_solver import *


win = Window(800, 600)

maze = Maze(Point(30, 30), 10, 10, Point(50, 50), win)

win.wait_for_close()
