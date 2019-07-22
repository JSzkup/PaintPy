from tkinter import *
from tkinter.colorchooser import askcolor


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("PaintPy")

        self.menubar = Menu(self.root)
        self.fileMenu = Menu(self.root, tearoff=0)

        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.menubar.add_cascade(label="View", menu=self.fileMenu)

        self.fileMenu.add_command(label="Open")
        self.fileMenu.add_command(label="Save")
        self.fileMenu.add_command(label="Exit", command=self.quit_app)

        self.penButton = Button(self.root, text='pen', command=self.usePen)
        self.penButton.grid(row=0, column=0)

        self.brushButton = Button(
            self.root, text='brush', command=self.useBrush)
        self.brushButton.grid(row=0, column=1)

        self.colorButton = Button(
            self.root, text='color', command=self.chooseColor)
        self.colorButton.grid(row=0, column=2)

        self.eraser_button = Button(
            self.root, text='eraser', command=self.useEraser)
        self.eraser_button.grid(row=0, column=3)

        self.chooseSizeButton = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.chooseSizeButton.grid(row=0, column=4)

        self.background = Canvas(self.root, bg='white', width=600, height=600)
        self.background.grid(row=1, columnspan=5)

        # configures and dsiplays the menu bar (file/View)
        self.root.config(menu=self.menubar)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.oldX = None
        self.oldY = None
        self.lineWidth = self.chooseSizeButton.get()
        self.color = self.DEFAULT_COLOR
        self.eraserOn = False
        self.activeButton = self.penButton
        self.background.bind('<B1-Motion>', self.paint)
        self.background.bind('<ButtonRelease-1>', self.reset)

    def usePen(self):
        self.activateButton(self.penButton)

    def useBrush(self):
        self.activateButton(self.brushButton)

    def chooseColor(self):
        self.eraserOn = False
        self.color = askcolor(color=self.color)[1]

    def useEraser(self):
        self.activateButton(self.eraser_button, eraser_mode=True)

    def activateButton(self, some_button, eraser_mode=False):
        self.activeButton.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.activeButton = some_button
        self.eraserOn = eraser_mode

    def paint(self, event):
        self.lineWidth = self.chooseSizeButton.get()
        paintColor = 'white' if self.eraserOn else self.color
        if self.oldX and self.oldY:
            self.background.create_line(self.oldX, self.oldY, event.x, event.y,
                                        width=self.lineWidth, fill=paintColor,
                                        capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.oldX = event.x
        self.oldY = event.y

    def reset(self, event):
        self.oldX, self.oldY = None, None

    def quit_app(event=None):
        self.root.quit()


if __name__ == '__main__':
    Paint()

# TODO Implement an actual eraser
# TODO background color picker
# TODO fill tool
# TODO Nicer brush size UI (number both ends/number on the moving bar)
# TODO CTRL + Z to undo
# TODO Save function
# TODO line / shape tool
# TODO Clear all
# TODO
# TODO
