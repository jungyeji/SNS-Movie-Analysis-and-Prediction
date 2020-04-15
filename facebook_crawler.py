from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pandas import Series, DataFrame
from openpyxl import Workbook
import pandas as pd
import time
import json

# 영화리스트 가져오기(검색어로 사용할 영화명)
f = open("test.txt",'r')
movie_list = []
while True:
    line = f.readline()
    if not line: break
    line = line.split('\n')[0]
    movie_list.append(line)
f.close()
movie_list

path = "./chromedriver.exe"
driver = webdriver.Chrome(path)

driver.implicitly_wait(3)

driver.get('https://www.facebook.com/')

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

## 로그인하기
email = driver.find_element_by_xpath("//input[@name='email']")
password = driver.find_element_by_xpath("//input[@name='pass']")
btn = driver.find_element_by_xpath("//input[@value='로그인']")

email.send_keys("ID")
password.send_keys("pw")
btn.click()

# 키워드 검색하기
def search(key):
    try:
        searchbox = driver.find_element_by_xpath("//form[@action='https://www.facebook.com/search/web/direct_search.php']//input[2]")
        time.sleep(1)
        searchbox.send_keys(key)
    except:
        searchbox = driver.find_element_by_xpath("//form[@action='/search/web/direct_search.php']//input[2]")
        time.sleep(1)
        searchbox.send_keys(key)

    time.sleep(1)
    driver.find_element_by_xpath("//button[@value='1']").submit()

def scroll_down():
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        time.sleep(7)


# 모두 보기
## 지금은 사용하지 않음
def select_option():
    add_button = driver.find_element_by_xpath("//div[@class='_4jq5']/div[text()='게시물']")
    driver.execute_script("arguments[0].click();", add_button)

    add_button = driver.find_element_by_xpath("//div[@data-testid='results']/div/div/div/div/a[text()='모두 보기']")
    driver.execute_script("arguments[0].click();", add_button)

    #add_button = driver.find_element_by_xpath('//*[@class="_4f38"][2]/div/a[@class="_4f3b"][2]')
    #driver.execute_script("arguments[0].click();", add_button)

def parser(str):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    c_post = soup.select('div._3ccb')

    contents = []
    dates = []
    likes = ['0' for _ in range(len(c_post))]
    comments = ['0' for _ in range(len(c_post))]
    shares = ['0' for _ in range(len(c_post))]
    shows =  ['0' for _ in range(len(c_post))]
    i = 0
    error = 0
    for posting in c_post:
        #내용, 게시날짜
        try:
            contents.append(posting.find("div",{"class":"userContent"}).text)
        except:
            error = 1+error
            print(posting.text)
            continue
        dates.append(posting.find("span",{"class":"timestampContent"}).text)

        if posting.find("div",{"class":"_ipo"}):
            # 댓글,공유,조회수
            for info in posting.find("div",{"class":"_ipo"}):
                try:
                    temp = info.find("a").text
                    if temp.find("댓글")>=0:
                        comments[i] = temp[3:-1]
                    elif temp.find("공유")>=0:
                        shares[i] = temp[3:-1]
                except:
                    shows[i] = info.find("span").text[3:-1]

        # 좋아요
        if posting.find("span",{"class":"_4arz"}):
            for info in posting.find("span",{"class":"_4arz"}):
                if(info.text.find('외')!=-1):
                    atpos = info.text.find('외')
                    sppos = info.text.find('명',atpos)
                    likes[i] = info.text[atpos+2 : sppos]
                else:
                    likes[i] = info.text[: -1]

        i = i+1
    if error >=1 :
        likes = likes[:-error]
        comments = comments[:-error]
        shares = shares[:-error]
        shows =  shows[:-error]

    dates = [datechange(i) for i in dates]
    comments = [numberchange(i) for i in comments]
    likes = [numberchange(i) for i in likes]
    shows = [numberchange(i) for i in shows]
    shares = [numberchange(i) for i in shares]

    Posts = {'MovieName':str,"Review":contents,"Date":dates,"Rate":0,"Comments":comments,"Likes":likes,"Shares":shares,"Shows":shows,"Retweet":0,"SNS":"facebook"}

    post_df = DataFrame(Posts)
    print('error=',error)
    return post_df


# 글자를 숫자로 변환
def numberchange(str):
    try:
        if(str.find('천') >= 0):
            if(str.find('.') == -1):
                str = str.replace('천','')
                str = str+'000'
            else:
                str = str.replace('.','')
                str = str.replace('천','')
                str = str+'00'
        elif(str.find('만') >= 0):
            if(str.find('.') == -1):
                str = str.replace('만','')
                str = str+'0000'
            else:
                str = str.replace('.','')
                str = str.replace('만','')
                str = str+'000'
        str = str.replace(',','')
    except:
        print("already complete")
    return str

# 날짜형식을 통일시킴
from datetime import datetime, timedelta
def datechange(str_date):
    try:
        if(str_date.find("일")==-1):
            if(str_date.find("시간")>=0):
                edit_hour = int(str_date.replace("시간",""))
                edit_date = datetime.now() - timedelta(hours=edit_hour)

            elif(str_date.find("분")>=0):
                edit_min = int(str_date.replace("분",""))
                edit_date = datetime.now() - timedelta(seconds=edit_min*60)

            if edit_date.month<10:
                str_date = str(edit_date.year) + "-0" + str(edit_date.month) + "-" + str(edit_date.day)
            else:
                str_date = str(edit_date.year) + "-" + str(edit_date.month) + "-" + str(edit_date.day)

        elif(str_date.find("년") == -1):
            str_date = "2018-" + str_date

        str_date = str_date.replace(" ","")
        str_date = str_date.replace("년","-")
        atpos = str_date.find("-")
        endpos = str_date.find("월")
        if(endpos-atpos == 2):
            str_date = str_date.replace("-","-0")

        str_date = str_date.replace("월","-")
        str_date = str_date.replace("일","")
        str_date = str_date.replace(" ","")

    except:
        print("already complete")

    try:
        if(str_date.find(":") >=0):
            if(str_date.find("오전")>=0):
                str_date = str_date[:str_date.find("오전")]
            elif(str_date.find("오후")>=0):
                str_date = str_date[:str_date.find("오후")]
    except:
        print("already complete")

    if(str_date.find("어제")>=0):
        edit_date = datetime.now() - timedelta(days=1)
        str_date = str(edit_date.year) + "-" + str(edit_date.month) + "-" + str(edit_date.day)

    return str_date

for movie in movie_list:
    try:
        #search(movie)
        #select_option()
        #scroll_down()
        driver.get('https://www.facebook.com/search/str/'+movie+'/stories-keyword/stories-public')
        scroll_down()
        data = parser(movie)

        writer = pd.ExcelWriter(movie+'Facebook.xlsx')
        data.to_excel(writer,'Sheet1')
        writer.save()
        print(movie)
    except:
        print(movie+'  - 실패')
        pass
    
