from room_area import *
from items import *

class Character(object):

	def __init__(self, name, description, dialogue):
		self.health = 100
		self.name = name
		self.description = description
		self.dialogue = dialogue
		
	def attack():
		pass
	def talk_to():
		pass
		
class Player(object):

	def __init__(self):
		self.health = 80
		self.alive = True
		print 'Office Bear says "Hello"'
		
	def add_health(self, amount):
		if self.health < 100:
			self.health = self.health+amount
			
		#health should never be above 100%
		if self.health > 100:
			self.health = 100
			
class Map(object):
	
	def __init__(self, start_room, start_area):
	
		self.rooms = {'office' : Room("The Office", "A subtle sense of confusion permeates the room.  A mouse nibbles an asian candy on one of the desks."),
					'kitchen' : Room("The Kitchen", "Someone has been cooking stinky fish, and the smell assaults your nasal passages." ),
					'corridor' : Room("The Corridor", "A dim light flickers above."),
					'toilet' : Room("Toilet", "The automatic light flickers on.  The single cubicle is engaged, and a faint sound of straining can be heard.")
					} 
		self.areas = {'office' : { 'your_desk' : Desk("Your desk", "The place of your greatest despair."),
								'corridor_exit' : Area("Corridor Exit", "The exit to the corridor"),
								'powerbears_desk' : Desk("Powerbear's desk", "It is well organised.  Everything is at right angles, and nothing is askew."),
								'barney_bears_desk' : Desk("Barney Bear's desk", "")}
					}
		self.items = {'your_desk' : { 'pizza' : Food("Pizza", 10, 100),
									'diary' : Document("Diary", "My Schedule:\n\nToday: Nothing") }
					}
		self.characters = {'office' : {'powerbears_desk' : {'powerbear' : Character("Powerbear", "He is large and extremely powerful bear.  You do not want to anger him.", get_dialogue('powerbear'))},
										'barney_bears_desk' : {'barney_bear' : Character("Barney Bear", "He is a girlish bear, who consistently whinges about how much he is getting paid.", get_dialogue('barney_bear'))}
										}				
						}
		
		
		self.current_room = start_room
		self.current_area = start_area
		print "Map initialised"
		
	def next_room(self, exit):
		pass
	
	def opening_room(self):
		return self.rooms.get(self.current_room)
		
	def opening_area(self):
		this_area = self.areas.get(self.current_room)
		return this_area.get(self.current_area)
	
	def goto_area(self, area):
		self.current_area = area
		this_area = self.areas.get(self.current_room).get(self.current_area)
		return this_area
		
	def get_room_areas(self):
		return self.areas.get(self.current_room)
		
	def get_area_items(self):
		if self.items.get(self.current_area):
			return self.items.get(self.current_area)
		else:
			return False
	
	def get_area_item(self, item_name):
		try:
			return self.items.get(self.current_area).get(item_name)
		except:
			return False
			
	def get_room_characters(self):
		try:
			return self.characters.get(self.current_room)
		except:
			return False
			
	def get_area_characters(self):
		try:
			return self.characters.get(self.current_room).get(self.current_area)
		except:
			return False
		
	def room_exists(self, room):
		if self.rooms.get(room):
			return True
		else:
			return False
			
	def area_exists(self, area):
		if self.areas.get(self.current_room).get(area):
			return True
		else:
			return False

def get_dialogue(character_id):
	dialogue = {"powerbear": [{'user_words' : "Hello",
								'response' : "Get back to work Office Bear!"},
							{'user_words' : "Can I go home yet?",
								'response' : "No you cannot.  You've only done 10 minutes work!"}
							]
				}
				
	try:
		return dialogue[character_id]
	except:
		return False
			
class Engine(object):
	
	def __init__(self, room_map):
		print "Game Engine Initialised"
		self.room_map = room_map
		self.player = Player()
		self.text_seperator = "------------------------------"
		
	def play(self):
		current_room = self.room_map.opening_room()
		current_area = self.room_map.opening_area()		
		playing = True
		
		print """
		
Welcome to OFFICEBEAR2000!
You are Office Bear, and you work for a company selling music experiences.  

It's 4pm, and you've just woken up at your desk.  Time to go home!		
		"""
		
		# Game loop
		while playing:
			print self.text_seperator
			current_room.enter(self.room_map.get_room_areas(), self.room_map.get_room_characters())
			
			room_exit = False
			
			while room_exit != True:

				area_exit = False
				current_area.enter(self.room_map.get_area_items(), self.room_map.get_area_characters())
				
				while area_exit != True:
					#action are: waddleto/wt use/u talkto/t pickup/p read/r
					print self.text_seperator
					prompt = "What do you want to do? %s%% > " % self.player.health
					user_input = raw_input(prompt)
					print self.text_seperator
					
					action = action_interpreter(user_input)
					
					if action['action'] == 'waddleto' or action['action'] == 'wt':
						#does the area exist?
						if self.room_map.area_exists(action['action_subject']):
							current_area = self.room_map.goto_area(action['action_subject'])
							area_exit = True
						else:
							print "You can't go to there!"
							
					elif action['action'] == 'use' or action['action'] == 'u':
						
						try:
							use_item = self.room_map.get_area_item(action['action_subject'])
							use_item.use(self.player)
						except:
							print "That isn't available to use.  Try read?"
						
					elif action['action'] == 'read' or action['action'] == 'r':
					
						if 'action_subject' in action:
							document = self.room_map.get_area_item(action['action_subject'])
							if document:
								try:
									print document.content
								except:
									print "This isn't something you can read!"
							else:
								print "You can't read that.  It doesn't exist!"
						else:
							print "Read what?"
					
					elif action['action'] == 'instructions' or action['action'] == 'intr':
						print "Actions: waddleto/wt, use/u, read/r, talkto/t, pickup/p, quit & instructions"
					
					elif action['action'] == 'quit':
						print "Bye Bye"
						area_exit = True
						room_exit = True
						playing = False
						
					else:
						print "%s?! You can't do that you plonker!" % action['action']
				
def action_interpreter(user_input):
	#get the first word
	user_input_list = user_input.split(' ')
	action_obj = {}
	action_obj['action'] = user_input_list.pop(0)
	
	#join the other bits back together
	user_input = ' '.join(user_input_list)
	#remove nasty characters
	user_input = user_input.replace("'", "")
	
	if action_obj['action'] == 'use' and ' on ' in user_input:
		action_obj.update({'action_subject' : user_input.split(' on ')[0].lower().replace(' ','_'),
				'action_on' : user_input.split(' on ')[1].lower().replace(' ','_')})
	elif len(user_input) > 0:
		action_obj['action_subject'] = user_input.lower().replace(' ','_')

	return action_obj
			
	
a_map = Map('office', 'your_desk')
a_game = Engine(a_map)
a_game.play()
		