from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

class gogoanime():
    def __init__(self, query, animeid, episode_num, genre_name, page):  # Intialises the anime class
        self.query = query
        self.animeid = animeid
        self.episode_num = episode_num
        self.genre_name = genre_name
        self.page = page

    def get_search_results(query):
        try:
            url1 = f"https://gogoanime.ai//search.html?keyword={query}"
            session = HTMLSession()
            response = session.get(url1)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            # print(animes)
            res_list_search = []
            for anime in animes:  # For every anime found
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
            ai = lis[2].find_all('a')  # .find_all('title')
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
            # print(vidstream_link)
            URL = vidstream_link
            dowCode = requests.get(URL)
            data = dowCode.text
            soup = BeautifulSoup(data, "lxml")
            dow_url1 = soup.findAll('div', {'class': 'dowload'})[0].find('a')
            dow_url2 = soup.findAll('div', {'class': 'dowload'})[1].find('a')
            dow_url3 = soup.findAll('div', {'class': 'dowload'})[2].find('a')
            dow_url4 = soup.findAll('div', {'class': 'dowload'})[3].find('a')
            dow_url5 = soup.findAll('div', {'class': 'dowload'})[4].find('a')
            try:
                dow_url6 = soup.findAll('div', {'class': 'dowload'})[5].find('a')
            except:
                pass
            try:
                dow_url7 = soup.findAll('div', {'class': 'dowload'})[6].find('a')
            except:
                pass


            downlink1 = dow_url1.get('href')
            downlink2 = dow_url2.get('href')
            downlink3 = dow_url3.get('href')
            downlink4 = dow_url4.get('href')
            downlink5 = dow_url5.get('href')
            try:
                downlink6 = dow_url6.get('href')
            except:
                pass
            try:
                downlink7 = dow_url7.get('href')
            except:
                pass    

            str1 = dow_url1.string
            str_spl1 = str1.split()
            str_spl1.remove(str_spl1[0])
            str_original_1 = ""
            quality_name1 = str_original_1.join(str_spl1)

            str2 = dow_url2.string
            str_spl2 = str2.split()
            str_spl2.remove(str_spl2[0])
            str_original_2 = ""
            quality_name2 = str_original_2.join(str_spl2)

            str3 = dow_url3.string
            str_spl3 = str3.split()
            str_spl3.remove(str_spl3[0])
            str_original_3 = ""
            quality_name3 = str_original_3.join(str_spl3)

            str4 = dow_url4.string
            str_spl4 = str4.split()
            str_spl4.remove(str_spl4[0])
            str_original_4 = ""
            quality_name4 = str_original_4.join(str_spl4)

            str5 = dow_url5.string
            str_spl5 = str5.split()
            str_spl5.remove(str_spl5[0])
            str_original_5 = ""
            quality_name5 = str_original_5.join(str_spl5)
            try:
                str6 = dow_url6.string
                str_spl6 = str6.split()
                str_spl6.remove(str_spl6[0])
                str_original_6 = ""
                quality_name6 = str_original_6.join(str_spl6)
            except:
                pass
            try:
                str7 = dow_url7.string
                str_spl7 = str7.split()
                str_spl7.remove(str_spl7[0])
                str_original_7 = ""
                quality_name7 = str_original_7.join(str_spl7)
            except:
                pass
            try:
                episode_res_link = {'title':f"{tit_url}", f"{quality_name1}":f"{downlink1}", f"{quality_name2}":f"{downlink2}", f"{quality_name3}":f"{downlink3}", f"{quality_name4}":f"{downlink4}", f"{quality_name5}":f"{downlink5}", f"{quality_name6}":f"{downlink6}", f"{quality_name7}":f"{downlink7}"}
            except:
                episode_res_link = {'title':f"{tit_url}", f"{quality_name1}":f"{downlink1}", f"{quality_name2}":f"{downlink2}", f"{quality_name3}":f"{downlink3}", f"{quality_name4}":f"{downlink4}", f"{quality_name5}":f"{downlink5}"}
            return episode_res_link

        except AttributeError:
            return {"status":"400", "reason":"Invalid animeid or episode_num"}
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}

    def get_by_genre(genre_name, page):
        try:
            url = f"https://gogoanime.ai/genre/{genre_name}?page={page}"
            response = requests.get(url)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            gen_ani_res = [{"genre":f"{genre_name}"}]
            gen_ani = []
            for anime in animes:  # For every anime found
                tits = anime.a["title"]
                urll = anime.a["href"]
                r = urll.split('/')
                gen_ani.append({"title":f"{tits}", "animeid":f"{r[2]}"})
            gen_ani_res.append(gen_ani)
            return gen_ani_res
        except AttributeError or KeyError:
            return {"status":"400", "reason":"Invalid genre_name or page_num"}
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}