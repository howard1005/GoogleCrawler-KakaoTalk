from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time as tm
import pdb

def waitClickElementhUntilExistXpath(driver, click_element, exist_xpath):
    while(1):
        print("click")
        tm.sleep(1)
        click_element.click()
        tm.sleep(1)
        element = driver.find_elements_by_xpath(exist_xpath)
        print("element : {}".format(element))
        if len(element) > 0:
            break
    return element


def chromeDebug(url):
    ### 크롬 debug ###
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    element = driver.find_element_by_name('q')
    element.send_keys("펭수")
    element.submit()
    driver.implicitly_wait(10)
    button_tool = driver.find_elements_by_xpath('//*[@id="hdtb-tls"]')
    button_date = waitClickElementhUntilExistXpath(driver, button_tool[0], '//*[@id="hdtbMenus"]/div/span[2]')
    button_hour = waitClickElementhUntilExistXpath(driver, button_date[0], '//*[@id="lb"]/div/g-menu/g-menu-item[2]')
    button_hour[0].click()
    cur_url = driver.current_url
    #pdb.set_trace()
    driver.__exit__()
    ############

class GoogleCrawler:
    base_url = 'https://www.google.com/'

    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver')

    def _url2Soup(self, url):
        resp = requests.get(url)
        return bs(resp.text, 'html5lib')

    def _getNextPage(self, soup):
        tag = soup.select('a[aria-label="다음 페이지"]')
        if len(tag) == 1:
            url = self.base_url + tag[0].get('href')
            return self._url2Soup(url)
        return None

    def _getPageResult(self, soup):
        ret = []
        for tag in soup.select('h3'):
            print("tag : {}".format(tag.string))
            tag_parent = tag.parent
            href = tag_parent.get('href')
            #link = self.base_url + str(href)
            link = str(href)
            text = '' # TODO : get text
            ret.append({'title' : tag.string,
                        'link' : link,
                        'text' : text})
        return ret

    def _getPageBySelenium(self, keyword):
        driver = self.driver
        driver.get(self.base_url)
        element = driver.find_element_by_name('q')
        element.send_keys(keyword)
        element.submit()
        driver.implicitly_wait(10)
        button_tool = driver.find_elements_by_xpath('//*[@id="hdtb-tls"]')
        if len(button_tool) == 0:
            print("fail button_tool")
            return
        button_date = waitClickElementhUntilExistXpath(driver, button_tool[0], '//*[@id="hdtbMenus"]/div/span[2]')
        if len(button_date) == 0:
            print("fail button_date")
            return
        button_hour = waitClickElementhUntilExistXpath(driver, button_date[0], '//*[@id="lb"]/div/g-menu/g-menu-item[2]')
        if len(button_hour) == 0:
            print("fail button_hour")
            return
        button_hour[0].click()
        cur_url = driver.current_url
        print("_getPageBySelenium url : {}".format(cur_url))
        #driver.__exit__()
        return bs(driver.page_source, 'html5lib')

    def _getNextPageBySelenium(self):
        driver = self.driver
        button_next = driver.find_elements_by_xpath('//*[@id="pnnext"]')
        if len(button_next) == 0:
            return None
        button_next[0].click()
        driver.implicitly_wait(10)
        return bs(driver.page_source, 'html5lib')

    def search(self, keywords, time='h'): #time : h d w m y
        ret = []
        for keyword in keywords:
            tm.sleep(1)
            #url = self.base_url + 'search?q={}&tbs=qdr:{}'.format(keyword, time)
            #chromeDebug(url)
            #soup = self._url2Soup(url)
            soup = self._getPageBySelenium(keyword)
            while True:
                if soup is None:
                    break
                ret += self._getPageResult(soup)
                tm.sleep(1)
                soup = self._getNextPageBySelenium()
        return ret


if __name__ == "__main__":
    keywords = ['삼성전자', '애플']
    crawler = GoogleCrawler()
    #while(1):
    #    chromeDebug("https://www.google.com/")

    result = crawler.search(keywords)
    print("result : {}".format(result))
    data_frame = pd.DataFrame(result, columns=['title', 'link', 'text'])
    data_frame.to_csv('./' + 'gc' + '.csv')
    data_frame.to_excel('./' + 'gc' + '.xlsx')
    pdb.set_trace()