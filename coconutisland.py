import curses
import startdata
import textwrap
promptinput=""
stdscr = curses.initscr()
curses.noecho()
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
import simpleaudio as sa


from curses import wrapper

wave_obj = sa.WaveObject.from_wave_file("/home/matt/coconutisland/thunder.wav")
play_obj = wave_obj.play()

begin_x = 20; begin_y = 7
height = 5; width = 10
while (promptinput != "exit"):
    stdscr.clear()
    stdscr.border(0)
    stdscr.refresh()
    win = curses.newwin(height, width, begin_y, begin_x)
    startdata.mapupdate()
    stdscr.addstr(1,1, "Coconut Island - A Python Text Adventure")
    stdscr.move(2,1)
    stdscr.hline("_",40)
    stdscr.addstr(24, 1, startdata.location, curses.A_REVERSE)
    for i, j in enumerate(textwrap.wrap(startdata.Locations[startdata.location]["Description"]["Neutral"])):
        stdscr.addstr(26+(2*i),2, j)
    for i, j in enumerate(textwrap.wrap(startdata.getprompt())):
        stdscr.addstr(4+(2*i),2, j)
    for item in startdata.Inventory:
        if item["Name"]=="Map":

            stdscr.addstr(3, 95, "    M A P    ", curses.A_REVERSE)
            stdscr.addstr(5, 100, " ".join(startdata.mapgrid[0]))
            stdscr.addstr(6, 100, " ".join(startdata.mapgrid[1]))
            stdscr.addstr(7, 100, " ".join(startdata.mapgrid[2]))
            stdscr.addstr(8, 100, " ".join(startdata.mapgrid[3]))
            stdscr.addstr(9, 100, " ".join(startdata.mapgrid[4]))
            stdscr.addstr(10, 100, " ".join(startdata.mapgrid[5]))
            stdscr.addstr(11, 100, " ".join(startdata.mapgrid[6]))
            stdscr.addstr(12, 100, " ".join(startdata.mapgrid[7]))
            stdscr.addstr(13, 100, " ".join(startdata.mapgrid[8]))
            stdscr.addstr(14, 100, " ".join(startdata.mapgrid[9]))
            stdscr.addstr(15, 100, " ".join(startdata.mapgrid[10]))
            stdscr.addstr(16, 100, " ".join(startdata.mapgrid[11]))
            stdscr.addstr(17, 100, " ".join(startdata.mapgrid[12]))
            stdscr.addstr(18, 100, " ".join(startdata.mapgrid[13]))

    if len(startdata.Inventory) != 0:
        stdscr.addstr (21,95,"    I N V E N T O R Y    ", curses.A_REVERSE)
        stdscr.addstr (22,95,", ".join(startdata.getinventoryitemnames()))

    if len(startdata.status) != 0:
        stdscr.addstr (25,95,"    S T A T U S    ", curses.A_REVERSE)
        stdscr.addstr (26,95,", ".join(startdata.status))

    stdscr.addstr(42,1, "What do you do?")
    promptinput = stdscr.getstr(43,1, 30).decode(encoding="utf-8")
    startdata.clearprintbuffer()
    action = startdata.findaction(promptinput)
    if action:
        action["Behavior"](promptinput)
    else:
        startdata.addprintbuffer("You Cannot.")
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
