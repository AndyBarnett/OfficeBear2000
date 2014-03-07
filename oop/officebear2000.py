#officebear2000

CONFIG = {'intro' : "You are Office Bear, a cuddly little developer working for a tech company in the forest.",
			'seperator' : "--------------------------------------------------",
			'instructions' : "You can: waddleto/wt somewhere, lookat/l something, use/u something, read/r something, talkto/t something, pickup/p something, quit or instructions"
			}

class Room(object):
	def __init__(self, name, description):
		self.name = name
		self.description = description
		self.contents = {}
		
	def add_item(self, id, item):
		self.contents[id] = item
	
	def remove_item(self, id):
		success = False
		try:
			del self.contents[id]
			success = True
		except:
			success = False
			
		#if we can't delete the item, try deleting items in items.
		if success == False:
			for ident, item in self.contents.iteritems():
				if success == False:
					success = item.remove_item(id)
		
		return success
		
	
	def get_item(self, id):
	
		return_item = False
	
		try:
			return_item = self.contents[id]
		except:
			return_item = False
		
		#if the item isn't directly available in the room, look in it's items.
		if return_item == False:
			for ident, item in self.contents.iteritems():
				return_item = item.get_item(id)
				
		return return_item
	
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
		self.description = description
		self.contents = {}
		self.container_type = 'internal'
		self.locked = False
		self.grabbable = False
		self.custom_properties = {}
		
	def add_item(self, id, item):
		self.contents[id] = item
	
	def remove_item(self, id):
		try:
			del self.contents[id]
			return True
		except:
			print "Cannot delete that item"
			return False
	
	def get_item(self, id):
		return_item = False
		try:
			return_item = self.contents[id]
		except:
			return_item = False
			
		if return_item != False and self.locked == False:
			return return_item
		else:
			return False
			

		
	def add_custom_prop(self, property, value):
		self.custom_properties[property] = value;
	def get_custom_prop(self, property):
		try:
			return self.custom_properties[property]
		except:
			return False
	
	def describe(self):
		return_string = "%s" % self.description
		
		if self.container_type == 'surface':
			adjunct = "On"
		else:
			adjunct = "In"
		
		if len(self.contents) > 0:
			return_string += "\n%s it there is:" % adjunct
			for ident, item in self.contents.iteritems():
				return_string += "\n - %s" % item.name
		
		return return_string

		
class Player(object):
	def __init__(self, name):
		self.name = name
		self.health = 100
		self.inventory = {}
		
	def add_to_inventory(self, ident, item):
		self.inventory[ident] = item
		print "%s is now in your pocket." % item.name
		
	def describe_inventory(self):
		return_string = "You pockets contain:\n"
		if len(self.inventory) > 0:
			for ident, item in self.inventory.iteritems():
				return_string += " - %s\n" % item.name
		else:
			return_string += "Bugger all."
			
		return return_string
		
	def get_inventory_item(self, id):
		return_item = False
		try:
			return_item = self.inventory[id]
		except:
			return_item = False
			
		return return_item
		
class Map(object):
	def __init__(self, start_room):
		self.rooms = {}
		self.rooms['office'] = Room("Office", "It is a place of despair.  A broken flourescent tube flickers above.  A rodent chews an asian candy on a nearby desk.")
		self.rooms['office'].add_item('your_desk', Item("Your Desk", "It is tired and wooden, and covered in general detritus."))
		self.rooms['office'].contents.get('your_desk').add_item('your_diary', Item("Your Diary", "A black leatherbound book"))
		self.rooms['office'].contents.get('your_desk').container_type = 'surface'
		self.rooms['office'].contents.get('your_desk').contents.get('your_diary').add_custom_prop('text_content', "My Schedule:\nFuck All")
		self.rooms['office'].contents.get('your_desk').contents.get('your_diary').grabbable = True
		
		self.start_room = self.rooms[start_room]

class Engine(object):
	def __init__(self, map, config):
		self.playing = True
		self.current_room = map.start_room
		self.player = Player("OfficeBear")
		self.introduction = config['intro']
		self.instructions = config['instructions']
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
				print "What do you want to do? (%s%%) >" % self.player.health,
				user_action = raw_input()
				print self.seperator
				action = action_interpreter(user_action)
				
				if action['action'] == 'waddleto' or action['action'] == 'wt':
					print "Walking"
					
				elif action['action'] == 'lookat' or action['action'] == 'l':
					item = self.current_room.get_item(action['action_subject'])
					
					if item == False:
						item = self.player.get_inventory_item(action['action_subject'])
					
					if item:
						print item.describe()
					else:
						print "There is no item called that to look at."
				
				elif action['action'] == 'read' or action['action'] == 'r':
					item = self.current_room.get_item(action['action_subject'])
					
					if item == False:
						item = self.player.get_inventory_item(action['action_subject'])
						
					if item:
						text = item.get_custom_prop('text_content')
						if text:
							print "It says:\n-----\n%s\n-----" % text
						else:
							print "There is nothing to read."
					else:
						print "There is no object called that that you can read."
					
				elif action['action'] == 'pickup' or action['action'] == 'p':
					item = self.current_room.get_item(action['action_subject'])
					if item and item.grabbable == True:
						self.player.add_to_inventory(action['action_subject'], item)
						del_success = self.current_room.remove_item(action['action_subject'])
					elif item and item.grabbable == False:
						print "You can't pick that up, that would be ridiculous!"
					else:
						print "There is no item called that to pick up!"
				
				elif action['action'] == 'inventory' or action['action'] == 'i':
					print self.player.describe_inventory()
				
				elif action['action'] == 'instructions':
					print self.instructions
				
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
game = Engine(room_map, CONFIG)
game.play()

