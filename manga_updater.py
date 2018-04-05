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
#MiA
MiAsrcs = {"mangakalot": "http://mangakakalot.com/manga/made_in_abyss", "mangahere": "http://www.mangahere.cc/manga/made_in_abyss/"}
MiAchptrs = {"mangakalot": "Chapter 45", "mangahere": "Made in Abyss 45"}
madeinabyss = Manga("Made in Abyss", MiAsrcs, MiAchptrs)
#AoT
AoTsrcs = {"mangakalot": "http://manganelo.com/manga/read_attack_on_titan_manga_online_free2", "mangahere": "http://www.mangahere.cc/manga/shingeki_no_kyojin/"}
AoTchptrs = {"crunchyroll": "Ch. 103", "mangakalot": "Chapter 104", "mangahere": "Shingeki no Kyojin 104"}
AoT = Manga("Shingeki no Kyojin", AoTsrcs, AoTchptrs)

manga_list = {madeinabyss.name: madeinabyss, AoT.name: AoT}

#to scrape crunchyroll find out how to scrape js websites



    
#generates the functions that Webscraper runs on each of the response objects it gets from its sources
def function_generator(chapter, m_name):
    #takes a manga chapter name and returns the chapter number as a float or returns -1 if chapter number is not found
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
    #This function returns a boolean: True (for when a unread chapter has been released) False (otherwise)
    def isUpdated(response):
        raw_html = response.text
        soup = BeautifulSoup(raw_html, "html.parser")
        #finding current chapter tag
        current_chapter_tag = soup.find(string=regex.compile(chapter + "|\\s" + chapter + "\\s"))
        while (current_chapter_tag.name != "a"):
            current_chapter_tag = current_chapter_tag.parent
        num = chapter_num(chapter)
        if num == -1:
            raise Exception("could not find chapter number in: " + chapter)
        #finding chapter list tag
        def a_tags(taglist):
            #if they add a tags that are not chapter a tags in between chapter a tags then
            #write algorithm to remove non chapter a tags from taglist
            #so far they don't do this ie the a_tag closest to a chapter a tag is another chapter a tag
            if current_chapter_tag in set(taglist):
                taglist.remove(current_chapter_tag)
            return taglist
        container = current_chapter_tag
        while len(a_tags(container.find_all("a"))) == 0:
            container = container.parent
        #checking whether a chapter has been updated or not
        updated = False
        updated_chapters = []
        for chapter_tag in container.find_all("a"):
            chapter_tag_strings = chapter_tag.stripped_strings
            if (len(chapter_tag_strings) == 0):
                print("chapter_a_tag does not contain any strings")
            else:
                for ch_string in chapter_tag_strings:
                    ch_number = chapter_num(ch_string)
                    if (ch_number != -1) and (ch_number > num):
                        updated = True
                        updated_chapters.append(chapter_tag)
        return (updated, updated_chapters)
                        
    return isUpdated

for manga in manga_list.values():
    scraper = Webscraper()
    for source in manga.sources:
        script = function_generator(manga.current_chapter[source], manga.name)
        target = Target(manga.sources[source], "HTTP", "GET", script)
        scraper.add_targets(target)
    result = scraper.scrape()
    scraper.remove_all_targets()



