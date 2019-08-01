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
        self.viewMenu.add_command(label="Hide UI", command=self.hideUI)
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label="About", command=self.aboutPage)

        # ------------main UI------------
        self.penButton = Button(self.root, text='pen', command=self.usePen)
        self.penButton.grid(row=0, column=0)

        self.shapeButton = Button(
            self.root, text='Shape', command=self.changeShape)
        self.shapeButton.grid(row=0, column=1)

        self.colorButton = Button(
            self.root, text='color', command=self.chooseColor)
        self.colorButton.grid(row=0, column=2)

        self.eraserButton = Button(
            self.root, text='eraser', command=self.useEraser)
        self.eraserButton.grid(row=0, column=3)

        self.sizeSlider = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.sizeSlider.grid(row=0, column=4)

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
        # TODO if shape is selected, draw shape instead
        self.background.bind('<B1-Motion>', self.paint)
        # Stops the mouse from drawing on M1 release
        self.background.bind('<ButtonRelease-1>', self.reset)

    # Hides the top ui from the user
    def hideUI(self):
        self.penButton.grid_remove()
        self.shapeButton.grid_remove()
        self.colorButton.grid_remove()
        self.eraserButton.grid_remove()
        self.sizeSlider.grid_remove()

    # TODO implement this into menu bar
    def restoreUI(self):
        self.penButton.grid()
        self.shapeButton.grid()
        self.colorButton.grid()
        self.eraserButton.grid()
        self.sizeSlider.grid()

    def usePen(self):
        self.activateButton(self.penButton)

    def changeShape(self):
        self.activateButton(self.shapeButton)

        self.top = Toplevel()
        self.shapeMenu = Menu(self.top)

        self.top.title("Shape Selection")
        self.msg = Message(self.top, text="sample text")
        self.msg.pack()

    def aboutPage(self):
        self.about = Toplevel(master=None, padx=10, pady=10)

        self.about.title("About PaintPy")
        self.msg = Message(
            self.about, text="Created by Jonathan Szkup using Python")
        self.msg.pack()

    def chooseColor(self):
        self.eraserOn = False
        self.color = askcolor(color=self.color)[1]

    def useEraser(self):
        # Eraser sets color of the brush to white
        self.activateButton(self.eraserButton, eraserMode=True)

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
