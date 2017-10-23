import re
printbuffer = []
promptinput = ""
action = ""
location = "Ocean"
Inventory = []
mappos = {"y":0,"x":2}
mapgrid=[["_", "_", "_", "_", "_"],
         ["_", "_", "_", "_", "_"],
         ["_", "_", "_", "_", "_"],
         ["_", "_", "_", "_", "_"],
         ["_", "_", "_", "_", "_"],]

Locations = {
        "Ocean" : {
            "Direction" : {
                "North" : None,
                "East" : None,
                "South" : "Shore",
                "West" : None,
                },
            "Description" : {
                "Neutral" : "You awake on a one-man boat on a roiling sea. The sky is blotched with dark, gray clouds. It fades into the ocean in all directions save to the south. There you see a sliver of dark between the peaks of the waves.",
                },
            "Items" : [{
                    "Name" : "Map", "Visual Description" : "A map of the indian ocean. It from what you can tell your current location is unmarked. You will have to update the map as you go.","Location Description" : "There is what appears to be a rolled up map under the bench.", "Obtainable" : True,
                    },{
                    "Name" : "Oar", "Visual Description" : "A wooden oar that has been worn smooth and shiny from use.","Location Description" : "There is an oar sitting next to you.", "Obtainable" : True,
                    },
                    ],
            "Icon" : "O",
            },
        "Shore" : {
            "Direction" : {
                "North" : "Ocean",
                "East" : None,
                "South" : "Jungle",
                "West" : None,
                },
            "Description" : {
                "Neutral" : "The sand is gray, as is everything. A one-man boat cuts into it near the lapping waves. The sea is north. To the east and west there is more beach. South there is jungle. A bare, black crag juts out from its center.",
                },
            "Items" : [ {
                    "Name" : "Sand", "Visual Description" : "Fine, gray sand.", "Location Description" : "There is sand as far as you can see.", "Obtainable" : True,
                    }],
            "Icon" : "S",
            },
        "Jungle" : {
            "Direction" : {
                "North" : "Shore",
                "East" : None,
                "South" : "Cave",
                "West" : None,
                },
            "Description" : {
                "Neutral" : "The air in the jungle is thick. You can only cut a narrow path through. Huge ferns sweep past your legs as you walk. They could be hiding anything. To the south, almost hidden behind a huge, moss covered rock, you find the entrance to the cave. To the east and west there is more jungle. You can hear the ocean to the north.",
                },
            "Items" :[ {
                    "Name" : "Coconut", "Visual Description" : "A round, Harry coconut.", "Location Description" : "There is a coconut half buried here.", "Obtainable" : True,
                    },
                    {"Name" : "Ferns", "Visual Description" : "The ferns are big and sticky.", "Location Description" : "","Obtainable" : False
                }],
            "Icon" : "J",
            },
        "Cave" : {
            "Direction" : {
                "North" : "Jungle",
                "East" : None,
                "South" : None,
                "West" : None,
                "Hidden" : "Chamber",
                },
            "Description" : {
                "Neutral" : "You are in a dark cave. The walls are wet and slick. After your eyes adjust you can see what appears to be a switch set into the wall high above you.",
                "Effected" : "Everything around you is on fire. There is a large crack to the north. You can see jungle beyond it. To the south there is a low opening.",
                },
            "Items" : {
                },
            "Icon" : "C",
            },
        }

Actions = {
        "Use Coconut on Switch" : {
            "Test" : lambda pi : matchall(["coconut","switch"], pi) and location == "Cave" and checkinventory("Coconut"),
            "Behavior" : lambda pi : [drop("Coconut"), changelocationdescription(location), reassigndirection(location, "South"), addprintbuffer("The coconut leaves your hand in a perfect arch and makes definite contact with the switch then bounces out of sight. A light flickers from somewhere high above the switch then a ring of fire encircles the ceiling of the cave. The fire decends down the oily walls and soon you are surrounded by flames. One the wall of the cave to the south collapses and burns away. It was a false wall.")],
            },
        "Inspect Item" : {
            "Test" : lambda pi : matchany(["inspect","look"], pi) and (matchany(getinventoryitemnames(), pi) or matchany(getlocationitemnames(), pi)),
            "Behavior" : lambda pi : inspectavailableitems(pi),
            },
        "Move North" : {
            "Test" : lambda pi : match("north", pi),
            "Behavior" : lambda pi : move("North"),
            },
        "Move East" : {
            "Test" : lambda pi : match("east", pi),
            "Behavior" : lambda pi : move("East"),
            },
        "Move South" : {
            "Test" : lambda pi : match("south", pi),
            "Behavior" : lambda pi : move("South"),
            },
        "Move West" : {
            "Test" : lambda pi : match("west", pi),
            "Behavior" : lambda pi : move("West"),
            },
        "Pickup Item" :  {
            "Test" : lambda pi : matchany(["take","get","pick","grab"], pi) and matchany(getlocationitemnames(), pi),
            "Behavior" : lambda pi : pickup(matchbyname(pi, getlocationitemnames())),
            },
        "Print Inventory" : {
            "Test" : lambda pi : match("inv", pi),
            "Behavior" : lambda pi : printinventory(),
            },
        }


l = open("pythonlog","w")
def log(string):
    if string == None:
        l.write("\nNone")

    l.write("\n" + repr(string))
def mapupdate():
    mapgrid[mappos["y"]][mappos["x"]]="@"

def inspectavailableitems(p):
    Item = (matchbynameList(p, Inventory) or matchbynameList(p, Locations[location]["Items"]))
    if Item is not None:
        addprintbuffer(Item["Visual Description"])

def addprintbuffer(string):
    printbuffer.append(string)

def clearprintbuffer():
    printbuffer.clear()

def getprintbuffer():
    return printbuffer

def matchbynameList(pattern, l):
    for dic in l:
        if match(dic["Name"], pattern):
            return dic

def matchbyname(pattern, l):
    for string in l:
        if match(string, pattern):
            return string

def reassigndirection(location, direction):
    Locations[location]["Direction"][direction] = Locations[location]["Direction"]["Hidden"]

def changelocationdescription(location):
    Locations[location]["Description"]["Neutral"] = Locations[location]["Description"]["Effected"]

def drop(itemname):
    item=None
    for i in Inventory:
        if itemname == i["Name"]:
            item = i

        if item == i:
            Inventory.remove(item)
            addprintbuffer("You no longer possess " + item["Name"] + ".")

def checkinventory(pattern):
    for i in Inventory:
        if i["Name"] == pattern:
            return True
    return False

def printinventory():
    if bool(Inventory):
        for i in Inventory:
            l=["You have ", i["Name"], "."]
            addprintbuffer("".join(l))
    else:
        addprintbuffer("You have nothing.")

def getinventoryitemnames():
    InvNames=[]
    for i in Inventory:
        InvNames.append(i["Name"])
    return InvNames

def getlocationitemnames():
    LocNames=[]
    for i in Locations[location]["Items"]:
        LocNames.append(i["Name"])
    return LocNames

def match(pattern, string):
    return bool( re.search(r"" + pattern, string, re.I))

def matchany(patternlist, string):
    for i in patternlist:
        if match(i, string) is True:
            return True
    return False


def matchall(patternlist, string):
    for i in patternlist:
        if match(i, string) is False:
            return False
    return True

def pickup(itemname):
    item = None
    for i in Locations[location]["Items"]:
        if itemname == i["Name"] and i["Obtainable"] is True:
            item = i
            Locations[location]["Items"].remove(item)
            Inventory.append(item)
            addprintbuffer("You have obtained " + item["Name"] + ".")
            return

    addprintbuffer("You cannot.")

def move(direction):
    global location
    if Locations[location]["Direction"][direction] is None:
        addprintbuffer("You cannot.")

    else:
        mapgrid[mappos["y"]][mappos["x"]]=Locations[location]["Icon"]
        location = Locations[location]["Direction"][direction]
        if direction == "South":
            mappos["y"]=mappos["y"]+1
        if direction == "North":
            mappos["y"]=mappos["y"]-1
        if direction == "East":
            mappos["x"]=mappos["x"]+1
        if direction == "West":
            mappos["x"]=mappos["x"]-1
def getprompt() :
    addprintbuffer(Locations[location]["Description"]["Neutral"])
    promptitemloop()
    return "\n".join(printbuffer)

def promptitemloop():
    l = []
    if bool(Locations[location]["Items"]) is True :
        for item in Locations[location]["Items"]:
            l.append(item["Location Description"])
        addprintbuffer(" ".join(l))

def findaction(promptinput):
    for key in Actions:
        action = Actions[key]
        if action["Test"](promptinput):
            return action
    return False
#while ( promptinput != "exit" ):
#    print(getprompt())
#    promptinput = input ("What do you do? ")
#    clearprintbuffer()
#    action = findaction(promptinput)
#    if action:
#        action["Behavior"](promptinput)
#    else:
#        addprintbuffer("You cannot.\n\n")


