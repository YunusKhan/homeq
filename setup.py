import csv, re, os
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import webbrowser as web
import pyautogui as pg
from pathlib import Path

def runner():
    url = "https://www.homeq.se/search?selectedShapes=metropolitan_area.8%3B8c2a29cf2222d13142db38ba811ab69d5d579f21ead150d5985f68070586548e%3BG%C3%B6teborg"
    browser = webdriver.Firefox()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find('section', 'wrapper')
    browser.quit()
    listhomes = []
    listnewhomes = []
    userpath = str(Path.home())
    filename = userpath + '\\Documents\\allhomes.csv'

    f = open(filename, 'a+', encoding="utf-8")
    f.close()

    with open(filename, 'r', encoding="utf-8") as csvfile:
        rf = csv.reader(csvfile)
        for row in rf:
            listhomes = list(itertools.chain(*rf))
    csvfile.close()
    #print(soup)

    with open(filename, 'a+', newline='', encoding="utf-8") as csvfile:
        wf = csv.writer(csvfile)
        for tag in soup.find_all('a', href=True):
            if "https://www.homeq.se/lagenhet/" in tag['href'] or "https://www.homeq.se/estate/" in tag['href']:
                if '2rum' in tag['href'] or '3rum' in tag['href']:
                    curr_url = str(tag['href'])
                    #print(curr_url)
                    if curr_url not in listhomes:
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
                        listnewhomes.append([tag['href'], dates, pricing])
                        wf.writerow([tag['href'], dates, pricing])

    csvfile.close()
    time.sleep(10)
    print(listnewhomes)
    #TODO - send message cleanly
    if len(listnewhomes) != 0:
        lead = '+919945073307'
        web.open("https://web.whatsapp.com/send?phone="+lead+"&text="+str(listnewhomes))
        width,height = pg.size()
        
        pg.click(width/2,height/2)
        time.sleep(8)
        pg.press('enter')
        time.sleep(8)
        pg.hotkey('ctrl', 'w')

if __name__ == "__main__":
    while(1):
        runner()
        time.sleep(900)
