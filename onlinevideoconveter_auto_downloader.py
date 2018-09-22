from selenium import webdriver
import time
import os

file = open('<filename.txt>', 'r') #filename.txt는 url이 있는 파일
url = file.read().splitlines()
file.close()

driver = webdriver.Chrome('./chromedriver')
errors = []

def downloads_done(dirname):
    filenames = os.listdir(dirname)
    for i in filenames:
        if ".crdownload" in i:
            print('not download completed')
            time.sleep(60)
            downloads_done(dirname)
        else :
            pass

def download():
    for down in url:
        try:
            driver.get('https://www.onlinevideoconverter.com/ko/video-converter')
            driver.find_element_by_css_selector('#texturl').send_keys(down)
            driver.find_element_by_css_selector('#select_main').click()
            driver.find_element_by_css_selector('#select_main > div > ul:nth-of-type(2) > li:nth-of-type(2) > a').click()
            driver.find_element_by_css_selector('#convert1').click()

            time.sleep(30)
            downloads_done("<chrome default download folder>") #chrome default download folder는 크롬 다운로드 지정 폴더
            driver.find_element_by_css_selector('#downloadq').click()
            driver.switch_to.window(driver.window_handles[0])

            time.sleep(10)

        except Exception as e:
            print(e)
            errors.append(down)

download()

print(errors)
