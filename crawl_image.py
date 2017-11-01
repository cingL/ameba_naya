import codecs
import os

import requests
import time
from bs4 import BeautifulSoup

from crawl_url import download_page


# get all passage urls from blog_link.txt
def get_url():
    links = {}
    with codecs.open('blog_link.txt', 'rb', 'utf-8') as f:
        for line in f:
            # print(line.split(',')[0])
            arr = line.split(',')
            url = arr[0]
            title = arr[1].rstrip()
            links[url] = title

    return links


def crawl(url, prefix):
    html = download_page(url)
    soup = BeautifulSoup(html, 'html.parser')

    # create dir with the date of passage
    time = soup.find('time')['datetime']
    print('time = ' + time)
    if not os.path.exists(time):
        os.mkdir(time)
    # named image with title and index
    all_a = soup.find_all('a', attrs={'class': 'detailOn'})
    for index in range(len(all_a)):
        a = all_a[index]
        img_link = a.find('img')['src']
        img_path = './' + time + '/' + prefix[5:] + '-' + (index + 1).__str__() + '.jpg'
        print('img_name = ' + img_path)
        print('img_link = ' + img_link)
        img_r = requests.get(img_link, stream=True)
        if img_r.status_code == 200:
            with open(img_path, 'wb') as f:
                for chunk in img_r.iter_content(1024):
                    f.write(chunk)


"""
 cost = 36:30
 total 202 post
"""
if __name__ == '__main__':

    s_time = time.time()

    all_blog_link = get_url()
    for ame_link in all_blog_link:
        print(ame_link + ', ' + all_blog_link[ame_link])
        crawl(ame_link, all_blog_link[ame_link])

    e_time = time.time()
    cost = e_time - s_time
    print('cost = ' + time.strftime('%M:%S', time.gmtime(cost)))
