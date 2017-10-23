import re
printbuffer = ["You're soaked. Have been for hours. There's lightning, but you can't hear the thunder over the constant beat of the rain on the ocean. In the flashes you can see the big houses on Ingrete tumbling down the hillside. Must have been a mudslide. Chop is lapping onto the dock and washing over your ankles. You came to Ricken's because you've already expended your other options. He can get you out and he wants what you've got."]
promptinput = ""
action = ""
location = "Ricken's Door"
Inventory = [{"Name":"Gold Bar", "Visual Description":"Solid gold is heavy and this is a lot of it. There is a trident stamped into the side.","Location Description":"There is a gold bar here. A big one.", "Obtainable":True,}]
mappos = {"y":0,"x":8}
mapgrid=[["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_","_", "_", "_", "_", "_","_", "_", "_", "_", "_",],]
selficon="_"
status=[]

Locations = {
        "Ricken's Door" : {
            "Direction" : {
                "North" : None,
                "East" : None,
                "South" : None,
                "West" : None,
                "Hidden" : "Docks",
                "Hidden2" : "Ricken's Hovel",
                },
            "Description" : {
                "Neutral" : "You stand in front of Ricken's door. It's east of you. His home is a dilapidated shack in a row of dilapidated shacks that line the waterfront. North of you is the docks. The crowd at the boats is impassable. The cobblestone is slippery under your boots.",
                "Effected" :"You stand in front of Ricken's door. It's east of you. His home is a dilapidated shack in a row of dilapidated shacks that line the waterfront. North of you is the docks. Ricken has cleared a path through to the boats. The cobblestone is slippery under your boots.",
                },
            "Items" : [{
                "Name" : "Door", "Visual Description" : "A shoddy wooden door.", "Location Description" : "The door to Ricken's hovel is locked." , "Obtainable" : False, "Open" : False,}
                    ],
            "Icon" : "_",
            "Visited" : True,
            },
        "Ricken's Hovel" : {
            "Direction" : {
                "North" : None,
                "East" : None,
                "South" : None,
                "West" : "Ricken's Door",
                },
            "Description" : {
                "Neutral" : "A small room lit by a mostly open fire with a cast iron pot hung over it. There are rum bottles scattered across the floor. The door to the west leads outside.",
                },
            "Items" : [{
                "Name" : "Ricken", "Visual Description" : "Ricken is a seaman if there ever was one. He has wispy silver hair that matches his moustaches. The moustaches, like his eyes and nose, are thin.", "Location Description" : "Ricken is standing by the fire, drinking.", "Obtainable" : False,},
            {
                "Name" : "Rifle", "Visual Description" : "A long, wooden rifle. You don't know enough to say more about it.", "Location Description" : "", "Obtainable" : True,},
                ],
            "Icon" : "_",
            "Visited":False,
            },
        "Docks" : {
            "Direction" : {
                "North" : None,
                "East" : None,
                "South" : None,
                "West" : None,
                },
            "Description" : {
                "Neutral" : "The entire population of the island is at the docks trying to get passage on a boat. One trawler is inundated with flesh and taking on water. Ricken's men are fending them off with spears. Ricken stands at the edge of his boat with his rifle on his hip waiting for you.",
                },
            "Items" : [
                ],
            "Icon" : "_",
            "Visited":False,
            "First Visit Text" : "As the crowd encroahces on his boat, Ricken fires his rifle into the air. The scene goes quiet except for one woman with a baby. She sees you waiver as you board and she pleads for you to take the child. You look away and she pushes it under your arm. You throw your hands up and the kid goes into the drink. She goes onto her knees. Two of the men leap at you."
            },
        "Unconscious" : {
            "Direction" : {
                "North" : None,
                "East" : None,
                "South" : None,
                "West" : None,
                },
            "Description" : {
                "Neutral" : "You are unconscious.",
                },
            "Items" : [
                ],
            "Icon" : "_",
            "Visited":False,
            },
        "Ocean" : {
            "Direction" : {
                "North" : None,
                "East" : None,
                "South" : "Shore",
                "West" : None,
                },
            "Description" : {
                "Neutral" : "You are on a one-man boat on a roiling sea. The sky is blotched with dark, gray clouds. It fades into the ocean in all directions save to the south. There you see a sliver of dark between the peaks of the waves.",
                },
            "Items" : [{
                    "Name" : "Map", "Visual Description" : "A map of the indian ocean. From what you can tell, your current location is unmarked. You will have to update the map as you go.","Location Description" : "There is what appears to be a rolled up map under the bench.", "Obtainable" : True,
                    },{
                    "Name" : "Oar", "Visual Description" : "A wooden oar that has been worn smooth and shiny from use.","Location Description" : "There is an oar sitting next to you.", "Obtainable" : True,
                    },
                    ],
            "Icon" : "\u223F",
            "Visited" : True,
            },
        "Shore" : {
            "Direction" : {
                "North" : "Ocean",
                "East" : None,
                "South" : "Jungle",
                "West" : None,
                },
            "Description" : {
                "Neutral" : "The sand is gray, as is everything. A one-man boat cuts into it near the lapping waves. The sea is north. To the east and west there is more beach. South there is a path into the jungle. A bare, black crag juts out from its center.",
                },
            "Items" : [ {
                    "Name" : "Sand", "Visual Description" : "Fine, gray sand.", "Location Description" : "There is sand as far as you can see.", "Obtainable" : True,
                    }],
            "Icon" : "\u2592",
            "Visited":False,
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
                    {"Name" : "Ferns", "Visual Description" : "The ferns are oozing a clear, sticky substance.", "Location Description" : "","Obtainable" : True,
                }],
            "Icon" : "J",
            "Visited":False,
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
            "Visited":False,
            },
        }

Actions = {
        "Talk to Ricken" : {
            "Test" : lambda pi : matchall(["talk","ricken"], pi) and location == "Ricken's Hovel" and checkinventory("Gold Bar"),
            "Behavior" : lambda pi : addprintbuffer(""""Take me with you," you plead. The storm bursts the window and sheets of rain crash on your faces. Ricken's voice is plodding. "Boat holds four." "Leave the others," you stammer, "Just take me. I'm a doctor. Who knows how long it'll be until you get picked up?" Ricken's face doesn't change. He says, "Show it to me." """),
            },
        "Give Ricken Gold Bar" : {
            "Test" : lambda pi : matchall(["ricken","gold bar"], pi) and location == "Ricken's Hovel",
            "Behavior" : lambda pi : [addprintbuffer("You stare at eachother. Your body shakes. The place is coming down around you. You start to pull the gold bar from your pocket. The orange light from the fire gleams against the trident emblem stamped into the side of the bar. When Ricken sees it he pushes the bar back into your pocket and retrieves two rifles from a case over the mantle. He hands you one of them then walks out to the docks."),pickup("Rifle"),reassigndirection("Ricken's Door","North","Hidden", ),changelocationdescription("Ricken's Door", "Effected"),removericken()]
            },
        "Fire Rifle" : {
            "Test" : lambda pi : matchany(["shoot","fire","rifle","gun",],pi) and location == "Docks",
            "Behavior" : lambda pi : [addprintbuffer("You kill one of the men. Ricken gets two more. The lightning starts again and you can see the worst of it now in strobes--billowing dark clouds the size of mountains, paradise coming down around you. A knife goes into your thigh and you slip in the blood. Your boat pushes off and away. You can see the mother treading water. You see a figure through your fogged glasses. It outlines a beast with tendrils thirty stories high but then it's a wave coming over the top of Ingrete. You are the only one looking back when Siere Marta is washed away by the sea. The wave breaks in front of you and your boat rides the swell high into the air. You lose consciousness."), gounconscious()]
                },
        "Use Coconut on Switch" : {
            "Test" : lambda pi : matchall(["coconut","switch"], pi) and location == "Cave" and checkinventory("Coconut"),
            "Behavior" : lambda pi : [drop("Coconut"), changelocationdescription(location, "Effected"), reassigndirection(location, "South", "Hidden",), addprintbuffer("The coconut leaves your hand in a perfect arch and makes definite contact with the switch then bounces out of sight. A light flickers from somewhere high above the switch then a ring of fire encircles the ceiling of the cave. The fire decends down the oily walls and soon you are surrounded by flames. One the wall of the cave to the south collapses and burns away. It was a false wall.")],
            },
        "Knock On Ricken's Door" : {
            "Test" : lambda pi : location == "Ricken's Door" and matchany(["Knock","rap","tap",],pi) and Locations["Ricken's Door"]["Items"][0]["Open"]==False,
            "Behavior" : lambda pi : openrickensdoor(),
            },
        "Wake Up" : {
            "Test" : lambda pi : match("wake",pi) and location == "Unconscious",
            "Behavior" : lambda pi : wakeup(),
            },
        "Use Ferns On Leg" : {
            "Test" : lambda pi : checkinventory("Ferns") and checkstatus("Laceration in Right Thigh (Bandaged--Bleeding)") and match("ferns", pi) and matchany(["leg","bandage","wound","laceration"],pi),
            "Behavior" : lambda pi : usefernsonleg(),
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
def usefernsonleg():
    global status
    for n, s in enumerate(status):
        if s=="Laceration in Right Thigh (Bandaged--Bleeding)":
            del status[n]
            addprintbuffer("You rub the oozing fern on the wound in your leg and it causes a cool, numbing sensation. The bleeding has stopped.")
def openrickensdoor():
    for i in Locations["Ricken's Door"]["Items"]:
        if i["Name"] == "Door":
            i["Open"]=True
            i["Location Description"]="The door to Ricken's Hovel is open."
    reassigndirection("Ricken's Door","East","Hidden2")
    addprintbuffer("You rap on Ricken's door twelve times before he opens it and bids you come in.")
def removericken():
    global Locations
    Locations[location]["Items"]=[]
def wakeup():
    global status
    for n, s in enumerate(status):
        if s == "Unconscious":
            del status[n]
    for n, s in enumerate(status):
        if s =="Laceration in Right Thigh":
            status[n]="Laceration in Right Thigh (Bandaged--Bleeding)"
    global selficon
    selficon="@"
    global mappos
    mappos = {"y":0,"x":8}
    global location
    location = "Ocean"
    addprintbuffer("You wake up and fling your head over the side of the boat, vomiting into the ocean. Your leg hurts bad. It's been wrapped in cloth, but it's still bleeding. It needs some sort of ointment to stop it. You are alone.")

def gounconscious():
    global location
    global Inventory
    global status
    status.append("Laceration in Right Thigh")
    status.append("Unconscious")
    Inventory = []
    location = "Unconscious"

def docks():
    Locations["Ricken's Door"]["Direction"]["North"] = Locations["Ricken's Door"]["Direction"]["Hidden"]

def mapupdate():
    mapgrid[mappos["y"]][mappos["x"]]=selficon

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

def reassigndirection(location, direction, newdirection):
    Locations[location]["Direction"][direction] = Locations[location]["Direction"][newdirection]

def changelocationdescription(l, description):
    Locations[l]["Description"]["Neutral"] = Locations[l]["Description"][description]

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

def checkstatus(pattern):
    for i in status:
        if i == pattern:
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
        if Locations[location]["Visited"]==False:
            Locations[location]["Visited"]=True
            try:
                addprintbuffer(Locations[location]["First Visit Text"])
            except KeyError:
                addprintbuffer("")
        if direction == "South":
            mappos["y"]=mappos["y"]+1
        if direction == "North":
            mappos["y"]=mappos["y"]-1
        if direction == "East":
            mappos["x"]=mappos["x"]+1
        if direction == "West":
            mappos["x"]=mappos["x"]-1
def getprompt() :
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


