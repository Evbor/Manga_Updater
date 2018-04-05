import requests
import functools

#Target object definition, has attributes: source(string), protocol(string), command(string), strip_data(function)
class Target:
	def __init__(self, source = None, proto = None, com = None, script = None):
		self.address = source
		self.protocol = proto
		self.command = com
		self.strip_data = script
#Webscraper object definition
class Webscraper:
	def __init__(self, list_of_targets = []):
		if not (isinstance(list_of_targets, list) and functools.reduce(lambda A, B: A and isinstance(B, Target), list_of_targets, True)):
			raise ValueError("Webscraper only accepts arguements of list of Targets type")
		self.targets = list_of_targets
			
	def add_targets(self, Momo):
		if isinstance(Momo, Target):
			self.targets.append(Momo)
		elif (isinstance(Momo, list) and Momo and functools.reduce(lambda A, B: A and isinstance(B, Target), Momo, True)): #the lambda checks out if each element in Momo is a Target Object and returns true if it is
			self.targets.extend(Momo)
		else:
			raise ValueError("arguement of add_targets is not a list of Targets or Target type")
	
	def remove_all_targets(self):
		self.targets.clear()
		
	def scrape(self):
		results = []
		for tar in self.targets:
			if (tar.protocol == "HTTP"):
				result = self.scrape_HTTP(tar)
				results.append(result)
			else:
				print("targets protocol is not supported")
		return results
			
	@staticmethod
	def scrape_HTTP(target):
		result = None
		if (target.command == "GET"):
			response = requests.get(target.address)
			result = target.strip_data(response)
		else:
			print("Command not supported by HTTP protocol/still working on adding other commands")
		return result
			
			

