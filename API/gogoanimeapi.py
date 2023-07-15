import requests
from bs4 import BeautifulSoup

class Gogo:
    def __init__(self, gogoanime_token: str, auth_token: str, host: str):
        self.gogoanime_token = gogoanime_token
        self.auth_token = auth_token
        self.host = host

    def get_search_results(self, query):
        try:
            url1 = f"https://www.{self.host}/search.html?keyword={query}"
            response = requests.get(url1)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            res_list_search = []
            for anime in animes:  
                tit = anime.text.strip().split("\n")[0]
                urll = anime.a["href"]
                r = urll.split('/')
                res_list_search.append({"title":tit, "animeid":r[2]})
            
            if res_list_search == []:
                return {"status":"204", "reason":"I have No Idea what the fuck went wrong"}
            else:
                return res_list_search
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}

    def get_anime_details(self, animeid):
        try:
            animelink = f'https://www.{self.host}/category/{animeid}'
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
            res_detail_search = {
                "title":tit_url,
                "year":int(year),
                "other_names":oth_names,
                "season":type_of_show,
                "status":status,
                "genres":", ".join(genres),
                "episodes":int(ep_num),
                "image_url":imgg,
                "summary":plot_summary
            }
            return res_detail_search
        
        except AttributeError:
            return {"status":"400", "reason":"Invalid animeid"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}
   
    def get_episodes_link(self, animeid, episode_num):
        try:
            url = f'https://www.{self.host}/{animeid}-episode-{episode_num}'
            cookies = {
                'gogoanime': self.gogoanime_token,
                'auth': self.auth_token
            }
            response = requests.get(url=url, cookies=cookies)
            plaintext = response.text
            soup = BeautifulSoup(plaintext, "lxml")
            download_div = soup.find("div", {'class': 'cf-download'}).findAll('a')
            result = {}  
            for links in download_div:
                download_link = links['href']
                quality_name = links.text.strip().split('x')[1]
                result[quality_name] = download_link
            return result
        except AttributeError:
            try:
                animeid = animeid.replace("-tv", "")
                url = f'https://www.{self.host}/{animeid}-episode-{episode_num}'
                cookies = {
                    'gogoanime': self.gogoanime_token,
                    'auth': self.auth_token
                }
                response = requests.get(url=url, cookies=cookies)
                plaintext = response.text
                soup = BeautifulSoup(plaintext, "lxml")
                download_div = soup.find("div", {'class': 'cf-download'}).findAll('a')
                result = {}  
                for links in download_div:
                    download_link = links['href']
                    quality_name = links.text.strip().split('x')[1]
                    result[quality_name] = download_link
                return result
            except:
                return {"status":"400", "reason":"Invalid animeid or episode_num"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}            

    def get_home_page(self):
        try:
            response = requests.get(f"https://www.{self.host}")
            response_html = response.text

            soup = BeautifulSoup(response_html, 'lxml')
            res_list_search =[]
            animes =  soup.find("ul", {"class": "items"}).find_all("li")
            for anime in animes:
                tit = anime.a["title"]
                urll = anime.a["href"]
                res_list_search.append({"name":f"{tit}","Id-Epnum":f"{urll[1:]}"})
            if res_list_search == []:
                return {"status":"204", "reason":"Need to refresh token"}
            else:
                return res_list_search
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}
        
    def get_stream_link(self, animeid, episode_num):
        try:
            animeid = animeid.replace("-tv", "")
            url = f"https://www.{self.host}/{animeid}-episode-{episode_num}"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            response = requests.get(url, headers=headers)
            plainText = response.text
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
        except AttributeError:
            return {"status":"400", "reason":"Invalid animeid"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}