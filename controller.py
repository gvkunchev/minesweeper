from model import Table, Content
from view import GUI


class Minesweeper:
    '''Minesweeper controller.'''

    def __init__(self, width, height, mine_count):
        '''Constructor.'''
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self._end = False
        self.model = Table(width, height, mine_count)
        self.gui = GUI(width, height,
                       lambda pos, type: self._handle_click(pos, type))
        self._sync_content()
        self.gui.start()

    def _sync_content(self):
        '''Sync model's content to GUI.'''
        for x in range(self.width):
            for y in range(self.height):
                cell = self.model.cells[x][y]
                if not cell.shown:
                    self.gui.set_table_cell(x, y, cell.shown,
                                            Content.empty.value)
                elif cell.marked:
                    self.gui.set_table_cell(x, y, cell.shown,
                                            Content.mine.value)
                else:
                    self.gui.set_table_cell(x, y, cell.shown,
                                            cell.content.value)

    def _handle_click(self, coordinates, type):
        '''Handle click on a button from the GUI.'''
        cell = self.model.cells[coordinates[0]][coordinates[1]]
        if type == 'R':
            cell.marked = not cell.marked
            cell.shown = cell.marked
        elif type == 'L':
            if cell.marked:
                return
            if cell.content == Content.mine:
                for x in range(self.width):
                    for y in range(self.height):
                        self.model.cells[x][y].shown = True
                print('Game over')
                self._end = True
            elif cell.content == Content.empty:
                self._propagate_click(cell)
            else:
                cell.shown = True
        self._sync_content()
        self._check_win()

    def _propagate_click(self, cell):
        '''Show all empty neighbouts of a cell.'''
        if not cell.marked:
            cell.shown = True
        for neighbour in self.model.get_neightbours(cell):
            if not neighbour.marked:
                if neighbour.content == Content.empty and not neighbour.shown:
                    self._propagate_click(neighbour)
                neighbour.shown = True

    def _check_win(self):
        '''Check for a win.'''
        if self._end:
            return False
        for x in range(self.width):
            for y in range(self.height):
                cell = self.model.cells[x][y]
                if cell.content not in (Content.empty, Content.mine):
                    if not cell.shown:
                        return False
        self._end = True
        print('You win')
        return True


if __name__ == '__main__':
    ms = Minesweeper(20, 20, 25)
