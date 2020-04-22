import random
from tkinter import *

import torch as torch
import logic
import constants as c

class GameGrid(Frame):
    def __init__(self, neuralNetwork):
        self.root = Tk()
        Frame.__init__(self)
        self.EXITCODE = True

        self.grid()
        self.master.title('2048')
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_H: logic.left, c.KEY_L: logic.right,
                         c.KEY_K: logic.up, c.KEY_J: logic.down}
        
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.didNothing = 0

        while self.EXITCODE == True:
            self.previousMatrix = self.matrix
            nnoutput = neuralNetwork(self.matrix2tensor(self.matrix))
            self.key_down(self.nnoutput2char(nnoutput))
            print(self.matrix)
            if(self.matrix == self.previousMatrix):
                self.didNothing += 1
                if(self.didNothing>c.DONOTHINGINPUT_MAX):
                    self.EXITCODE = logic.game_score(self.matrix)
            if(self.EXITCODE == True):
                self.root.update()
        
    def quitting(self):
        self.root.destroy()
    def nnoutput2char(self, x):
        x = x.tolist().index(max(x.tolist()))  # returns the index which has max probability

        # transforms index into char
        valid_chars = [c.KEY_LEFT, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_UP]

        return valid_chars[x]

    def matrix2tensor(self, matrix):
        y = []
        for i in matrix:
            for e in i:
                y.append(float(e))
        y = torch.FloatTensor(y)
        return y

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = event
        if key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                global EXITCODE
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                done = False
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="Won", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.EXITCODE = logic.game_score(self.matrix)
                    self.quitting()
                elif(logic.game_state(self.matrix) == 'not over'):
                    None
                else:
                    self.EXITCODE = logic.game_score(self.matrix)
                    self.quitting()
                    

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2
