from tkinter import *
import random


class Apple:
    def __init__(self):
        self.location = [random.randint(1, 79), random.randint(1, 29)]
        self.char = "X"

    def new(self):
        self.location = [random.randint(1, 79), random.randint(1, 29)]


class GameBox:
    def __init__(self, master, start_text):
        self.text = start_text
        self.game_box = Text(master)
        self.game_box.insert("1.0", self.text)
        self.game_box.config(state='disabled')

    def update(self, new_text):
        self.text = new_text
        self.game_box.config(state='normal')
        self.game_box.delete("1.0", "end-1c")
        self.game_box.insert("1.0", self.text)
        self.game_box.config(state='disabled')


class Snake:
    def __init__(self):
        self.body = ["-", "-", "O"]
        self.positions = [[1, 1], [2, 1], [3, 1]]
        self.direction = "E"
        self.alive = True

    def update_positions(self):
        head_index = len(self.positions) - 1

        for x in range(0, len(self.positions) - 1):
            self.positions[x] = self.positions[x + 1]

        head_position = self.positions[head_index]
        if self.direction == "E":
            head_position = [head_position[0] + 1, head_position[1]]
            self.positions[len(self.positions) - 1] = head_position

        elif self.direction == "W":
            head_position = [head_position[0] - 1, head_position[1]]
            self.positions[len(self.positions) - 1] = head_position

        elif self.direction == "N":
            head_position = [head_position[0], head_position[1] - 1]
            self.positions[len(self.positions) - 1] = head_position

        else:
            head_position = [head_position[0], head_position[1] + 1]
            self.positions[len(self.positions) - 1] = head_position

        self.check_dead()

    def check_dead(self):
        for p in self.positions:
            if p[0] > 80 or p[0] < 0 or p[1] > 30 or p[1] < 0:
                self.alive = False

    def add(self):
        self.body.insert(0, "-")
        self.positions.insert(0, self.positions[0])


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("590x410")
        self.root.resizable(width=False, height=False)
        self.root.title("Snake - 0 points")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.game_box = GameBox(self.root, "")

        self.game_box.game_box.grid(row=0, column=0, sticky=N + S + E + W)

        self.snake = Snake()

        self.apple = Apple()

        self.score = 0

        self.root.bind("<Key>", self.change_direction)

        self.root.after(0, self.build_display)

    def build_display(self):
        print(self.snake.positions)
        display = []
        for y in range(0, 31):
            display.append([])
            for x in range(0, 81):
                if x == 0 or x == 80:
                    display[y].append("|")

                if y == 0 or y == 30:
                    display[y].append("-")

                else:
                    display[y].append(" ")

        for x in range(0, len(self.snake.positions)):
            display[self.apple.location[1]][self.apple.location[0]] = self.apple.char
            display[self.snake.positions[x][1]][self.snake.positions[x][0]] = self.snake.body[x]

        head = self.snake.positions[len(self.snake.positions) - 1]
        for x in range(0, len(self.snake.positions) - 1):
            if head == self.snake.positions[x]:
                self.snake.alive = False

        d = ""
        for x in range(0, len(display)):
            d += "".join(display[x])
            d += "\n"

        display = d

        self.game_box.update(display)
        self.snake.update_positions()

        if self.snake.positions[len(self.snake.positions) - 1] == self.apple.location:
            self.score += 1
            self.apple.new()
            self.snake.add()
            self.root.title("Snake - {} points".format(self.score))

        if self.snake.alive:
            self.root.after(100, self.build_display)
        else:
            self.game_box.update("YOU DIED")

    def change_direction(self, event):
        if event.char == 'w':
            self.snake.direction = "N"
        elif event.char == 'd':
            self.snake.direction = "E"
        elif event.char == 's':
            self.snake.direction = "S"
        elif event.char == 'a':
            self.snake.direction = "W"


if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
