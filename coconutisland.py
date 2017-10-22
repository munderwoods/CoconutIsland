import curses
import ifgame
import textwrap
promptinput=""
stdscr = curses.initscr()
curses.noecho()
curses.nocbreak()
stdscr.keypad(False)
curses.echo()

from curses import wrapper


begin_x = 20; begin_y = 7
height = 5; width = 10
while (promptinput != "exit"):
    stdscr.clear()
    stdscr.border(0)
    stdscr.refresh()
    win = curses.newwin(height, width, begin_y, begin_x)
    ifgame.mapupdate()
    stdscr.addstr(1,1, "Coconut Island - A Python Text Adventure")
    stdscr.addstr(3, 1, ifgame.location, curses.A_REVERSE)

    for i, j in enumerate(textwrap.wrap(ifgame.getprompt())):
        stdscr.addstr(5+(2*i),2, j)
    for item in ifgame.Inventory:
        if item["Name"]=="Map":

            stdscr.addstr (3, 101, "    M A P    ", curses.A_REVERSE)
            stdscr.addstr(4, 103, " ".join(ifgame.mapgrid[0]))
            stdscr.addstr(5, 103, " ".join(ifgame.mapgrid[1]))
            stdscr.addstr(6, 103, " ".join(ifgame.mapgrid[2]))
            stdscr.addstr(7, 103, " ".join(ifgame.mapgrid[3]))
            stdscr.addstr(8, 103, " ".join(ifgame.mapgrid[4]))


    if len(ifgame.Inventory) != 0:
        stdscr.addstr (21,95,"    I N V E N T O R Y    ", curses.A_REVERSE)
        stdscr.addstr (22,95,", ".join(ifgame.getinventoryitemnames()))
    stdscr.addstr(21,1, "What do you do?")
    promptinput = stdscr.getstr(22,1, 30).decode(encoding="utf-8")
    ifgame.clearprintbuffer()
    action = ifgame.findaction(promptinput)
    if action:
        action["Behavior"](promptinput)
    else:
        ifgame.addprintbuffer("You Cannot.")
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
