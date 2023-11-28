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
         
        self.url = "https://karhanbang.com/office/office_list.asp?topM=09"
        self.url_state = "&page={}&search=&sel_sido={}sel_gugun={}&sel_dong={}"
        
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
    
        self.sido_data = {
            "value" : "",
            "text" : ""
        }
        
        self.get_data = {
            "region": "",
            "name": "",
            "owner": "",
            "callNum": "",
            "owner": "",
            "full_adress": "",
        }
         
        # sido셀렉 -> 구군 차례대로 받아와서 셀렉 -> 읍면동 차레대로 받아와서 셀렉 -> 리스트 가져오기
        
        self.count = 0      
        
    def data_list(self):
        page = 1
        print(123123)
        
        driver = webdriver.Chrome("/Users/choesuhun/Desktop/Code/GitHub/crawling/chromedriver")
        driver.get(self.url)
        
        # drop down 값 순회하기
        
        ## NOTE - 시/도
        
        sido = Select(driver.find_element_by_id('sido'))
        
        for sidoValue in sido.options:
            
            value = sidoValue.get_attribute('value') # value 값 가지고 오기
            textValue = sidoValue.text
            print("🔥🔥🔥🔥" + value + ":" + textValue + "🔥🔥🔥🔥")
            
            
            self.sido_data["value"] = value
            self.sido_data["text"] = textValue
            self.data.append(self.sido_data)
            time.sleep(1)
            
            self.sido_data = {
            "value" : "",
            "text" : ""
            }

            # NOTE - 구/군
            
            # gugun = Select(driver.find_element_by_id('gugun'))
            # for gugunValue in gugun.options:
                
            #     gugun.select_by_value(gugunValue.get_attribute('value'))    
            #     print("✔️✔️✔️" + gugunValue.text + "✔️✔️✔️")
                
            #     ## NOTE - 읍/면/동   
                
            #     dong = Select(driver.find_element_by_id('dong'))
            #     for dongValue in dong.options:
                    
            #         dong.select_by_value(dongValue.get_attribute('value'))
            #         print(dongValue.text)
                    
            #         # param Url 생성
            #         # format_url = self.url + self.url_state
            #         # format_url = format_url.format(page, sidoValue, gugunValue, dongValue)
                    
            #         driver.close()
                    
            #         time.sleep(1)

                    
                    # 숫자로 가지고올수있는지
                    
                    
            
        driver.close()


hanBang = Hanbang()
hanBang.data_list()