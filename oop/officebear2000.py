#officebear2000

CONFIG = {'intro' : "You are Office Bear, a cuddly little developer working for a tech company in the forest.",
			'seperator' : "-------------------------",
			'instructions' : "You can: waddleto/wt somewhere, use/u something, read/r something, talkto/t something, pickup/p something, quit & instructions"
			}

class Room(object):
	def __init__(self, name, description):
		self.name = name
		self.description = description
		self.contents = {}
		
	def add_item(self, id, item):
		self.contents[id] = item
		
	def get_item(self, id):
		try:
			return self.contents[id]
		except:
			return False
	
	def describe(self):
		return_string = "%s\n" % self.description
		
		if len(self.contents) > 0:
			return_string += "You can see:\n"
			for ident, item in self.contents.iteritems():
				return_string += " - %s\n" % item.name
			
		return return_string
		
class Item(object):
	def __init__(self, name, description):
		self.name = name
		self.descripton = description
		self.custom_properties = {}
		
	def add_custom_prop(self, property, value):
		self.custom_properties[property] = value;
	def get_custom_prop(self, property):
		try:
			return self.custom_properties[property]
		except:
			return False
		
class Player(object):
	def __init__(self, name):
		self.name = name
		self.health = 100
		
class Map(object):
	def __init__(self, start_room):
		self.rooms = {}
		self.rooms['office'] = Room("Office", "It is a place of despair.  A broken flourescent tube flickers above.  A rodent chews an asian candy on a nearby desk.")
		self.rooms['office'].add_item('your_diary', Item("Your Diary", "A black leatherbound book"))
		self.rooms['office'].contents.get('your_diary').add_custom_prop('text_content', "My Schedule:\nFuck All")
		
		self.start_room = self.rooms[start_room]

class Engine(object):
	def __init__(self, map, config):
		self.playing = True
		self.current_room = map.start_room
		self.player = Player("OfficeBear")
		self.introduction = config['intro']
		self.seperator = config['seperator']
		
	def play(self):
		
		print self.introduction
		
		while self.playing == True:
			
			#introduce room
			print "You are in the %s" % self.current_room.name
			print self.current_room.describe()
			
			room_changed = False
			while room_changed == False:
				print self.seperator
				print "What do you want to do? (%s%%) >" % player.health,
				user_action = raw_input()
				action = action_interpreter(user_action)
				
				if action['action'] == 'waddleto' or action['action'] == 'wt':
					print "Walking"
				elif action['action'] == 'read' or action['action'] == 'r':
					item = self.current_room.get_item(action['action_subject'])
					if item:
						text = item.get_custom_prop('text_content')
						if text:
							print "It says:\n-----\n%s\n-----" % text
						else:
							print "There is nothing to read."
					else:
						print "There is no object called %s that you can read" % action['action_subject']
					
					
				elif action['action'] == 'quit':
					room_changed = True
					self.playing = False
					print "Byeeeeeeeeeeee!"
				else:
					print "You can't do that!"




		
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

print "Starting..."
room_map = Map('office')
player = Player("Office Bear")			
game = Engine(room_map, CONFIG)
game.play()

