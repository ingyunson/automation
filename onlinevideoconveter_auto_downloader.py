from selenium import webdriver
import time
import random

url = ['#URL ¸®½ºÆ®']

driver = webdriver.Chrome('./chromedriver')
errors = []

for down in url:
    try:
        driver.get('https://www.onlinevideoconverter.com/ko/video-converter')
        driver.find_element_by_css_selector('#texturl').send_keys(down)
        driver.find_element_by_css_selector('#select_main').click()
        driver.find_element_by_css_selector('#select_main > div > ul:nth-of-type(2) > li:nth-of-type(2) > a').click()
        driver.find_element_by_css_selector('#convert1').click()

        time.sleep(60)

        driver.find_element_by_css_selector('#downloadq').click()
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(60)

    except Exception as e:
        print(e)
        errors.append(down)



print(errors)