import datetime
import urllib.request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

PIXEL_PER_SCROLL = 500
SCROLL_PAUSE_SEC = 2

def scroll_down(driver):
    h = PIXEL_PER_SCROLL
    while True:
        driver.execute_script(f"window.scrollTo(0, {h});")
        time.sleep(SCROLL_PAUSE_SEC)
        last_height = driver.execute_script("return document.body.scrollHeight")
        curr = driver.execute_script("return window.innerHeight")
        yOffset = driver.execute_script("return pageYOffset")
        h += PIXEL_PER_SCROLL
        # print(f'curr = {curr} yOffset = {yOffset} last_height = {last_height}')
        if yOffset + curr >= last_height:
            break

def scrap_icons():
    page = range(1, 91)
    url = 'https://coinmarketcap.com/?page='

    for idx in page:
        page = url + str(idx)
        driver = webdriver.Chrome()
        driver.get(page)

        time.sleep(1)
        scroll_down(driver)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')
        images = tbody.find_all('img', attrs={'class': 'coin-logo'})
        symbols = tbody.find_all('p', attrs={'class': 'sc-e225a64a-0 dfeAJi coin-item-symbol'})
        print(f'page = {idx} saves images = {len(images)} symbols = {len(symbols)}')
        for i in range(len(images)):
            img_url = images[i]['src']
            img_symbol = symbols[i].decode_contents()

            with urllib.request.urlopen(img_url) as f:
                with open('./img/' + str(img_symbol) + '.png', 'wb') as h:
                    img = f.read()
                    h.write(img)


if __name__ == '__main__':
    scrap_icons()
