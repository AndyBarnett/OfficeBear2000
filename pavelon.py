import sys
from sys import exit, argv
import pygame
from ConfigParser import SafeConfigParser

#--------------All the stuff to do with reading rooms, items, characters from the config.ini file and storing them as dictionary items--------------

script, config = argv

if len(sys.argv) != 2:
            sys.exit("Incorrect number of arguments")

content = open(sys.argv[1], 'r')

#print content.read()

def readcFile(fileName):
    
    cFile={}
          
    parser = SafeConfigParser()
    parser.read(fileName)
    
    #put this in a loop eventually
    
    #rooms
    cFile['roomA'] = parser.get('rooms', 'roomA')
    cFile['roomB'] = parser.get('rooms', 'roomB')
    
    #roomA items
    cFile['itemA1'] = parser.get('itemsA', 'item1')
    cFile['itemA2'] = parser.get('itemsA', 'item2')
    cFile['itemA3'] = parser.get('itemsA', 'item3')
    cFile['itemA4'] = parser.get('itemsA', 'item4')
    
    #roomB items
    cFile['itemB1'] = parser.get('itemsB', 'item1')
    cFile['itemB2'] = parser.get('itemsB', 'item2')
    cFile['itemB3'] = parser.get('itemsB', 'item3')
    cFile['itemB4'] = parser.get('itemsB', 'item4')
    
    #roomA characters
    cFile['characterA1'] = parser.get('charactersA', 'char1')
    cFile['characterA2'] = parser.get('charactersA', 'char2')
    cFile['characterA3'] = parser.get('charactersA', 'char3')
    cFile['characterA4'] = parser.get('charactersA', 'char4')
    cFile['characterA5'] = parser.get('charactersA', 'char5')
    
    #roomB characters
    
    #roomA character greetings
    cFile['character_greetingsA1'] = parser.get('character_greetingsA', 'char1')
    cFile['character_greetingsA2'] = parser.get('character_greetingsA', 'char2')
    cFile['character_greetingsA3'] = parser.get('character_greetingsA', 'char3')
    cFile['character_greetingsA4'] = parser.get('character_greetingsA', 'char4')
    cFile['character_greetingsA5'] = parser.get('character_greetingsA', 'char5')
    
    #roomA character angrys
    cFile['character_angryA1'] = parser.get('character_angrysA', 'char1')
    cFile['character_angryA2'] = parser.get('character_angrysA', 'char2')
    cFile['character_angryA3'] = parser.get('character_angrysA', 'char3')
    cFile['character_angryA4'] = parser.get('character_angrysA', 'char4')
    
    return dict(cFile)

print readcFile(sys.argv[1])
#--------------All the stuff to do with reading rooms, items, characters from the config.ini file and storing them as dictionary items--------------

#--------------All the music and image stuff--------------

soundFile='musicwav.wav'
pygame.init()
pygame.mixer.music.load(soundFile)
pygame.mixer.music.play()

backgroundimage="paploo.jpg"
background = pygame.image.load(backgroundimage)
backgroundRect = background.get_rect()
size = (width, height) = background.get_size()
screen = pygame.display.set_mode(size)
img=pygame.image.load(backgroundimage) 
screen.blit(img,(0,0))
pygame.display.flip()

#--------------All the music and image stuff--------------

room="office"
hunger=0
max_hunger=0
inventory=[]
room_items=["desk", "exit", "powerman", "pizza", "diary"]
in_room=True
position="desk"
powerman_subdued=False


print "Welcome to Pavelon, the Pavel-based text adventure game \n"
def instructions():
    print "The acceptable verbs are:"
    print "\"waddle to\",\n\"take\",\n\"use\",\n\"attack\",\n\"eat\""
    print "To list the objects around you, type \"look\""
    print "To check what items you have, as well as your position and hunger level, type \"status\". To see these instructions again at any time, type 'help'"

def difficulty():
    global hunger
    global max_hunger
    
    prompt = "foobear"  
    while prompt!="1" and prompt!="2" and prompt!="3" and prompt!="death":
        prompt = raw_input("Select Difficulty, 1=easy, 2=medium or 3=hard: >")
        
    if prompt=="1":
        hunger=30
        max_hunger=30
    elif prompt=="2":
        hunger=20
        max_hunger=20
    elif prompt=="3":
        hunger=10
        max_hunger=10
    elif prompt=="death":
        hunger=0
        max_hunger=0
    main()
    
def main():

    room_intro(room)
    while in_room==True and hunger!=0:
        prompt = raw_input("> ")
        if prompt=="look":
            look()
        elif prompt=="status":
            status()
        elif "use" in prompt:
            use(prompt)
        elif "take" in prompt:
            take(prompt)
        elif "waddle to" in prompt:
            go_to(prompt)
        elif "eat" in prompt:
            eat(prompt)
        elif "attack" in prompt:
            attack(prompt)
        elif prompt=="help":
            instructions()
        else:
            print "pardon?"
    dead("You starved! Pizza was back at your desk, try again!")
            

def room_intro(room):
    if room=="office":
        print "You are Pavel. You wake up at your desk in London. It is 4pm. You must get home, your Ewok family needs you."
        print "Your hunger level is %d/%d. Infinite pizza is at your desk, you lucky thing." % (hunger, max_hunger)
    else:
        print "you click your heels together three times and wish really hard, and you wake up in The Motherland"
        exit(0)

#I should try-except all of this shit instead of returning after every if/elif is reached. I suck.
def go_to(prompt):
    if len(room_items)!=0:
        for room_object in room_items:
            if room_object in prompt:
                print "You waddle over to the %s" %room_object
                global position
                position=str(room_object)
                hunger_down()
                return
        print "Waddle to where sorry? To list items, type 'look'"
        return
    else:
        print "There are no objects left in the room you crazy bastard"
    
    
def status():
    if len(inventory)!=0:
        print "You have the following items:"
        for inventory_item in inventory:
            print inventory_item
    else:
        print "You don't have anything in your Ewockets"
    print "Your position is at %s" %position
    print "Your hunger level is %d/%d. Infinite pizza is at your desk." % (hunger, max_hunger)
        
def look():
    print "Items in the room are:"
    for room_object in room_items:
        print room_object

def hunger_down():
    global hunger
    hunger-=1
    print "Your hunger level is %d/%d. Infinite pizza is at your desk."% (hunger, max_hunger)
            
def use(prompt):
    global powerman_subdued
    global position
    if len(inventory)!=0:
        for inventory_item in inventory:
            if inventory_item in inventory and inventory_item in prompt:
                print "You attempt to use %s" %inventory_item
                if inventory_item=="diary" and position!="powerman":
                    print "You open your diary and it is blank as usual ='("
                    hunger_down()
                    return
                elif inventory_item=="pizza" and position !="powerman":
                    print "A pizza is never worth 'using', only eating!"
                    return
                elif inventory_item=="pizza" and position=="powerman":
                    print "Lord Powerman is not impressed with your mortal sustenance"
                    return
                elif inventory_item=="diary" and position=="powerman":
                    print "\"Uhrhm, Gray-hum, I must need to go to a meetings at this present times...\" Powerman just tells you to go away then. NOW'S YOUR CHANCE!"
                    powerman_subdued=True
                    hunger_down()
                    return
            elif "exit" in prompt and position!="exit":
                print "You attempt to use the exit"
                print "You ain't at the exit"
                return
            
            for room_object in room_items:
                if room_object in prompt and prompt !="use exit" and prompt!="use powerman":
                    print "You aren't carrying that"
                    return
                elif "exit" in prompt and powerman_subdued==False and position=="exit":
                    print "Powerman shouts at you for attempting to leave early! Everyone laughs."
                    hunger_down()
                    return
                elif "exit" in prompt and powerman_subdued==True and position=="exit":
                    print "YOU ARE FREE! YOU WIN!"
                    exit(0)
        print "Use what? That item isn't even in this game, you must be drunk you silly bear"

    elif prompt=="use powerman":
        print "The powerman can not be used.  Only the powerman can use another.  Powerman uses you as an involuntary martial arts opponent.  You are entirely destroyed"
        dead("A swift fisting")
    else:
        print "you don't have anything in your Ewockets"
    

def take(prompt):
    global hunger
    global position
    if len(room_items)!=0:
        for room_object in room_items:
            if room_object in room_items and position==room_object and room_object in prompt:
                print "You attempt to pick up %s" %room_object
                if room_object=="diary":
                    print "Diary successfully picked up."
                    inventory.append(room_object)
                    room_items.remove(room_object)
                    return
                elif room_object=="powerman":
                    print "You wrap your arms around Powerman. He smiles as he silently kills you."
                    dead("you were crushed by the mighty Powerman.")
                elif room_object=="desk":
                    print "You lift the desk off the floor and drop it again, and everyone stares at you. You can't drag the desk around, it is your sacred shrine of pizza."
                    hunger_down()
                    return
                elif room_object=="exit":
                    print "Try 'use exit'"
                    return
            elif room_object in room_items and position!=room_object and room_object in prompt and "pizza" not in prompt:
                print "Your little ewok arms can't reach that! You're still at "+position+". Waddle over to it"
                return
        
        if "pizza" in room_items and position=="desk" and "pizza" in prompt:
                if "pizza" not in inventory and hunger !=max_hunger:
                    print "Pizza successfully picked up."
                    inventory.append("pizza")
                    return
                elif "pizza" not in inventory and hunger==max_hunger:
                    print "Smart bear, taking one for the road!"
                    inventory.append("pizza")
                    return
                elif "pizza" in inventory:
                    print "You can only take once slice at a time with you on your adventure!"
                    return
        elif "pizza" in room_items and position!="desk" and "pizza" in prompt:
            print "Your little ewok arms can't reach pizza! You're still at "+position+". Waddle over to your desk."
            return
        print "Take what? That item isn't even in this game, you must be drunk you silly bear"
    else:
        print "There are no objects left in the room you crazy bastard"

def eat(prompt):
    if len(inventory)!=0:
        for inventory_item in inventory:
            if inventory_item in inventory and inventory_item in prompt:
                print "Om nom nom. Delicious %s!" %inventory_item
                if inventory_item=="diary":
                    dead("your stomach is filled with nothingness.")
                    return
                elif inventory_item=="pizza":
                    print "You replenished your hunger for pizza you fuzzy bastard"
                    global hunger
                    hunger=max_hunger
                    inventory.remove(inventory_item)
                    return
                elif inventory_item=="exit door":
                    print "You roar as you're sore from gnawing the door"
                    return

        for room_object in room_items:
            if room_object in prompt and prompt!="eat pizza":
                print "You aren't carrying that"
                return
            if room_object in prompt and prompt=="eat pizza":
                print "You've run out of pizza! Oh nooooooo!"
                return
        print "Eat what? That item isn't even in this game, you must be drunk you silly bear"
    else:
        print "you don't have any items yet"
        
def attack(prompt):
    for room_object in room_items:
        if room_object in prompt:
            print "You attack the %s." %room_object
            if room_object=="diary":
                print "You rip the diary to shreds with your bear claws and its usefulness remains the same"
                room_items.remove("diary")
                return
            elif room_object=="pizza":
                print "You truly have lost your mind. You realise what you've done and take your own life"
                dead("you're a pizza traitor")
            elif room_object=="exit":
                print "You scratch your claws angrily at the door but it does not open."
                return
            elif room_object=="powerman":
                print "The mighty Powerman laughs heartily and crushes you with his fist"
                dead("you were Powerman'd")
                    

    for inventory_item in inventory:
        if inventory_item in prompt:
            inventory.remove(inventory_item)
            print "You attack the %s." %inventory_item
            if inventory_item=="diary":
                print "You rip it to shreds with your bear claws and its usefulness remains the same"
                return
            elif inventory_item=="pizza":
                print "You truly have lost your mind. You realise what you've done and take your own life"
                dead("you're a pizza traitor")
    hunger_down()

def dead(why):
    print "You're dead because "+why+". He was a boisterous, sometimes foolhardy, Ewok"
    prompt="foobear"
    while prompt != "y" and prompt != "n":
        prompt = raw_input("Try again? (y/n) >")
        if prompt == "y":
            launch()
        elif prompt == "n":
            exit(0)

def launch():
    instructions()
    difficulty()
    
launch()