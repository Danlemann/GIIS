import keyboard
import numpy as np
import tkinter as tk

class LineEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Графический редактор")

        self.canvas = tk.Canvas(self.root, width=900, height=400, bg="grey")
        self.canvas.pack()

        self.debug_mode = False

        self.grid_size = 10
        for x in range(0, 800, self.grid_size):
            self.canvas.create_line(x, 0, x, 800, fill="gray")
        for y in range(0, 800, self.grid_size):
            self.canvas.create_line(0, y, 800, y, fill="gray")

        self.dda_button = tk.Button(self.root, text="ЦДА", command=self.draw_dda)
        self.bresenham_button = tk.Button(self.root, text="Брезенхем", command=self.draw_bresenham)
        self.wu_button = tk.Button(self.root, text="Алгоритм Ву", command=self.draw_wu)
        self.delete_button = tk.Button(self.root, text="Удалить все", command=self.delete)
        self.debug_mode_button = tk.Button(self.root, text="Отладка", command=self.toggle_debug_mode)

        self.dda_button.pack()
        self.bresenham_button.pack()
        self.wu_button.pack()
        self.delete_button.pack()
        self.debug_mode_button.pack()

        self.current_algorithm = None
        self.points = []

        self.canvas.bind("<Button-1>", self.on_click)

        self.root.mainloop()

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.debug_mode_button.configure(bg="green")
        else:
            self.debug_mode_button.configure(bg="grey")

    def on_click(self, event):
        # Округляем координаты до ближайшей ячейки сетки
        x = round(event.x / self.grid_size) * self.grid_size
        y = round(event.y / self.grid_size) * self.grid_size
        self.points.append((x, y))

        if len(self.points) == 2:
            self.draw_line()
            self.points = []

    def draw_line(self):
        self.grid_size = 10
        if self.current_algorithm:
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]
            self.current_algorithm(x1, y1, x2, y2)

    def draw_dda(self):
        self.current_algorithm = self.dda

    def draw_bresenham(self):
        self.current_algorithm = self.bresenham

    def draw_wu(self):
        self.current_algorithm = self.wu

    def delete(self):
        self.canvas.delete("all")
        for x in range(0, 800, self.grid_size):
            self.canvas.create_line(x, 0, x, 800, fill="gray")
        for y in range  (0, 800, self.grid_size):
            self.canvas.create_line(0, y, 800, y, fill="gray")

    def dda(self, x1, y1, x2, y2):
        dx = int((x2 - x1) / self.grid_size)
        dy = int((y2 - y1) / self.grid_size)
        steps = max(abs(dx), abs(dy))

        x_increment = (dx / steps) * self.grid_size
        y_increment = (dy / steps) * self.grid_size

        x = x1
        y = y1

        for _ in range(int(steps) + 1):
            pixel_x = int(x)
            pixel_y = int(y)
            pixel_x = ((pixel_x // self.grid_size) * self.grid_size) + (self.grid_size // 2)
            pixel_y = ((pixel_y // self.grid_size) * self.grid_size) + (self.grid_size // 2)
            self.canvas.create_rectangle(pixel_x - self.grid_size / 2, pixel_y - self.grid_size / 2,
                                         pixel_x + self.grid_size / 2, pixel_y + self.grid_size / 2, fill="black")
            if self.debug_mode:
                self.canvas.update()
                keyboard.wait('space')
            x += x_increment
            y += y_increment

    def bresenham(self, x1, y1, x2, y2):
        dx = int(abs(x2 - x1) / self.grid_size)
        dy = int(abs(y2 - y1) / self.grid_size)
        sx = -1 * self.grid_size if x1 > x2 else self.grid_size
        sy = -1 * self.grid_size if y1 > y2 else self.grid_size
        err = dx - dy

        while x1 != x2 or y1 != y2:
            x1 = ((x1 // self.grid_size) * self.grid_size) + (self.grid_size // 2)
            x2 = ((x2 // self.grid_size) * self.grid_size) + (self.grid_size // 2)
            self.canvas.create_rectangle(x1 - self.grid_size / 2, y1 - self.grid_size / 2, x1 + self.grid_size / 2,
                                         y1 + self.grid_size / 2, fill="black")
            if self.debug_mode:
                self.canvas.update()
                keyboard.wait('space')
            err2 = 2 * err
            if err2 > -dy:
                err -= dy
                x1 += sx

            if err2 < dx:
                err += dx
                y1 += sy

    def wu(self, x1, y1, x2, y2):
        steep = abs(y2 - y1) > abs(x2 - x1)
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        self.draw_pixel_wu(steep, x1, y1, 0)
        self.draw_pixel_wu(steep, x2, y2, 0)
        dx = int((x2 - x1) / self.grid_size)
        dy = int((y2 - y1) / self.grid_size)
        gradient = dy / dx
        y = y1 + gradient * self.grid_size
        steps = int((x2 - x1) / self.grid_size)
        x = x1 + self.grid_size
        for _ in range(steps):
            if self.debug_mode:
                self.canvas.update()
                keyboard.wait('space')
            if (y % self.grid_size != y % (self.grid_size / 2)):
                if (y % (self.grid_size / 2) < 0.2 * self.grid_size):
                    self.draw_pixel_wu(steep, x, int(y), 0)
                else:
                    self.draw_pixel_wu(steep, x, int(y), y % (self.grid_size / 2) / self.grid_size)
                    self.draw_pixel_wu(steep, x, int(y) + self.grid_size, 1 - y % (self.grid_size / 2) / self.grid_size)
            else:
                if (self.grid_size / 2 - y % (self.grid_size / 2) < 0.2 * self.grid_size):
                    self.draw_pixel_wu(steep, x, int(y), 0)
                else:
                    self.draw_pixel_wu(steep, x, int(y),
                                       (self.grid_size / 2 - y % (self.grid_size / 2)) / self.grid_size)
                    self.draw_pixel_wu(steep, x, int(y) - self.grid_size,
                                       (self.grid_size / 2 - 1 + y % (self.grid_size / 2)) / self.grid_size)

            y += gradient * self.grid_size
            x += self.grid_size

    def draw_pixel_wu(self, steep, x, y, intensity):
        if steep:
            x, y = y, x
        x = ((x // self.grid_size) * self.grid_size) + (self.grid_size // 2)
        y = ((y // self.grid_size) * self.grid_size) + (self.grid_size // 2)
        intensity = max(0, min(intensity, 1))
        color = "#" + "{:02x}{:02x}{:02x}".format(int(255 * intensity), int(255 * intensity), int(255 * intensity))
        self.canvas.create_rectangle(x - self.grid_size / 2, y - self.grid_size / 2, x + self.grid_size / 2,
                                     y + self.grid_size / 2, fill=color, outline=color)

if __name__ == "__main__":
    LineEditor()