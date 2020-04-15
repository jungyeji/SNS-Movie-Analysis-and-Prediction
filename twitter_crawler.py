from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import  FirefoxBinary
from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
import datetime as dt
import csv

binary  = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
browser = webdriver.Firefox(executable_path='C:/Users/yeji/geckodriver.exe',firefox_binary=binary)

# 검색할 영화 리스트 파일 열기
movieListFile  = open('movie50.txt', 'r')

# 한 줄씩 읽기
line = movieListFile.readline()
while line:
    # delimiter: Tab
    pair = line.split('\t')
    moviename = pair[0]
    title = moviename.replace(':','') + 'twitter.csv'
    outputFile = open(title, 'w', encoding='euc-kr', newline = '')
    csvWriter = csv.writer(outputFile)
    csvWriter.writerow(['moviename', 'date', 'review', 'rate', 'likes', 'comments', 'shares','shows', 'snsflag'])                   

    # :과 -는 OR로 바꿈 -> 검색어
    keyword = moviename.replace(':', ' OR').replace(',', '').replace('-',' OR ')

    # 검색할 기간 설정, untilDate는 커서 역할
    released_date = pair[1].replace('\n','').split('-')

    startDate = dt.date(year = int(released_date[0]), month = int(released_date[1]), day = int(released_date[2])) - dt.timedelta(days = 7)
    untilDate = startDate + dt.timedelta(days = 1)
    endDate   = startDate + dt.timedelta(days = 14)

    # startDate = dt.date(year = int(released_date[0]), month = int(released_date[1]), day = int(released_date[2]))
    # untilDate = startDate + dt.timedelta(days = 1)
    # endDate   = untilDate

    # startDate ~ untilDate 의 트윗 크롤링 반복
    while not endDate == startDate:
        url  = 'https://twitter.com/search?q=' + \
        keyword + '%20since%3A' + str(startDate) + '%20until%3A'+ str(untilDate)+'&amp;amp;amp;amp;amp;amp;lang=ko'
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')

        newHeight  = -1
        lastHeight = browser.execute_script("return document.body.scrollHeight")
        # 맨 밑까지 스크롤다운
        while not newHeight == lastHeight:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4) # 로딩 될 때 까지 기다리는 시간
            lastHeight = newHeight
            newHeight  = browser.execute_script("return document.body.scrollHeight")
            
            
        html          = browser.page_source
        soup          = BeautifulSoup(html,'html.parser')
        tweets        = soup.find_all("p", {"class": "TweetTextSize"})
        reply_html    = soup.find_all("div", {"class": "ProfileTweet-action--reply"})
        favorite_html = soup.find_all("div", {"class": "ProfileTweet-action--favorite"})
        retweet_html  = soup.find_all("div", {"class": "ProfileTweet-action--retweet"})

        replies   = []
        favorites = []
        retweets  = []

        for i in range(len(reply_html)):
            replies.append(reply_html[i].find("span", {"class": "ProfileTweet-actionCountForPresentation"}))
            favorites.append(favorite_html[i].find("span", {"class": "ProfileTweet-actionCountForPresentation"}))
            retweets.append(retweet_html[i].find("span", {"class": "ProfileTweet-actionCountForPresentation"}))

        for i in range(len(tweets)):
            tweet    = tweets[i].get_text(strip=True).replace('\n', ' ')
            reply    = replies[i].get_text(strip=True)
            favorite = favorites[i].get_text(strip=True)
            retweet  = retweets[i].get_text(strip=True)
            
            if reply == '':
                reply = 0
            else:
                reply = int(reply.replace(',', ''))

            if favorite == '':
                favorite = 0 
            else:
                favorite = int(favorite.replace(',', ''))

            if retweet == '':
                retweet = 0
            else:
                retweet = int(retweet.replace(',', ''))
            
            writeLine = [moviename, startDate, tweet, '', favorite, reply, retweet, '', 'twitter']
            #예외처리
            try:
                csvWriter.writerow(writeLine)
            except UnicodeEncodeError :
                pass                   

        # 커서 이동
        startDate  = untilDate
        untilDate  = untilDate + dt.timedelta(days = 1)

    # 다음 영화 읽기
    line = movieListFile.readline()

movieListFile.close()
outputFile.close()