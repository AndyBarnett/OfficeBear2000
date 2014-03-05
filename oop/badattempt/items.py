
class Item(object):
	def __init__(self, name):
		self.name = name
	def use(self):
		pass
	def pickup(self):
		pass
	def get_name(self):
		return self.name
		
class Food(Item):
	def __init__(self, name, parts, energy_per_part):
		self.name = name
		self.parts = parts
		self.energy_per_part = energy_per_part
		
	def use(self, player):
		player.add_health(self.energy_per_part)
		print "Nom nom nom, your health has increased."
		
class Document(Item):
	def __init__(self, name, content):
		self.name = name
		self.content = content
