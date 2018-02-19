import requests
import functools
from bs4 import BeautifulSoup

class Target:
	def __init__(self, source = None, proto = None, script = None):
		self.address = source
		self.protocol = proto
		self.strip_data = script

class Webscraper:
	def __init__(self, list_of_targets = []):
		if not (isinstance(list_of_targets, list) and functools.reduce(lambda A, B: A and isinstance(B, Target), list_of_targets, True)):
			raise ValueError("Webscraper only accepts arguements of list of Targets type")
		self.__targets = list_of_targets
			
	def add_targets(self, Momo):
		if isinstance(Momo, Target):
			self.__targets.append(Momo)
		elif (isinstance(Momo, list) and Momo and functools.reduce(lambda A, B: A and isinstance(B, Target), Momo, True)): #the lambda checks out if each element in Momo is a Target Object and returns true if it is
			self.__targets.extend(Momo)
		else:
			raise ValueError("arguement of add_targets is not a list of Targets or Target type")
	
	def remove_targets(self, Momo):
	
	def scrape(self):
		for tar in self.__targets:
			if (tar.protocol == "HTTP"):
				scrape_HTTP(tar)
			else:
				print("targets protocol is not supported")

	@staticmethod
	def scrape_HTTP(target):
		response = requests.get(address)
		soup = BeautifulSoup(response.text)
		print(soup.prettify())
			
			
			
			
#human method for checking chapter updates
#find area where all other chapters are 
#look for updated chapter
#ex: looking for whether rezero 17 is out
#find tag that contains the rezero 16 link 
#go up to parent tag
#look for rezero 17
