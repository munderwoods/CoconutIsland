from cursed import CursedApp, CursedWindow
import ifgame
import textwrap
# the main context of the curses application
app = CursedApp()

# Derive from CursedWindow to declare curses windows to be created after app.run()
# It is required to declare X, Y, WIDTH, and HEIGHT for each window.
# You'll want to put the main looping code for each window thread in the `update` class function.

class MapWindow(CursedWindow):
    X, Y = (0 , 25)
    WIDTH, HEIGHT = (75, 25)
    BORDERED = True
    @classmethod
    def update(cls):
        cls.hline(0,21,"_",71)
        cls.addstr("                                                                       ", 1, 22)
        cls.addstr (", ".join(ifgame.getinventoryitemnames()), 1, 22)


class MainWindow(CursedWindow):

    # Coordinate for top-left of window.
    X, Y = (0, 0)

    # WIDTH and HEIGHT can be 'max' or integers.
    WIDTH, HEIGHT = (75, 25)

    # Create a default border around the window.
    BORDERED = True


    @classmethod
    def update(cls):
        ''' update runs every tick '''

        # Hello world printed at x,y of 0,0
        for i, j in enumerate(textwrap.wrap(ifgame.getprompt())):
            cls.addstr(j,  1, 0+(2*i))

        cls.hline(0,21,"_",71)

        promptinput = cls.getstr(1, 22, "What do you do? ")

        ifgame.clearprintbuffer()

        action = ifgame.findaction(promptinput)

        if action:
            action["Behavior"](promptinput)
        else:
            ifgame.addprintbuffer("You cannot.")
        cls.redraw()

        # Get character keycode of keypress, or None.
        if cls.getch() == 27:
            # Escape was pressed. Quit.
            # 'quit' must be triggered for each open window for the program to quit.
            # Call cls.trigger('quit') to quit the window you're in, and to quit the other
            # declared windows, call OtherWindow.trigger('quit') which will run in that
            # window's thread, regardless of where it's called.
            cls.trigger('quit')

class MapWindow(CursedWindow):
    X, Y = (75 , 0)
    WIDTH, HEIGHT = (75, 25)
    BORDERED = True
    @classmethod
    def update(cls):
        cls.hline(0,21,"_",71)
        cls.addstr("                                                                       ", 1, 22)
        cls.addstr (", ".join(ifgame.getinventoryitemnames()), 1, 22)




# To trigger app to start
result = app.run()

# check if ctrl-C was pressed
if result.interrupted():
    print('Quit!')
else:
    # Raises an exception if any thread ran into a different exception.
    result.unwrap()
