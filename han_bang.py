import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from openpyxl import Workbook
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import pandas as pd

class Hanbang:
    def __init__(self):
        # 변수 URL
        self.url = "http://karhanbang.com/office/office_list.asp?topM=09&flag=G&page={}&search=&sel_sido={}"
        self.url_gugun = "&sel_gugun={}"
        self.url_dong = "&sel_dong={}"
        
        # base URL
        self.base_url = "http://karhanbang.com/main/"
        
        # Detail URL
        self.image_base_url = (
            "http://karhanbang.com/office/office_detail.asp?topM=09&mem_no={}&sel_sido={}&sel_gugun={}&sel_dong={}&search="
        )
        
        self.data = []
        
        self.headers = {
             "Content_Type": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        
        self.page_num = 0
        
        # data 객체
        self.get_data = {
            "list_region": "",
            "list_name": "",
            "list_owner": "",
            "list_callNum": "",
            "list_owner": "",
            "list_full_adress": "",
        }
         
        # sido셀렉 -> 구군 차례대로 받아와서 셀렉 -> 읍면동 차레대로 받아와서 셀렉 -> 리스트 가져오기
        
        self.count = 0      
        
    def data_list(self):
        page = 1
        print(123123)
        
        # "http://karhanbang.com/office/office_list.asp?topM=09&flag=G&page={}&search=&sel_sido={}&sel_gugun={}&sel_dong={}"
        
        format_url = self.url.format(page, 1)
        
        driver = webdriver.Chrome("/Users/choesuhun/Desktop/Code/GitHub/crawling/chromedriver")
        driver.get(format_url)
        
        sido = Select(driver.find_element_by_id('sido'))
        
        for option1 in sido.options:
            sido.select_by_value(option1.get_attribute('value'))
            time.sleep(1)
            
            print(sido)
            # print(option1.text)
            
        driver.close()
        # time.sleep(3)
        
        # html = driver.page_source
        # print(html)
        
        # time.sleep(2)
        
        # soup = BeautifulSoup(html, "html.parser")
            

hanBang = Hanbang()
hanBang.data_list()