import codecs
import re

import datetime
import requests
from bs4 import BeautifulSoup

URL = "https://search.ameba.jp/search.html?q=%E3%80%90%E7%B4%8D%E8%B0%B7%E5%81%A5%E3%80%91&target=id&aid=patch-west&author=all&row=10&prevRow=10&profileRow="


def download_page(url):
    return requests.get(url).content


def parse_html(html):
    blog_list_urls = []

    # get url and title
    soup = BeautifulSoup(html, 'html.parser')
    blog_list_soup = soup.find('ul', attrs={'class': 'seachResult'})
    for blog_li in blog_list_soup.find_all('li'):
        update_array = re.split('\D', blog_li.find('span', attrs={'class': 'updateTime'}).getText())
        update_time = datetime.date(int(update_array[1]), int(update_array[2]), int(update_array[3]))
        if update_time > datetime.date(2017, 10, 31):
            a = blog_li.find('a', attrs={'class': 'areaClick'})
            link = a['href']
            title = a.find('h3').getText()
            blog_list_urls.append(link + "," + title + " ," + update_time.__str__())

    # get next page
    # next_page = soup.find('div', attrs={'class': 'cmnPaging'}).find('a', attrs={'class': 'fwd'})
    # if next_page:
    #     return blog_list_urls, 'https:' + next_page['href']
    return blog_list_urls, None


if __name__ == '__main__':
    current_url = URL
    with codecs.open('blog_link_180116.txt', 'wb', encoding='utf-8') as fp:
        while current_url:
            current_html = download_page(current_url)
            urls, current_url = parse_html(current_html)
            fp.write('{urls}\n'.format(urls='\n'.join(urls)))
            print('{urls}\n'.format(urls='\n'.join(urls)))
