import re
import datetime
from copy import deepcopy
printbuffer = ["You're soaked. Have been for hours. There's lightning, but you can't hear the thunder over the constant beat of the rain on the ocean. In the flashes you can see the big houses on Ingrete tumbling down the hillside. Must have been a mudslide. Chop is lapping onto the dock and washing over your ankles. You came to Ricken's because you've already expended your other options. He can get you out and he wants what you've got."]
promptinput = ""
action = ""
location = "Ricken's Door"
Inventory = [{"Name":"Gold Bar", "Visual Description":"Solid gold is heavy and this is a lot of it. There is a trident stamped into the side.","Location Description":"There is a gold bar here. A big one.", "Obtainable":1, "Edible": False,}]
MaxInventorySize=4
mappos = {"y":0,"x":8}
mapgrid=[["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],
         ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",],]
selficon="_"
status=[]
blood = 10
bloodbar=[]
stamina = 10
staminabar=[]
mobility = 10
mobilitybar=[]
temperature = 5
temperaturebar=[]
thirst = 10
thirstmod=3
thirstfloor=1
thirstbar=[]
hunger = 10
hungermod=10
hungerfloor=1
hungerbar=[]
bloodmod=1
bloodfloor=2
staminamod=1
staminafloor=1
mobilitymod=1
mobilityfloor=1
makeables=[{"Name" : "Fire","Visual Description" : "A small fire. It offers meager warmth.", "Location Description" : "There is a fire here.", "Obtainable" : 0,"Edible": False,},
        {"Name" : "Sundial","Visual Description" : "A stick protruding from the sand. The shadow coming off of the stick indicates the time of day. Only works where sunlight is present.", "Location Description" : "There is a sundial here.", "Obtainable" : 0,"Edible": False,},
        {"Name":"Pack", "Visual Description":"A crude packpack you crafted out of an old shipmast and some vines. It carries little and looks like it might fall apart from a slight jossling.","Location Description":"There is a pack here.", "Obtainable":1,"Edible": False,}]

time=65
hours=0

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
                "Name" : "Door", "Visual Description" : "A shoddy wooden door.", "Location Description" : "The door to Ricken's hovel is locked." , "Obtainable" : 0, "Open" : False,"Edible": False,}
                    ],
            "Icon" : "_",
            "Visited" : True,
            "Temperature" : 5,
            "Access" : "Open",
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
                "Name" : "Ricken", "Visual Description" : "Ricken is a seaman if there ever was one. He has wispy silver hair that matches his moustaches. The moustaches, like his eyes and nose, are thin.", "Location Description" : "Ricken is standing by the fire, drinking.", "Obtainable" : 0,"Edible": False,},
            {
                "Name" : "Rifle", "Visual Description" : "A long, wooden rifle. You don't know enough to say more about it.", "Location Description" : "", "Obtainable" : 1,"Edible": False,},
                ],
            "Icon" : "_",
            "Visited":False,
            "Temperature" : 6,
            "Access" : "Open",
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
            "First Visit Text" : "As the crowd encroahces on his boat, Ricken fires his rifle into the air. The scene goes quiet except for one woman with a baby. She sees you waiver as you board and she pleads for you to take the child. You look away and she pushes it under your arm. You throw your hands up and the kid goes into the drink. She goes onto her knees. Two of the men leap at you.",
            "Temperature" : 5,
            "Access" : "Open",
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
            "Temperature" : 5,
            "Access" : "Open",
            },
        "Ocean" : {
            "Direction" : {
                "North" : None,
                "East" : None,
                "South" : "Shore",
                "West" : None,
                },
            "Description" : {
                "Neutral" : "You are on a small boat on a roiling sea. The sky is blotched with dark, gray clouds. It fades into the ocean in all directions save to the south. There you see a sliver of dark between the peaks of the waves.",
                },
            "Items" : [
                    ],
            "Icon" : "\u223F",
            "Visited" : False,
            "Temperature" : 5,
            "Access" : "Water",
            },
        "Shore" : {
            "Direction" : {
                "North" : "Ocean",
                "East" : None,
                "South" : "Jungle",
                "West" : "Delta",
                },
            "Description" : {
                "Neutral" : "The sand is gray, as is everything. The sea is north. To the east and west there is more beach. South there is a path into the jungle. A bare, black crag juts out from its center.",
                },
            "Items" : [ {
                "Name" : "Sand", "Visual Description" : "Fine, gray sand.", "Location Description" : "There is sand here.", "Obtainable" : 2,"Edible": False,
                    },
                    {
                        "Name" : "Boat", "Visual Description" : "It's got room for four crew or some small cargo.", "Location Description" : "There is a boat here.", "Obtainable" : 0,"Edible": False, "Holding": [{
                            "Name" : "Map", "Visual Description" : "A map of the indian ocean. From what you can tell, your current location is unmarked. You will have to update the map as you go.","Location Description" : "There is what appears to be a rolled up map here.", "Obtainable" : 1,"Edible": False,
                    },{
                        "Name" : "Oar", "Visual Description" : "A wooden oar that has been worn smooth and shiny from use.","Location Description" : "There is an oar sitting next to you.", "Obtainable" : 1,"Edible": False,
                    },],
                    },],
            "Icon" : "\u2592",
            "Visited":True,
            "Temperature" : 5,
            "Access" : "Shore",
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
                "Name" : "Coconut", "Visual Description" : "A round, Harry coconut.", "Location Description" : "There is a coconut half buried here.", "Obtainable" : 1,"Edible": False,
                    },
                    {"Name" : "Ferns", "Visual Description" : "The ferns are oozing a clear, sticky substance.", "Location Description" : "There are sticky ferns here.","Obtainable" : 2,"Edible": False,
                },{
                    "Name" : "Wood", "Visual Description" : "A small bit of wood.", "Location Description" : "There is wood here.", "Obtainable" : 2,"Edible": False,
                },{
                    "Name" : "Vines", "Visual Description" : "Some long, thin vines that curl around the trees here. They are dark green and shine in the sunlight.", "Location Description" : "There are some vines here.", "Obtainable" : 2,"Edible": False,                }],
            "Icon" : "J",
            "Visited":False,
            "Temperature" : 5,
            "Access" : "Open",
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
            "Items" :
                [],
            "Icon" : "C",
            "Visited":False,
            "Temperature" : 4,
            "Access" : "Open",
            },
        "Chamber" : {
            "Direction" : {
                "North" : "Cave",
                "East" : None,
                "South" : None,
                "West" : None,
                "Hidden" : None,
                },
            "Description" : {
                "Neutral" : "This is a smaller cave. The walls are jagged and shiny.",
                "Effected" : "",
                },
            "Items" :
            [{"Name" : "Flint", "Visual Description" : "A shiny, smooth stone with sharp edges.", "Location Description" : "There is flint here.", "Obtainable" : 2,"Edible": False,}],
            "Icon" : "F",
            "Visited":False,
            "Temperature" : 4,
            "Access" : "Open",
            },
        "Delta" : {
            "Direction" : {
                "North" : None,
                "East" : "Shore",
                "South" : None,
                "West" : None,
                },
            "Description" : {
                "Neutral" : "A narrow but deep river meets the sea here. There is some vegetation around the edges, but nothing of any apparent use. To the east is a stretch of beach. North is the ocean. The river continues south. There is thick vegetation surrounding it, but you could make your way through.",
                },
            "Items" : [ {
                "Name" : "Water", "Visual Description" : "The water is clear and looks refreshing.", "Location Description" : "The water appears clean and drinkable.", "Obtainable" : 2,"Edible": False,
                    },{
                "Name" : "Berries", "Visual Description" : "Small, red berries.", "Location Description" : "There are some wild berries here.", "Obtainable" : 2,"Edible": True,
                    },{
                        "Name" : "Cloth", "Visual Description" : "It appears to be a piece of an old ship mast.", "Location Description" : "There is some tattered cloth here.", "Obtainable" : 1,"Edible": False,
                    },
                    ],
            "Icon" : "V",
            "Visited":False,
            "Temperature" : 5,
            "Access" : "Shore",
            },

        }











Actions = {
        "Talk to Ricken" : {
            "Test" : lambda pi : matchany(["talk","speak"], pi) and location == "Ricken's Hovel" and checkinventory("Gold Bar"),
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
            "Behavior" : lambda pi : [drop("Coconut"),changetemp("Cave", 10), changelocationdescription(location, "Effected"), reassigndirection(location, "South", "Hidden",), addprintbuffer("The coconut leaves your hand in a perfect arch and makes definite contact with the switch. A light flickers from somewhere high above the switch then a ring of fire encircles the ceiling of the cave. The fire decends down the oily walls and soon you are surrounded by flames. One the wall of the cave to the south collapses and burns away. It was a false wall.")],
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
            "Test" : lambda pi : checkavailableitems("Ferns") and checkstatus("Laceration") and matchany(["bandage","wound","laceration","cut"],pi),
            "Behavior" : lambda pi : usefernsonleg(),
            },
        "Drink" : {
            "Test" : lambda pi : checkavailableitems("Water") and matchany(["drink"],pi),
            "Behavior" : lambda pi : drink(),
            },
        "Eat" : {
            "Test" : lambda pi : match("eat",pi),
            "Behavior" : lambda pi : eat(pi),
            },
        "Inspect Item" : {
            "Test" : lambda pi : matchany(["inspect","look"], pi) and (matchany(getinventoryitemnames(), pi) or matchany(getlocationitemnames(), pi)),
            "Behavior" : lambda pi : inspectavailableitems(pi),
            },
        "Drop Item" : {
            "Test" : lambda pi : match("drop", pi) and (matchany(getinventoryitemnames(), pi) or matchany(getlocationitemnames(), pi)),
            "Behavior" : lambda pi : drop(pi),
            },
        "Put in Boat" : {
            "Test" : lambda pi : matchall(["put","boat"], pi) and (matchany(getinventoryitemnames(), pi) or matchany(getlocationitemnames(), pi)),
            "Behavior" : lambda pi : putinboat(pi),
            },
        "Start Fire" : {
            "Test" : lambda pi : checkavailableitems("Wood") and checkavailableitems("Flint") and matchany(["use","make","build","Construct","start"],pi) and (match("Fire",pi) or (matchall(["wood","flint"],pi))),
            "Behavior" : lambda pi : [make("Fire"), removeitem("Wood"),removeitem("Flint"),],
            },
        "Make Sundial" : {
            "Test" : lambda pi : checkavailableitems("Wood") and checkavailableitems("Sand") and matchany(["use","make","build","Construct","start"],pi) and (match("Sundial",pi) or (matchall(["wood","sand"],pi))),
            "Behavior" : lambda pi : [make("Sundial"), removeitem("Wood"),removeitem("Sand"),],
            },
        "Make Pack" : {
            "Test" : lambda pi : checkavailableitems("Cloth") and checkavailableitems("Vines") and matchany(["use","make","build","Construct","start"],pi) and (match("Pack",pi) or (matchall(["cloth","vines"],pi))),
            "Behavior" : lambda pi : [make("Pack"), removeitem("cloth"),removeitem("vines"),],
                                                    },
        "Move Northn" : {
            "Test" : lambda pi : n("n", pi),
            "Behavior" : lambda pi : move("North"),
            },
        "Move Easte" : {
            "Test" : lambda pi : n("e", pi),
            "Behavior" : lambda pi : move("East"),
            },
        "Move Souths" : {
            "Test" : lambda pi : n("s", pi),
            "Behavior" : lambda pi : move("South"),
            },
        "Move Westw" : {
            "Test" : lambda pi : n("w", pi),
            "Behavior" : lambda pi : move("West"),
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
        "Wait" : {
            "Test" : lambda pi : matchany(["wait","rest","sleep"],pi),
            "Behavior" : lambda pi:addprintbuffer("Time passes."),
            },
        }


l = open("pythonlog","w")
def log(string):
    if string == None:
        l.write("\nNone")

    l.write("\n" + repr(string))

def drink():
    global thirst
    thirst=10
    removeitem("Water")
    addprintbuffer("You drink the water and it refreshes you.")

def checkitemtrait(trait, itemname):
    Item=list(filter(lambda x: x["Name"]==itemname, getavailableitems()))
    return bool(len(list(filter(lambda x: x[trait] is True, Item)))!=0)

def eat(PI):
    global hunger
    itemname=matchbyname(PI,getlocationitemnames())
    if itemname==None:
        itemname=matchbyname(PI,getinventoryitemnames())
    if itemname==None:
        addprintbuffer("You cannot.")
        return
    if itemname != None:
        if checkitemtrait("Edible",itemname):
            hunger=10
            addprintbuffer("You have eaten " + itemname + ".")
            removeitem(itemname)
            return
    else:
        addprintbuffer("That is not edible.")
        return
    addprintbuffer("You cannot.")
    return


def removeitem(item):
    boat=None
    for b in Locations[location]["Items"]:
        if b["Name"]=="Boat":
            boat=b
    for a, x in enumerate(Inventory):
        if x["Name"]==item and x["Obtainable"] != 2:
            del Inventory[a]
    for b, y in enumerate(Locations[location]["Items"]):
        if y["Name"]==item and y["Obtainable"] != 2:
            del Locations[location]["Items"][b]
    if boat is not None:
        for c in Locations[location]["Items"]:
            if c["Name"]=="Boat":
                for d, z in enumerate(c["Holding"]):
                    if z["Name"]==item and z["Obtainable"] != 2:
                        del c["Holding"][d]

def make(thing):
    for i in makeables:
        if i["Name"]==thing:
            addprintbuffer("You have made "+thing+".")
            if i["Obtainable"] == 1:
                Inventory.append(i)
            else:
                Locations[location]["Items"].append(i)

def daynight():
    global hours
    td=datetime.timedelta(minutes=(time*20))
    hours, remainder = divmod(td.seconds,3600)
    if hours >= 6 and hours <22:
        return "Day"
    if hours >= 22 or hours >=0 and hours < 6 :
        return "Night"

def changetemp(location, temp):
    Locations[location]["Temperature"]=temp

def dead():
    global promptinput
    clearprintbuffer()
    addprintbuffer("You died.")
    print("You died")
    1/0


def setstats():
    global MaxInventorySize
    global blood
    global bloodbar
    global stamina
    global staminabar
    global mobility
    global mobilitybar
    global temperature
    global temperaturebar
    global thirst
    global thirstbar
    global hunger
    global hungerbar
    global status
    global hours
    global MaxInventorySize

    mobility=10

    for item in Inventory:
        if item["Name"]=="Pack":
            MaxInventorySize = 9

    bloodbar=[]
    staminabar=[]
    mobilitybar=[]
    temperaturebar=[]
    thirstbar=[]
    hungerbar=[]

    temperature = Locations[location]["Temperature"]
    if daynight() == "Night":
        temperature-=2
    if hours >= 12 and hours < 14:
        temperature+=2
    if checklocalinventory("Fire") is True:
        temperature+=2
    if blood<10 and hunger>=3 and temperature >3 and time % 1 == 0:
        blood+=1
    if stamina<10 and hunger>=3 and time % 1 ==0:
        stamina+=1
        staminafloor=time
    if time %10 ==0:
        hunger-=1
        hungerfloor=time
    if time % 5 == 0:
        thirst-=1
        thirstfloor=time
    if thirst<1:
        blood-=2
    if hunger<1:
        blood-=1
    if stamina<5:
        mobility-=4
    if temperature <3:
        hunger-=1
        if checkstatus("Cold") is not True:
            status.append("Cold")
    if temperature >= 3:
        if checkstatus("Cold") is True:
            removestatus("Cold")
    if temperature <= 1:
        blood-=1
        if checkstatus("Freezing") is not True:
            status.append("Freezing")
        if checkstatus("Cold") is True:
            removestatus("Cold")
    if temperature > 1:
        if checkstatus("Freezeing") is True:
            removestatus("Freezing")
    if temperature > 7:
        thirst-=1
        if checkstatus("Hot") is not True:
            status.append("Hot")
    if temperature <= 7:
        if checkstatus("Hot") is True:
            removestatus("Hot")
    if temperature >= 10:
        blood-=2
        if checkstatus("Burning") is not True:
            status.append("Burning")
        if checkstatus("Hot") is True:
            removestatus("Hot")
    if temperature < 10:
        if checkstatus("Burning") is True:
            removestatus("Burning")
    if thirst<3:
        stamina-=1
        if checkstatus("Thirsty") is not True:
            status.append("Thirsty")
    if thirst>=3:
        if checkstatus("Thirsty") is True:
            removestatus("Thirsty")
    if hunger<3:
        stamina-=1
        if checkstatus("Hungry") is not True:
            status.append("Hungry")
    if hunger >= 3:
        if checkstatus("Hungry") is True:
            removestatus("Hungry")

    if checkstatus("Laceration"):
        if blood>5:
            blood=5
        if mobility>5:
            mobility=5

    RealMaxInventorySize=MaxInventorySize+1
    if RealMaxInventorySize - len(Inventory) == 2:
        mobility-=2
    if RealMaxInventorySize - len(Inventory) == 1:
        mobility-=4
    if RealMaxInventorySize - len(Inventory) == 0:
        mobility-=6

    if checkstatus("Laceration"):
        if blood>5:
            blood=5
        if mobility>5:
            mobility=5

    if blood<0:
        blood=0
    if blood ==0:
        dead()
    if blood>10:
        blood=10
    if stamina<0:
        stamina=0
    if stamina>10:
        stamina=10
    if mobility<0:
        mobility=0
    if temperature<0:
        temperature=0
    if temperature>10:
        temperature=10
    if thirst<0:
        thirst=0
    if thirst>10:
        thirst=10
    if hunger<0:
        hunger=0
    if hunger>10:
        hunger=10
    bloodbar=["\u2588"]*blood
    bloodbar.append("\u2592"*(10-blood))
    staminabar=["\u2588"]*stamina
    staminabar.append("\u2592"*(10-stamina))
    mobilitybar=["\u2588"]*mobility
    mobilitybar.append("\u2592"*(10-mobility))
    temperaturebar=["\u2588"]*temperature
    temperaturebar.append("\u2592"*(10-temperature))
    thirstbar=["\u2588"]*thirst
    thirstbar.append("\u2592"*(10-thirst))
    hungerbar=["\u2588"]*hunger
    hungerbar.append("\u2592"*(10-hunger))

def n(i,p):
    return bool(i==p)

def removestatus(item):
    global status
    for n, s in enumerate(status):
        if s==item:
            del status[n]
def usefernsonleg():
    global status
    for n, s in enumerate(status):
        if s=="Laceration":
            del status[n]
            removeitem("Ferns")
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
        if s =="Laceration":
            status[n]="Laceration"
    global selficon
    selficon="@"
    global mappos
    mappos = {"y":1,"x":8}
    global location
    location = "Shore"
    addprintbuffer("You wake up on a gray beach, half submerged and vomit into the ocean. Your leg hurts bad. It's been wrapped in cloth, but it's still bleeding. It needs some sort of ointment to stop it. You are alone.")

def gounconscious():
    global location
    global Inventory
    global status
    global time
    time+=20
    status.append("Laceration")
    status.append("Unconscious")
    Inventory = []
    location = "Unconscious"

def docks():
    Locations["Ricken's Door"]["Direction"]["North"] = Locations["Ricken's Door"]["Direction"]["Hidden"]

def mapupdate():
    mapgrid[mappos["y"]][mappos["x"]]=selficon

def inspectavailableitems(p):
    Item = (matchbynameList(p, Inventory) or matchbynameList(p, Locations[location]["Items"]))
    for i in Locations[location]["Items"]:
        if i["Name"]=="Boat":
            if matchbynameList(p,i["Holding"]) is not False:
                Item = matchbynameList(p, i["Holding"])
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
    return False
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
        if match(i["Name"],itemname):
            item = i

        if item == i:
            Inventory.remove(item)
            Locations[location]["Items"].append(item)
            addprintbuffer("You no longer possess " + item["Name"] + ".")

def putinboat(itemname):
    item=None
    for b in Locations[location]["Items"]:
        if b["Name"]=="Boat":
            for i in Inventory:
                if match(i["Name"],itemname):
                    item = i

                if item == i:
                    Inventory.remove(item)
                    b["Holding"].append(item)
                    addprintbuffer("You no longer possess " + item["Name"] + ".")

def checkavailableitems(item):
    boat=None
    for b in Locations[location]["Items"]:
        if b["Name"]=="Boat":
            boat=b
    for i in Inventory:
        if i["Name"]==item:
            return True
    for a in Locations[location]["Items"]:
        if a["Name"]==item:
                    return True
    if boat is not None:
        for c in Locations[location]["Items"]:
            if c["Name"]=="Boat":
                for d in c["Holding"]:
                    if d["Name"]==item:
                        return True
    return False

def checkinventory(pattern):
    for i in Inventory:
        if i["Name"] == pattern:
            return True
    return False

def checklocalinventory(item):
    for i in Locations[location]["Items"]:
        if i["Name"]==item:
            return True
    return False

def checkstatus(pattern):
    global status
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

def getavailableitems():
    AvailableItems=[]
    for i in Locations[location]["Items"]:
        AvailableItems.append(i)
    boat=list(filter(lambda x: x["Name"]=="Boat",Locations[location]["Items"]))
    for a in boat[0]["Holding"]:
        AvailableItems.append(a)
    for b in Inventory:
        AvailableItems.append(b)
    return AvailableItems

def getlocationitemnames():
    LocNames=[]
    for i in Locations[location]["Items"]:
        LocNames.append(i["Name"])
    for stuff in Locations[location]["Items"]:
        if stuff["Name"]=="Boat":
            for h in stuff["Holding"]:
                LocNames.append(h["Name"])
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
    global MaxInventorySize
    for num, p in enumerate(Inventory):
        if num >= MaxInventorySize:
            addprintbuffer("You can not carry anymore items.")
            return
    for posession in Inventory:
        if posession["Name"]==itemname:
            addprintbuffer("You already have " + itemname + ".")
            return
    for item in Locations[location]["Items"]:
        if itemname == item["Name"]:
            if item["Obtainable"]==1:
                Locations[location]["Items"].remove(item)
                Inventory.append(item)
            if item["Obtainable"]==0:
                addprintbuffer("You cannot pick this up.")
                return
            if item["Obtainable"]==2:
                ItemCopy=deepcopy(item)
                Inventory.append(ItemCopy)
                for i in Inventory:
                    if i["Name"]==itemname:
                        i["Obtainable"]=1

            addprintbuffer("You have obtained " + item["Name"] + ".")
            return

        elif item["Name"]=="Boat":
            for subitem in item["Holding"]:
                if itemname == subitem["Name"]:
                    if subitem["Obtainable"] == 1:
                        item["Holding"].remove(subitem)
                        Inventory.append(subitem)
                    if subitem["Obtainable"] == 0:
                        addprintbuffer("You cannot pick this up.")
                        return
                    if subitem["Obtainable"]==2:
                        SubitemCopy=deepcopy(subitem)
                        Inventory.append(SubitemCopy)
                        for i in Inventory:
                            if i["Name"]==itemname:
                                i["Obtainable"]=1

                    addprintbuffer("You have obtained " + subitem["Name"] + ".")
                    return

    addprintbuffer("You cannot.")

def move(direction):
    if mobility == 0:
        addprintbuffer("You are unable to move.")
        return
    global location
    boat=None
    destination=Locations[location]["Direction"][direction]
    for b in Locations[location]["Items"]:
        if b["Name"]=="Boat":
            boat=b
    if destination is None:
        addprintbuffer("You cannot.")
        return
    else:
        if Locations[destination]["Access"]=="Open":
            mapgrid[mappos["y"]][mappos["x"]]=Locations[location]["Icon"]
            location = destination
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
        elif boat is not None and Locations[destination]["Access"]=="Water":
            Locations[location]["Items"].remove(boat)
            Locations[destination]["Items"].append(boat)
            mapgrid[mappos["y"]][mappos["x"]]=Locations[location]["Icon"]
            location = destination
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
        elif boat is not None and Locations[location]["Access"]=="Water" and Locations[destination]["Access"]=="Shore":
            Locations[location]["Items"].remove(boat)
            Locations[destination]["Items"].append(boat)
            mapgrid[mappos["y"]][mappos["x"]]=Locations[location]["Icon"]
            location = destination
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
        elif Locations[destination]["Access"]=="Shore":
            mapgrid[mappos["y"]][mappos["x"]]=Locations[location]["Icon"]
            location = destination
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
    boatitems=[]
    if bool(Locations[location]["Items"]) is True :
        for item in Locations[location]["Items"]:
            l.append(item["Location Description"])
        addprintbuffer(" ".join(l))
    for i in Locations[location]["Items"]:
        if i["Name"]=="Boat":
            for h in i["Holding"]:
                boatitems.append(h["Name"])
            if len(i["Holding"]) != 0:
                addprintbuffer("The boat is holding "+", ".join(boatitems)+".")


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


