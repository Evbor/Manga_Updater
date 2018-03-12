from scraperdesu import *
from bs4 import BeautifulSoup

class Manga: 
	def __init__(self, namae = None, jouhougen = None, honshou = None): #name = string, sources = {source: url} e.g. {"mangakalot": "http://mangakakalot.com/search/made_in_abyss"}, current_chapter = number
		self.name = namae
		self.sources = jouhougen
		self.current_chapter = honshou

sources = {"mangakakalot": "http://mangakakalot.com/search/made_in_abyss", "mangahere": "http://www.mangahere.cc/search.php?name=made+in+abyss", "crunchyroll": "http://www.crunchyroll.com/search?from=comics&q=seven+deadly+sins"}
MiAsrcs = {"mangakakalot": "http://mangakakalot.com/manga/made_in_abyss", "mangahere": "http://www.mangahere.cc/manga/made_in_abyss/"}
chptrs = {"mangakakalot": "Chapter 45", "mangahere": "Made in Abyss 45"}
madeinabyss = Manga("Made in Abyss", MiAsrcs, chptrs)
manga_list = {madeinabyss.name: madeinabyss}


def function_generator(chapter):
	def isUpdated(response):
		raw_html = response.text
		soup = BeautifulSoup(raw_html)
		prev_chapter = #reduce chapter
		chapter_list = soup.find("a", string=prev_chapter)
	return isUpdated

for manga in manga_list.values():
	scraper = Webscraper()
	for source in manga.sources:
		script = function_generator(manga.current_chapter[source])
		target = Target(manga.sources[source], "HTTP", "GET", script)
		scraper.add_targets(target)
	result = scraper.scrape()


