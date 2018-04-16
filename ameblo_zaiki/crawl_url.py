import codecs
import datetime
import re
import string

import requests
from bs4 import BeautifulSoup

import param


def download_page(url):
    return requests.get(url).content


def parse_html(html, for_search=False):
    """
    :param html: blog main page
    :param for_search: whether use to crawl image (title will be format, string.punctuation will be replaced by X)
    :return: blog links, link for next page or None if there is no next page
    """
    blog_list_urls = []

    # get url and title
    soup = BeautifulSoup(html, 'html.parser')
    blog_list_soup = soup.find('ul', attrs={'class': 'skin-archiveList'})
    for blog_li in blog_list_soup.find_all('li'):
        update_array = re.split('\D', blog_li.find('p', attrs={'class': 'skin-textQuiet'}).getText())
        update_array = [e for e in update_array if e != '']
        update_time = datetime.date(int(update_array[0]), int(update_array[1]), int(update_array[2]))
        # if update_time > param.latest_date:
        if update_time < param.latest_date:
            a = blog_li.find('h2').find('a')
            link = a['href']
            title = a.getText().strip()
            if for_search:
                for e in string.punctuation:
                    title = title.replace(e, 'X')  # 妈呀这货颜文字多的，建文件夹时真心累
            blog_list_urls.append(link + "," + title + " ," + update_time.__str__())
        else:
            return blog_list_urls, None

    # get next page
    next_page = soup.find('a', attrs={'class': 'js-paginationNext'})
    print(next_page)
    try:
        return blog_list_urls, next_page['href']
    except Exception as e:
        return blog_list_urls, None


if __name__ == '__main__':
    current_url = param.URL
    with codecs.open(param.blog_link_txt_name, 'wb', encoding='utf-8') as fp:
        while current_url:
            current_html = download_page(current_url)
            # urls, current_url = parse_html(current_html)
            urls, current_url = parse_html(current_html, True)
            fp.write('{urls}\n'.format(urls='\n'.join(urls)))
            print('{urls}\n'.format(urls='\n'.join(urls)))
            print('\n')
