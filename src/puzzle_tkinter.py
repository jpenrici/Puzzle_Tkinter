# -*- Mode: Python3; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-
#
# Reference:
#   https://docs.python.org/3/library/tkinter.html

import os
from tkinter import *
from tkinter import filedialog, messagebox
from random import choice, shuffle
from PIL import Image, ImageTk


class PuzzleGUI(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Hobby")
        self.pack()
        self.create_widgets()
        # Example
        self.newImage("../images/base.png")

    def create_widgets(self):
        self.vbox = [Frame(self.master) for i in range(4)]

        self.info = Label(self.vbox[0], text="")
        self.info.pack(side="left")

        self.height, self.width = 500, 550
        self.canvas = Canvas(self.vbox[1], height=self.height, width=self.width)
        self.canvas.bind("<Button-1>", self.mouse_clicked)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)
        self.canvas.pack()

        self.status = Label(self.vbox[2], text="")
        self.status.pack(side="left")

        self.btnLoad = Button(self.vbox[3], text="Load", command=self.newImage)
        self.btnLoad.pack(side="left")

        self.btnShuffle = Button(self.vbox[3], text="Shuffle", command=self.shuffleImage)
        self.btnShuffle.pack(side="left")

        for vbox in self.vbox:
            vbox.pack()

    def newImage(self, filename=None):
        start = False
        if filename == None:
            filename = filedialog.askopenfilename(title="Select An Image")
        try:
            img = Image.open(filename)
            img_width, img_height = img.size
            self.image = img
            start = True
            if img_height > self.height or img_width > self.width:
                size = min(self.width, self.height)
                self.image = img.resize((size, size), Image.ANTIALIAS)
        except:
            self.status.configure(text="Load a image file.")
            messagebox.showwarning(title="Alert",
                message="There is something wrong.")

        if start:
            filename = os.path.basename(filename)
            self.status.configure(text="Image: {}".format(filename))
            self.make()

    def shuffleImage(self):
        while self.puzzle == self.original:
            shuffle(self.puzzle)
        info = "To move the pieces, keep the left mouse button pressed."
        self.info.configure(text=info)
        self.start = True
        self.render()

    def make(self):
        img_width, img_height = self.image.size
        self.borderX = (self.width - img_width) / 2
        self.borderY = (self.height - img_height) / 2

        self.size = choice([50, 100, 250])
        self.rows = int(img_height / self.size)
        self.cols = int(img_width / self.size)

        self.original = []
        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c * self.size, r * self.size
                cropped = self.image.crop((x, y, x + self.size, y + self.size))
                self.original += [ImageTk.PhotoImage(cropped)]

        self.puzzle = self.original[::]
        self.start = False
        self.selected = 0
        self.steps = 1
        self.render()

    def render(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#fff")
        for r in range(self.rows):
            y = (r * self.size) + self.borderY
            for c in range(self.cols):
                x = (c * self.size) + self.borderX
                self.canvas.create_image(x, y, anchor="nw",
                    image=self.puzzle[r * self.cols + c])

    def validate(self, x, y):
        if not self.start:
            return False     
        if x < (self.borderX + 2) or x > (self.width - self.borderX - 2):
            return False
        if y < (self.borderY + 2) or y > (self.height - self.borderY - 2):
            return False
        return True

    def mouse_clicked(self, event):
        x, y = event.x, event.y
        if not self.validate(x, y):
            return
        r = int((y - self.borderY) / self.size)
        c = int((x - self.borderX) / self.size)
        self.selected = r * self.cols + c

    def mouse_move(self, event):
        x, y = event.x, event.y
        if not self.validate(x, y):
            return
        self.render()
        self.canvas.create_image(x, y, image=self.puzzle[self.selected])

    def mouse_release(self, event):
        x, y = event.x, event.y
        if not self.validate(x, y):
            self.render()
            return
        r = int((y - self.borderY) / self.size)
        c = int((x - self.borderX) / self.size)
        i = r * self.cols + c
        temp = self.puzzle[i]
        self.puzzle[i] = self.puzzle[self.selected]
        self.puzzle[self.selected] = temp
        self.render()

        if self.original == self.puzzle:
            self.info.configure(text="Click Load or Shuffle.")
            messagebox.showinfo(title="Congratulations",
                message="Completed in {} steps.".format(self.steps))
            self.make()
        else:
            self.steps += 1


if __name__ == '__main__':
    root = Tk()
    app = PuzzleGUI(master=root)
    app.mainloop()
