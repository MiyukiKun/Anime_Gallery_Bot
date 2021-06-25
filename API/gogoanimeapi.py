from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

class gogoanime():
    def __init__(self, query, animeid, episode_num):
        self.query = query
        self.animeid = animeid
        self.episode_num = episode_num

    def get_search_results(query):
        try:
            url1 = f"https://gogoanime.ai//search.html?keyword={query}"
            session = HTMLSession()
            response = session.get(url1)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            res_list_search = []
            for anime in animes:
                tit = anime.a["title"]
                urll = anime.a["href"]
                r = urll.split('/')
                res_list_search.append({"name":f"{tit}","animeid":f"{r[2]}"})
            if res_list_search == []:
                return {"status":"204", "reason":"No search results found for the query"}
            else:
                return res_list_search
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}

    def get_anime_details(animeid):
        try:
            animelink = 'https://gogoanime.ai/category/{}'.format(animeid)
            response = requests.get(animelink)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            source_url = soup.find("div", {"class": "anime_info_body_bg"}).img
            imgg = source_url.get('src')
            tit_url = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            lis = soup.find_all('p', {"class": "type"})
            plot_sum = lis[1]
            pl = plot_sum.get_text().split(':')
            pl.remove(pl[0])
            sum = ""
            plot_summary = sum.join(pl)
            type_of_show = lis[0].a['title']
            ai = lis[2].find_all('a')
            genres = []
            for link in ai:
                genres.append(link.get('title'))
            year1 = lis[3].get_text()
            year2 = year1.split(" ")
            year = year2[1]
            status = lis[4].a.get_text()
            oth_names = lis[5].get_text()
            lnk = soup.find(id="episode_page")
            ep_str = str(lnk.contents[-2])
            a_tag = ep_str.split("\n")[-2]
            a_tag_sliced = a_tag[:-4].split(">")
            last_ep_range = a_tag_sliced[-1]
            y = last_ep_range.split("-")
            ep_num = y[-1]
            res_detail_search = {"title":f"{tit_url}", "year":f"{year}", "other_names":f"{oth_names}", "type":f"{type_of_show}", "status":f"{status}", "genre":f"{genres}", "episodes":f"{ep_num}", "image_url":f"{imgg}","plot_summary":f"{plot_summary}"}
            return res_detail_search
        except AttributeError:
            return {"status":"400", "reason":"Invalid animeid"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}

    def get_episodes_link(animeid, episode_num):
        try:
            animelink = f'https://gogoanime.ai/category/{animeid}'
            response = requests.get(animelink)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            lnk = soup.find(id="episode_page")
            source_url = lnk.find("li").a
            tit_url = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            URL_PATTERN = 'https://gogoanime.ai/{}-episode-{}'
            url = URL_PATTERN.format(animeid, episode_num)
            srcCode = requests.get(url)
            plainText = srcCode.text
            soup = BeautifulSoup(plainText, "lxml")
            source_url = soup.find("li", {"class": "dowloads"}).a
            vidstream_link = source_url.get('href')
            URL = vidstream_link
            dowCode = requests.get(URL)
            data = dowCode.text
            soup = BeautifulSoup(data, "lxml")

            dow_url = []
            for i in range(11):
                try:
                    dow_url.append(soup.findAll('div', {'class': 'dowload'})[i].find('a'))
                except:
                    pass

            downloadlink = []
            qualityname = []
            for i in range(len(dow_url)):
                downloadlink.append(dow_url[i].get('href'))
                string = dow_url[i].string
                string_spl = string.split()
                string_spl.remove(string_spl[0])
                string_original = ''
                qualityname.append(string_original.join(string_spl))
            episode_res_link = {}
            for i in range(len(qualityname)):
                episode_res_link[qualityname[i]] = downloadlink[i]

            return episode_res_link

        except AttributeError:
            return {"status":"400", "reason":"Invalid animeid or episode_num"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}
    
    def get_home_page():
        try:
            url = 'https://gogoanime.ai'
            session = HTMLSession()
            response = session.get(url)
            response_html = response.text

            soup = BeautifulSoup(response_html, 'lxml')
            res_list_search =[]
            animes =  soup.find("ul", {"class": "items"}).find_all("li")
            for anime in animes:
                tit = anime.a["title"]
                urll = anime.a["href"]
                res_list_search.append({"name":f"{tit}","Id-Epnum":f"{urll[1:]}"})
            if res_list_search == []:
                return {"status":"204", "reason":"I have No Idea what the fuck went wrong"}
            else:
                return res_list_search
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}
    
    def jugad(animeid, episode_num):
        url = f"https://www1.gogoanime.ai/{animeid}-episode-{episode_num}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        response = requests.get(url, headers=headers)
        plainText = response.text
        with open("test.html", "w", encoding="utf-8") as f:
            f.write(plainText)
        soup = BeautifulSoup(plainText, "lxml")
        links = soup.find("div", {"class":"anime_muti_link"}).find_all("li")
        result = {}
        for link in links:
            server = link.text
            server = server.replace("Choose this server", "")
            server = server.replace("\n", "")
            ep_url = link.a["data-video"]
            if ep_url.startswith("//"):
                ep_url = ep_url[2:]
            result[server] = ep_url
        return result

    
    
    
