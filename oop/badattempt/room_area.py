class Room(object):
	def __init__(self, name, description):
		self.name = name
		self.description = description
		
	def enter(self, areas, characters):
		print "You are in %s." % self.name
		print self.description
		print "You can see:"
		for ident, area in areas.iteritems():

			characters_desc = ""
			
			if characters and characters.get(ident):
				area_characters = characters.get(ident)
				characters_desc = character_sentence(area_characters, "room")

			else:
				pass
				
			if len(characters_desc) > 1:
				print " - %s. %s" % (area.name, characters_desc)
			else:
				print " - %s" % area.name

			
			
	def exit(self):
		pass
		
	def get_name(self):
		return self.name
		
class Area(Room):
	def enter(self, items, characters):
		print "You are at %s." % self.name, self.description
		
		if characters:
			print character_sentence(characters, "area"),
		
		if items:
			print "Items on %s:" % self.name
			for ident, item in items.iteritems():
				print " - ", item.get_name()
		else:
			print "There is nothing of interest on %s" % self.name	
		

# Define rooms and areas below
		
class Desk(Area):
	pass	

def character_sentence(character_list, room_area_switch):
	characters_desc = ""
	if room_area_switch == "room":
		here_there = "there"
	else:
		here_there = "here"
	
	if len(character_list) > 1:
		character_count = len(character_list)
		i = 0
		for ident, character in character_list.iteritems():
			
			if i == 0:
				characters_desc += "%s " % character.name
			elif i == character_count-1:
				characters_desc += "and %s " % character.name
			else:
				characters_desc += "%s, " % character.name
			i += 1
			
		
		characters_desc += "are %s." % here_there
	elif len(character_list) == 1:
		for ident, character in character_list.iteritems():
			characters_desc += "%s " % character.name
		characters_desc += "is %s." % here_there
	else:
		pass
		
	return characters_desc
	
	