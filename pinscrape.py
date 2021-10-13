#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import os
import sys
import getopt
import requests
import sqlite3

def set_browser(url):
    driver = webdriver.Firefox()
    driver.get(url)
    return driver


# Download images and insert them into database
def download_images(url_list, dbfile='data.sqlite'):
    with sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        # check existence of database
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS images
                    (id TEXT, file_name TEXT, custom_title TEXT, url TEXT, img_url TEXT, PRIMARY KEY(id,url))''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_id ON images (id)''')

        for pic_url in url_list:
            current_dir = os.path.join(os.curdir, "downloaded_imgs")
            pic_name = pic_url.rsplit('/', 1)[-1]
            c.execute('SELECT id, file_name, custom_title, url, img_url FROM images WHERE img_url=?', (pic_url,))
            r = c.fetchone()
            if r == None:
                print(pic_name)
                pic = requests.get(pic_url)
                with open(os.path.join(current_dir, pic_name), 'wb') as file:
                    if not pic.ok:
                        continue

                    for block in pic.iter_content(1024):
                        if not block:
                            break
                        file.write(block)

                c.execute(f"INSERT INTO images VALUES('{pic_name}', '{pic_name}', '', '{url}','{pic_url}')")





# Number of scrolls is needed, there is no good way to find end of board
# Portions taken from another pinterest scraper: https://github.com/eamander/Pinterest_scraper/blob/master/pinterest_scraper.py
def run(url, number_of_scrolls = 2, number_of_pics = -1):
    browser = set_browser(url)
    counter = 0 #temporary
    sleep(3)
    scrapped_list = []
    counting_pics = 0;
    while(1):
        pic_list = browser.find_elements_by_xpath('//div[contains(@class, "PinCard__imageWrapper")]//div//div//div//div//img')
        pic_url_list = [pic_elem.get_attribute('src') for pic_elem in pic_list]
        end = False
        for pic_url in pic_url_list:
            # change url 236x to originals
            pic_url = pic_url.replace('https://i.pinimg.com/236x', 'https://i.pinimg.com/originals')
            # if not in list, add it in
            if pic_url not in scrapped_list:
                counting_pics = counting_pics + 1
                scrapped_list.append(pic_url)
                # check number of pics downloaded, if limited by user
                if(number_of_pics != -1 and counting_pics >= number_of_pics):
                    end = True
                    break

        # break from pic_url_list loop
        if(end):
            break


        # scroll down
        body = browser.find_element_by_css_selector('body')
        for j in range(2):
            body.send_keys(Keys.PAGE_DOWN)

        # hack to make it load
        sleep(2)

        # check number of scrolls
        if(counter > number_of_scrolls):
            break

        counter = counter + 1

    browser.close()
    download_images(scrapped_list)

if __name__ == "__main__":
    url = ''
    scrolls = 2
    pics = -1
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:s:p:", ["url=", "scrolls=", "pics="])
    except getopt.GetoptError:
        print('pinscrape.py -u <url of board> -s <number of scrolls> -p <number of pics>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('pinscrape.py -u <url of board> -s <number of scrolls> -p <number of pics>')
            sys.exit()
        elif opt in ('-u', '--url'):
            url = arg
        elif opt in ('-s', '--scrolls'):
            scrolls = int(arg)
        elif opt in ('-p', '--pics'):
            pics = int(arg)

    run(url, scrolls, pics)
