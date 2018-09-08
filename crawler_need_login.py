from selenium import webdriver
from bs4 import BeautifulSoup as bs


#크롬 드라이버 가져옴
driver = webdriver.Chrome('./chromedriver')

#대상 페이지를 불러오고 로그인하기
driver.get('#Login URL')
driver.find_element_by_css_selector('#CSS selector of ID form').send_keys("#input ID")
driver.find_element_by_css_selector('#CSS selector of password form').send_keys("#input password")
driver.find_element_by_css_selector('#CSS selector of login button').click()


#대상 페이지를 불러오기
driver.get('#target site URL')

#페이지의 소스를 html 변수로 저장하기
html = driver.page_source
driver.quit()

#html 변수를 lxml로 파싱하여 soup로 저장하기
soup = bs(html, 'lxml')
crawling = soup.select('#CSS selector of target area')

'''
#반복해서 목록을 크롤링하는 경우

for i in crawling :
    print(i.text)
'''

print(crawling)

