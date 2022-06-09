from distutils.command.build import build
import tkinter as tk

class GUI:
    '''Minesweeper GUI.'''

    BUTTON_SIZE = 20
    BUTTON_FONT = 'sans 10 bold'
    HOVER_COLOR = "#9a9a9a"
    SHOWN_COLOR = "#BCBCBC"
    COLOR_MAP = {
        0: 'black', # Empty cell so color is not important
        1: 'blue',
        2: 'green',
        3: 'red',
        4: 'purple',
        5: 'black',
        6: 'gray',
        7: 'maroon',
        8: 'turquoise',
        9: 'black'
    }
    VALUE_MAP = {
        0: '', 1: '1', 2: '2', 3: '3', 4: '4',
        5: '5', 6: '6', 7: '7', 8: '8', 9: 'X'
    }

    def __init__(self, width, height, callback):
        '''Constructor.'''
        self.width = width
        self.height = height
        self._callback = callback
        self._window = None
        self._table = None
        self._buttons = []
        self._last_hover = None
        self._init_window()
        self._init_table()
        self._bind_events()

    def _init_window(self):
        '''Set up main window.'''
        self._window = tk.Tk()
        self._window.geometry('{}x{}'.format(self.BUTTON_SIZE*self.width,
                                             self.BUTTON_SIZE*self.height))
        self._window.resizable(width=0, height=0)
        self._window.title('Minewseeper')

    def _init_table(self):
        '''Initiate a table.'''
        self._table = tk.Frame(self._window,
                               width=self.BUTTON_SIZE*self.width,
                               height=self.BUTTON_SIZE*self.height)
        self._table.place(x=0, y=0)
        for x in range(self.width):
            self._buttons.append([])
            for y in range(self.height):
                button = tk.Button(self._table, font=self.BUTTON_FONT,
                                   activebackground="SystemButtonFace",
                                   relief=tk.GROOVE)
                button.place(width=self.BUTTON_SIZE, height=self.BUTTON_SIZE,
                             x=self.BUTTON_SIZE * x, y=self.BUTTON_SIZE * y)
                self._buttons[-1].append(button)
                button.coordinates = (x, y)
                button.default_color = 'SystemButtonFace'
                button.shown = False
                button.bind("<Button-1>", lambda x: self._handle_click('L'))
                button.bind("<Button-3>", lambda x: self._handle_click('R'))

    def _handle_click(self, type):
        '''Handle click by passing to the controller callback.'''
        x, y = self._window.winfo_pointerxy()
        button = self._window.winfo_containing(x, y)
        if button:
            self._callback(button.coordinates, type)

    def _on_drag(self, event):
        '''Handle mousemove.'''
        x, y = self._window.winfo_pointerxy()
        button = self._window.winfo_containing(x, y)
        if self._last_hover:
            self._last_hover.configure(bg=self._last_hover.default_color,
                                        activebackground="SystemButtonFace")
        if button and not button.shown:
            self._last_hover = button
            button.configure(bg=self.HOVER_COLOR,
                             activebackground=self.HOVER_COLOR)

    def _bind_events(self):
        '''Bind events for hover and click.'''
        self._window.bind('<Motion>', lambda event: self._on_drag(event))

    def set_table_cell(self, x, y, shown, value):
        '''Change value of a cell in the table.'''
        self._buttons[x][y].configure(text=self.VALUE_MAP[value],
                                      fg=self.COLOR_MAP[value])
        if shown:
            self._buttons[x][y].shown = True
            self._buttons[x][y].default_color = self.SHOWN_COLOR
        else:
            self._buttons[x][y].shown = False
            self._buttons[x][y].default_color = 'SystemButtonFace'
        self._buttons[x][y].configure(bg=self._buttons[x][y].default_color)

    def start(self):
        '''Start main loop.'''
        self._window.mainloop()

if __name__ == '__main__':
    pass
