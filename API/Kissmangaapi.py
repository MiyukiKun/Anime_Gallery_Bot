from bs4 import BeautifulSoup
import requests
import re

class kissmangaapi():
    
    def get_search_results(query):  # returns list of tuples cotaining name of manga and its id [(name1, id1), (name2, id2)]
        try:
            url = f"http://kissmanga.nl/search?q={query}"
            response = requests.get(url)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'lxml')
            mangas = soup.findAll("div", class_="media mainpage-manga")
            res_search_list = []
            for manga in mangas:
                manganame = manga.a["title"]
                link = manga.a["href"]
                split = link.split("/")
                split2 = split[-1].split("?")
                mangaid = split2[0]
                result = (manganame, mangaid)
                res_search_list.append(result)
            return res_search_list
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"
       
    def get_manga_details(mangaid):  # returns [str(details of manga), image_url]
        try:
            url = f"http://kissmanga.nl/manga/{mangaid}"
            response = requests.get(url)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'lxml')
            manga_description = soup.find("div", class_="summary_content").find_all("div", class_="post-content_item")
            txt = ''
            for i in manga_description:
                h = i.find("div", class_="summary-heading").text.strip()
                c = i.find("div", class_="summary-content").text.strip()
                c = re.sub(r'.*Average(?!.*Average)', '', c).strip()
                c = re.sub(r'\s+', ' ', c)
                c = re.sub(r' ,', ',', c)
                txt += f"{h}: {c}\n"
            title = soup.find("div", class_="post-title").text.strip()
            image = soup.find("div", class_="summary_image").a.img["data-src"]
            txt = f"Title: {title}\n{txt}".strip()
            
            return txt, image

        except AttributeError:
            return "Invalid Mangaid"
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"

    def get_manga_chapter(mangaid, chapternum):  # returns list of image links of pages of full chapter [imglink1, imglink2, full chapter]
        try:
            url = f"https://mangapure.net/manga/{mangaid}-chapter-{chapternum}"
            response = requests.get(url)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'lxml')
            chapter_pages = soup.find("p", id="arraydata")
            pages = chapter_pages.text.split(",")
            return pages
        except AttributeError:
            return "Invalid Mangaid or chapter number"
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"