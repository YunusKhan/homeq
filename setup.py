import csv
import re
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import webbrowser as web
import pyautogui as pg
from pathlib import Path


def runner():
    url = "https://www.homeq.se/search?selectedShapes=metropolitan_area.8" \
          "%3B8c2a29cf2222d13142db38ba811ab69d5d579f21ead150d5985f68070586548e%3BG%C3%B6teborg "
    browser = webdriver.Firefox()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # a = soup.find('section', 'wrapper')
    browser.quit()
    list_homes = []
    list_new_homes = []
    user_path = str(Path.home())
    filename = user_path + '\\Documents\\all_homes.csv'

    f = open(filename, 'a+', encoding="utf-8")
    f.close()

    with open(filename, 'r', encoding="utf-8") as csv_file:
        rf = csv.reader(csv_file)
        list_homes = list(itertools.chain(*rf))
    csv_file.close()

    with open(filename, 'a+', newline='', encoding="utf-8") as csv_file:
        wf = csv.writer(csv_file)
        for tag in soup.find_all('a', href=True):
            if "https://www.homeq.se/lagenhet/" in tag['href'] or "https://www.homeq.se/estate/" in tag['href']:
                if '2rum' in tag['href'] or '3rum' in tag['href']:
                    curr_url = str(tag['href'])
                    # print(curr_url)
                    if curr_url not in list_homes:
                        print(curr_url)
                        browser = webdriver.Firefox()
                        browser.get(curr_url)
                        html = browser.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        rows = str(soup.findAll('div', attrs={'class': 'homeq-ad-dates'}))
                        dates = re.sub('<[^>]*>', '', rows)
                        rows = str(soup.findAll('div', attrs={'class': 'homeq-ad-numbers'}))
                        pricing = re.sub('<[^>]*>', '', rows)

                        browser.quit()
                        time.sleep(2)
                        list_new_homes.append([tag['href'], dates, pricing])
                        wf.writerow([tag['href'], dates, pricing])

    csv_file.close()
    time.sleep(10)
    print(list_new_homes)
    # TODO - send message cleanly
    if len(list_new_homes) != 0:
        lead = '+919945073307'
        web.open("https://web.whatsapp.com/send?phone=" + lead + "&text=" + str(list_new_homes))
        width, height = pg.size()

        pg.click(width / 2, height / 2)
        time.sleep(30)
        pg.press('enter')
        time.sleep(30)
        pg.hotkey('ctrl', 'w')
    else:
        return
    return


if __name__ == "__main__":
    while 1:
        t = 900
        runner()
        while t:
            minutes, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(minutes, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
