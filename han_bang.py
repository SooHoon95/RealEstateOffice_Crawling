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
         
        self.base_url = "https://karhanbang.com/office/office_list.asp?topM=09"
        self.state_url = "https://karhanbang.com/office/office_list.asp?topM=09&flag=S&page={}&search=&sel_sido={}&sel_gugun={}&sel_dong={}"
        
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
            "idxValue" : 0,
            "sidoText" : "",
            "gugun" : [],
        }
        
        self.gugun_data = {
            "idxValue" : 0,
            "gugunText" : "",
            "dong" : []
        }
        
        self.dong_data = {
            "idxValue" : 0,
            "dongText" : ""
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
        
    def state_list(self):
        
        driver = webdriver.Chrome("/Users/choesuhun/Desktop/Code/GitHub/crawling/chromedriver")
        driver.get(self.base_url)
        
        # drop down 값 순회하기
        
        # NOTE - 시/도
        sido = Select(driver.find_element_by_id('sido'))
        for sidoValue in tqdm(sido.options):
            self.sido_data = {
                "idxValue" : 0,
                "sidoText" : "",
                "gugun" : [],
            }
        
            sido.select_by_value(sidoValue.get_attribute('value'))
            sidoIdx = sidoValue.get_attribute('value') # value 값 가지고 오기
            sidoText = sidoValue.text
            # print("🔥🔥🔥🔥" + sidoIdx + ":" + sidoText + "🔥🔥🔥🔥")
            
            self.sido_data["idxValue"] = sidoIdx
            self.sido_data["sidoValue"] = sidoText
            time.sleep(1)
            
            # NOTE - 구/군
            
            gugun = Select(driver.find_element_by_id('gugun'))
            for gugunValue in gugun.options:
                
                self.gugun_data = {
                    "idxValue" : 0,
                    "gugunText" : "",
                    "dong" : []
                }
   
                gugun.select_by_value(gugunValue.get_attribute('value'))
                gugunIdx = gugunValue.get_attribute('value') # value 값 가지고 오기
                gugunText = gugunValue.text
                
                # print("✔️✔️✔️" + gugunIdx + ":" + gugunText + "✔️✔️✔️")
                
                self.gugun_data["idxValue"] = gugunIdx
                self.gugun_data["gugunText"] = gugunText
                
                # NOTE - 읍/면/동   
                
                dong = Select(driver.find_element_by_id('dong'))
                for dongValue in dong.options:
                    self.dong_data = {
                        "idxValue" : 0,
                        "dongText" : ""
                    }
                    dong.select_by_value(dongValue.get_attribute('value'))
                    dongIdx = dongValue.get_attribute('value') # value 값 가지고 오기
                    dongText = dongValue.text
                    
                    self.dong_data["idxValue"] = dongIdx
                    self.dong_data["dongText"] = dongText
                    
                    # print("📌📌" + dongIdx + ":" + dongText)
                    self.gugun_data["dong"].append(self.dong_data)
                    self.sido_data["gugun"].append(self.gugun_data)

                    self.data.append(self.sido_data)
            
        driver.close()
        
    def data_list(self):
        page = 1
        
        # NOTE : - data 사용해서 담은 객체 순회하며 url 돌기
        
        for idxSi in tqdm(range(0, len(self.data))):
            
            si = self.data[idxSi]["idxValue"]
            
            for idxGugun in tqdm(range(0, len(self.data[idxSi]["gugun"]))):
                gugun = self.data[idxSi]["gugun"][idxGugun]["idxValue"]
                print(gugun)
                
                for idxDong in tqdm(range(0,len(self.data[idxSi]["gugun"][idxGugun]["dong"]))):
                    dong = self.data[idxSi]["gugun"][idxGugun]["dong"]["idxValue"]
        

    # self.sido_data = {
    #             "idxValue" : "1",
    #             "sidoText" : "서울특별시",
    #             "gugun" : [
        #               { 
        #                   idxValue : "143",
        #                   gugunText: "강남구",
        #                   dong : [
        #                      {
        #                          idxValue : "3918"
        #                          dongText: "개포동"
        #                       }
        #                           ]
        #                   ],
    #         }        


hanBang = Hanbang()
hanBang.state_list()
# for i in range(0, len(hanBang.data)):
#     print(hanBang.data[i]["idxValue"], type(hanBang.data[i]["idxValue"]))
hanBang.data_list()