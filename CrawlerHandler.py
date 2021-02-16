from GoogleCrawler import GoogleCrawler
from DataBase import DataBase
from KakaoTalk import KakaoTalk

import logging
import pandas as pd
import time
import pdb

class CrawlerHandler():
    def __init__(self):
        self.crawler = GoogleCrawler()
        self.db = DataBase()
        self.kakao = KakaoTalk()

        self.db_table_name = 'googlecrawler'
        self.keywords = []

    def addKeywords(self, keywords):
        self.keywords += list(keywords)

    def filterTitle(self, title=""):
        for keyword in self.keywords:
            if title.find(keyword) >= 0:
                return 0
        return -1

    def process(self, result, head_tag=""):
        for data in result:
            # 제목 필터
            if self.filterTitle(data['title']) == -1:
                print("Data skip({})".format(data['title']))
                continue
            # DB에서 중복검사
            stored_data = self.db.db_select(self.db_table_name, 'title', data['title'])
            if len(stored_data) != 0:
                # print('Data({}) is already exist'.format(data['title']))
                continue
            # # DB에 데이터 넣고 kakao메세지 전송
            print('Data insert({})'.format(data['title']))
            self.db.db_insert(self.db_table_name, data)
            self.kakao.sendToMeMessage("<{}> {} \n {} \n\n [Text] \n\n {}".format(head_tag, *data.values()))

    def run(self):
        logging.basicConfig(filename='run.log', \
                            level=logging.INFO, \
                            format='[%(asctime)s][%(levelname)s] %(message)s', \
                            datefmt='%Y-%m-%d %H:%M:%S')
        while(True):
            for keyword in self.keywords:
                try:
                    print("=================== {} ===================".format(keyword))
                    result = self.crawler.search([keyword], time='h')
                    print("result : {}".format(result))
                    if len(result) == 0:
                        print("reset webBrowser..")
                        del self.crawler
                        self.crawler = GoogleCrawler()
                    self.process(result, head_tag=keyword)
                except Exception as e:
                    logging.error(f"Error : {e}")
                    print('Error wait 60 sec...')
                    time.sleep(60)

            print('wait 120 sec...')
            time.sleep(120)


if __name__ == "__main__":
    crawler_handler = CrawlerHandler()
    '''
    crawler_handler.addKeywords(['삼성전자', '애플', '삼성SDI', '키움증권', '초록뱀',\
                                 '두산퓨얼셀', '삼성제약', '셀리버리', '태경케미컬', 'LG전자',\
                                 '현대차', '기아차', '대한항공', '빅히트', '우리바이오',\
                                 '제주반도체', 'NAVER', '인터파크', '디피씨', '태경케미컬',\
                                 '오리엔탈정공', '네온테크', '카카오', '현대비앤지스틸', '신라에스지',\
                                 '인콘', '선진뷰티사', '금호에이치티', '삼양홀딩스',\
                                 '알로이스', '삼원강재', '아이에이', '디피씨', '대성엘텍',\
                                 '원익큐브', '씨아이에스', 'SFA반도체', 'HMM', '셀트리온',\
                                 'YG플러스'])
    '''
    crawler_handler.addKeywords(['삼성전자', '기아차', '피비파마', '바이넥스', '이수앱지스',
                                 '현대바이오', 'HMM', '위지트', '이아이디', '우리기술투자',
                                 '이트론', '동방', '솔루엠', '대덕전자', '와이더플래닛',
                                 'LG전자', '엠에스오토텍', '셀트리온', 'AP위성'])
    #crawler_handler.addKeywords(['삼성SDI'])
    crawler_handler.run()