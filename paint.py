from tkinter import *
from tkinter.colorchooser import askcolor


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("PaintPy")

        # ------------TOP UI------------
        self.menubar = Menu(self.root)
        self.fileMenu = Menu(self.root, tearoff=0)
        self.editMenu = Menu(self.root, tearoff=0)
        self.viewMenu = Menu(self.root, tearoff=0)

        # Creating the TOP file menu
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        # Dropdown Menu for file menu
        self.fileMenu.add_command(label="Open")
        self.fileMenu.add_command(label="Save")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.quitApp)

        # Creating EDIT tab in menubar
        self.menubar.add_cascade(label="Edit", menu=self.editMenu)
        self.editMenu.add_command(label="Undo")
        self.editMenu.add_command(label="Clear Canvas", command=self.deleteAll)

        # Creating the View tab in the menubar, next to file
        self.menubar.add_cascade(label="View", menu=self.viewMenu)
        self.viewMenu.add_command(label="Fullscreen", command=self.fullscreen)
        self.viewMenu.add_command(label="Hide UI")
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label="About")

        # ------------main UI------------
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

        self.sizeSlider = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.sizeSlider.grid(row=0, column=4)

        # TODO implement
        # self.deleteAll = Button(
        #     self.root, text='Delete All', command=self.DeleteALL)
        # self.eraser_button.grid(row=0, column=5)

        # Sets resolution of the window, color of the canvas
        self.background = Canvas(self.root, bg='white', width=950, height=700,)
        self.background.grid(row=1, columnspan=5)

        # configures and dsiplays the menu bar (file/View)
        self.root.config(menu=self.menubar)
        self.setup()
        self.root.mainloop()

    def setup(self):
        self.oldX = None
        self.oldY = None
        self.lineWidth = self.sizeSlider.get()
        self.color = self.DEFAULT_COLOR
        self.eraserOn = False
        self.activeButton = self.penButton
        # Sets mouse click one to paint on the canvas
        self.background.bind('<B1-Motion>', self.paint)
        # Stops the mouse from drawing on M1 release
        self.background.bind('<ButtonRelease-1>', self.reset)

    def usePen(self):
        self.activateButton(self.penButton)

    def useBrush(self):
        self.activateButton(self.brushButton)

    def chooseColor(self):
        self.eraserOn = False
        self.color = askcolor(color=self.color)[1]

    def useEraser(self):
        # Eraser sets color of the brush to white
        self.activateButton(self.eraser_button, eraserMode=True)

    def activateButton(self, someButton, eraserMode=False):
        # On button click the button will sink
        # if selectable will stay sunken
        self.activeButton.config(relief=RAISED)
        someButton.config(relief=SUNKEN)
        self.activeButton = someButton
        self.eraserOn = eraserMode

    def fullscreen(self):
        # TODO scale the whole drawing window to resolution (Canvas())
        self.root.attributes("-fullscreen", True)
        # menu.entryconfigure(1, label="Exit Fullscreen")
        # TODO if already in fullscreen have the text change to exit fullscreen, and leave fullscreen

    def paint(self, event):
        # Gets the size of the stroke
        self.lineWidth = self.sizeSlider.get()
        # Sets the eraser to be the color "white"
        paintColor = 'white' if self.eraserOn else self.color
        # Painting based on position of the mouse relative to the canvas
        if self.oldX and self.oldY:
            self.background.create_line(self.oldX, self.oldY, event.x, event.y,
                                        width=self.lineWidth, fill=paintColor,
                                        capstyle=ROUND, smooth=TRUE,
                                        splinesteps=36)
        self.oldX = event.x
        self.oldY = event.y

    # stops drawing
    def reset(self, event):
        self.oldX, self.oldY = None, None

    # Deletes everything on the canvas
    def deleteAll(self):
        self.background.delete("all")

    # Closes PaintPy
    def quitApp(self):
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
