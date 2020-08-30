#!/usr/bin/env python3

from field import Field
from tkinter import Tk, Frame, Canvas, ALL, NW

class MADN(Frame):

    def __init__(self):
        super().__init__()

        self.master.title('Mensch aergere dich nicht!')
        self.Field = Field(3)
        self.pack()


def main():

    root = Tk()
    nib = MADN()
    root.mainloop()


if __name__ == '__main__':
    main()
