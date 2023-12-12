from maze_solver import *


win = Window(800, 600)

maze = Maze(30, 30, 15, 15, 25, 25, win)

maze.solve()


win.wait_for_close()
