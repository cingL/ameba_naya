import codecs
import os
import time

import requests
from bs4 import BeautifulSoup

from crawl_url import download_page
# get all passage urls from blog_link.txt
from param import blog_link_txt_name


def get_url():
    links = {}
    with codecs.open(blog_link_txt_name, 'rb', 'utf-8') as f:
        for line in f:
            # print(line.split(',')[0])
            arr = line.split(',')
            url = arr[0]
            title = arr[1].rstrip()
            links[url] = title

    return links


def crawl(url, prefix):
    """
    :param url: blog url
    :param prefix: blog title
    """
    html = download_page(url)
    soup = BeautifulSoup(html, 'html.parser')

    # create dir with the date of passage
    time = soup.find('time')['datetime']
    print('time = ' + time)
    if not os.path.exists(time):
        os.mkdir(time)
    # named image with title and index
    # all_a = soup.find_all('a', attrs={'class': 'detailOn'}) -> soup读出来找不到了，懒加载了？
    all_a = soup.find_all('a')
    index = 0
    for each_a in all_a:
        img = each_a.find('img')
        if img is not None:
            img_link = img['src']
            if img_link[-3:] == '800':
                index += 1
                img_path = './' + time + '/' + prefix + '-' + index.__str__() + '.jpg'
                print('img_name = ' + img_path)
                print('img_link = ' + img_link)
                img_r = requests.get(img_link, stream=True)
                if img_r.status_code == 200:
                    with open(img_path, 'wb') as f:
                        for chunk in img_r.iter_content(1024):
                            f.write(chunk)


if __name__ == '__main__':

    s_time = time.time()

    all_blog_link = get_url()
    for ame_link in all_blog_link:
        print(ame_link + ', ' + all_blog_link[ame_link])
        crawl(ame_link, all_blog_link[ame_link])

    e_time = time.time()
    cost = e_time - s_time
    print('cost = ' + time.strftime('%M:%S', time.gmtime(cost)))
