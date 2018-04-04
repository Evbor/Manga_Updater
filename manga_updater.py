from scraperdesu import *
from bs4 import BeautifulSoup
import regex

chapter_synonyms = ["chapter", "Ch\\."]

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



    
#generates the functions that Webscraper runs on each of the response objects it gets from its sources
def function_generator(chapter, m_name):
    #takes a manga chapter name and returns the chapter number as a float
    def chapter_num(chapter_name):
        cnum_signals = chapter_synonyms
        cnum_signals.insert(0, m_name) 
        for cnum_signal in cnum_signals:
            re_string = "(?<=" + cnum_signal + "[\\w]+ )\\d+|(?<=" + cnum_signal + " )\d+"
            pattern = regex.compile(re_string, regex.IGNORECASE)
            if pattern.search(chapter_name):
                num = int(pattern.search(chapter_name).group())
                return num
        return -1 
    #function generator will return modified versions of this script which takes a requests response object
    def isUpdated(response):
        raw_html = response.text
        soup = BeautifulSoup(raw_html, "html.parser")
        #finding current chapter tag
        current_chapter_tag = soup.find(string=regex.compile(chapter + "|\\s" + chapter + "\\s")).parent
        print(current_chapter_tag)
        while (current_chapter_tag.name != "a"):
            current_chapter_tag = current_chapter_tag.parent
        num = chapter_num(chapter)
        if num == -1:
            raise Exception("could not find chapter number in: " + chapter)
        #finding a previous chapter tag
        prev_tag = None
        def a_tags(taglist):
            if current_chapter_tag in set(taglist):
                taglist.remove(current_chapter_tag)
            return taglist
        container = current_chapter_tag
        while len(a_tags(container.find_all("a"))) == 0:
            container = container.parent
        for tag in container.find_all("a"):
            prev_num = num - 1
            if tag.find(string=regex.compile(str(prev_num))) != None:
                prev_tag = tag
        if prev_tag == None:
            print("couldn't find previous tag")
        else:
            print(prev_tag)
        
    return isUpdated

for manga in manga_list.values():
	scraper = Webscraper()
	for source in manga.sources:
		script = function_generator(manga.current_chapter[source], manga.name)
		target = Target(manga.sources[source], "HTTP", "GET", script)
		scraper.add_targets(target)
	result = scraper.scrape()



