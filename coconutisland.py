import curses
import startdata
import textwrap
import datetime
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

height,width = stdscr.getmaxyx()

while (promptinput != "exit"):
    stdscr.clear()
    stdscr.refresh()
    startdata.time+=1
    startdata.mapupdate()
    startdata.setstats()
    stdscr.addstr(0,0, "Coconut Island - A Python Text Adventure by Matt S Underwood", curses.A_REVERSE)
    stdscr.hline(" ",width,curses.A_REVERSE)
    stdscr.move(0,divmod(width,2)[0])
    stdscr.vline(" ",height-1,curses.A_REVERSE)
    stdscr.addstr(divmod(height,2)[0], 1, startdata.location, curses.A_REVERSE)
    for i, j in enumerate(textwrap.wrap(startdata.Locations[startdata.location]["Description"]["Neutral"],width=divmod(width,2)[0]-4)):
        stdscr.addstr(divmod(height,2)[0]+2+(2*i),2, j)
    for i, j in enumerate(textwrap.wrap(startdata.getprompt(),width=divmod(width,2)[0]-4)):
        stdscr.addstr(2+(2*i),2, j)
    for item in startdata.Inventory:
        if item["Name"]=="Map":

            stdscr.move(3,divmod(width,2)[0]+6,)
            stdscr.hline("_",31)
            stdscr.move(18,divmod(width,2)[0]+6,)
            stdscr.hline("_",31)
            stdscr.move(4,divmod(width,2)[0]+5)
            stdscr.vline("|",15)
            stdscr.move(4,divmod(width,2)[0]+37)
            stdscr.vline("|",15)

            stdscr.addstr(2, divmod(width,2)[0]+2, "    M A P    ", curses.A_REVERSE)
            stdscr.addstr(4, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[0]))
            stdscr.addstr(5, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[1]))
            stdscr.addstr(6, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[2]))
            stdscr.addstr(7, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[3]))
            stdscr.addstr(8, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[4]))
            stdscr.addstr(9, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[5]))
            stdscr.addstr(10, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[6]))
            stdscr.addstr(11, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[7]))
            stdscr.addstr(12, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[8]))
            stdscr.addstr(13, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[9]))
            stdscr.addstr(14, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[10]))
            stdscr.addstr(15, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[11]))
            stdscr.addstr(16, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[12]))
            stdscr.addstr(17, divmod(width,2)[0]+7, " ".join(startdata.mapgrid[13]))


    stdscr.addstr (20,divmod(width,2)[0]+2,"    I N V E N T O R Y    ", curses.A_REVERSE)
    if len(startdata.Inventory) != 0:
        stdscr.addstr (21,divmod(width,2)[0]+2,", ".join(startdata.getinventoryitemnames()))


    stdscr.addstr (24,divmod(width,2)[0]+2,"    S T A T U S    ", curses.A_REVERSE)
    if len(startdata.status) != 0:
        stdscr.addstr (25,divmod(width,2)[0]+2,", ".join(startdata.status))
    stdscr.addstr(28, divmod(width,2)[0]+2, "BLOOD")
    stdscr.addstr(29, divmod(width,2)[0]+2, "".join(startdata.bloodbar),)
    stdscr.addstr(30, divmod(width,2)[0]+2, "STAMINA")
    stdscr.addstr(31, divmod(width,2)[0]+2, "".join(startdata.staminabar),)
    stdscr.addstr(32, divmod(width,2)[0]+2, "MOBILITY")
    stdscr.addstr(33, divmod(width,2)[0]+2, "".join(startdata.mobilitybar),)
    stdscr.addstr(34, divmod(width,2)[0]+2, "TEMPERATURE")
    stdscr.addstr(35, divmod(width,2)[0]+2, "".join(startdata.temperaturebar),)
    stdscr.addstr(36, divmod(width,2)[0]+2, "THIRST")
    stdscr.addstr(37, divmod(width,2)[0]+2, "".join(startdata.thirstbar),)
    stdscr.addstr(38, divmod(width,2)[0]+2, "HUNGER")
    stdscr.addstr(39, divmod(width,2)[0]+2, "".join(startdata.hungerbar),)


    stdscr.addstr(height-2,1, "What do you do?",curses.A_REVERSE)
    stdscr.hline(" ",width,curses.A_REVERSE)
    if startdata.checklocalinventory("Sundial") is True and startdata.Locations[startdata.location]["Access"]=="Shore" and startdata.daynight() is "Day":
        startdata.addprintbuffer("IN FUNC")
        stdscr.addstr(43, divmod(width,2)[0]+2, str(datetime.timedelta(minutes=(startdata.time*20))), curses.A_REVERSE)
    if startdata.daynight() is "Day":
        stdscr.addstr(42, divmod(width,2)[0]+2, "It is day.", curses.A_REVERSE)
    else:
        stdscr.addstr(42, divmod(width,2)[0]+2, "It is night." )
    promptinput = stdscr.getstr(height-1,1, 30).decode(encoding="utf-8")
    startdata.clearprintbuffer()
    action = startdata.findaction(promptinput)
    if action:
        action["Behavior"](promptinput)
    else:
        startdata.addprintbuffer("You cannot.")
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
