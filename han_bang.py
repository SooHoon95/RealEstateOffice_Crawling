import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from openpyxl import Workbook
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from copy import deepcopy

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
        
        self.office_list = {
            "region": "",
            "name": "",
            "owner": "",
            "phone": "",
            "address": "",
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
            self.sido_data["sidoText"] = sidoText
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
                    
                    self.gugun_data["dong"].append(deepcopy(self.dong_data))
                self.sido_data["gugun"].append(deepcopy(self.gugun_data))

                    
                    # self.gugun_data["dong"].append(self.dong_data)
                    # self.sido_data["gugun"].append(self.gugun_data)

            self.data.append(self.sido_data)
                    
        driver.close()
        
    def data_list(self):
        
        # NOTE : - data 사용해서 담은 객체 순회하며 url 돌기
        for idxSi in tqdm(range(0, len(self.data))):
            
            si = self.data[idxSi]["idxValue"]
            siText = self.data[idxSi]["sidoText"]
            print(si, siText)
            # TODO: - 엑셀파일 생성 "시" 별로
            for idxGugun in tqdm(range(0, len(self.data[idxSi]["gugun"]))):
                gugun = self.data[idxSi]["gugun"][idxGugun]["idxValue"]
                gugunText = self.data[idxSi]["gugun"][idxGugun]["gugunText"]
                
                if "시/군/구" in gugunText:
                    print("pass 시군구")
                    continue
                
                print(gugun, gugunText)
                # TODO: - 시트 생성 "구/군" 별로
                
                for idxDong in tqdm(range(0,len(self.data[idxSi]["gugun"][idxGugun]["dong"]))):
                    page = 1
                    dong = self.data[idxSi]["gugun"][idxGugun]["dong"][idxDong]["idxValue"]
                    dongText = self.data[idxSi]["gugun"][idxGugun]["dong"][idxDong]["dongText"]
                    
                    if "읍/면/동" in dongText:
                        print("pass 읍면동")
                        continue
                    
                    print("🔥🔥🔥🔥🔥", si, gugun, dong, "🔥🔥🔥🔥🔥")
                    
                    # 리스트 담을 변수 선언
                    office_data_list = [] 
                    
                    # NOTE - Page 순회
                    is_last_bool = False
                    
                    while is_last_bool == False:
                        
                        # driver 사용
                        driver = webdriver.Chrome("/Users/choesuhun/Desktop/Code/GitHub/crawling/chromedriver")
                        format_url = self.state_url.format(page, si, gugun, dong)
                        driver.get(format_url)
                        time.sleep(2)
                        
                        # 리스트 가져오기
                        rows = driver.find_elements(By.XPATH, "//tr[contains(@class, 'even') or contains(@class, 'odd')]")
                        for row in rows:
                            region = row.find_element(By.XPATH, ".//td[1]").text # 동 정보
                            name = row.find_element(By.XPATH, ".//td[2]").text 
                            owner = row.find_element(By.XPATH, ".//td[3]").text 
                            phone = row.find_element(By.XPATH, ".//td[4]").text
                            address = row.find_element(By.XPATH, ".//td[5]").text  # 주소
                            
                            self.office_list["region"] = region
                            self.office_list["name"] = name
                            self.office_list["owner"] = owner
                            self.office_list["phone"] = phone
                            self.office_list["address"] = address
                            
                            office_data_list.append(self.office_list)
                            
                            self.office_list = {
                                "region": "",
                                "name": "",
                                "owner": "",
                                "phone": "",
                                "address": "",
                            }
                            
                            # 마지막 페이지인지 검사
                            if self.is_last_check(driver) == True:
                                is_last_bool = True
                            else:
                                page += 1

                                                        
                        driver.close()  # 현재 드라이버 세션 종료
                
    def is_last_check(self, driver) -> bool:
        try:
            # '>' 버튼이 존재하는지 확인
            next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'gradient next')]")
            return False
        except NoSuchElementException as nse:
            # '다음 페이지' 버튼이 없으면 루프 종료
            print("No Such Element Exception : ", nse)
            print("마지막 페이지")
            return True
            
    
    def make_exel(self, office_data_list):
        try:
            df = pd.json_normalize(
                office_data_list,
                
            )
        except Exception as e:
            print(e)
            pass
        

hanBang = Hanbang()
hanBang.state_list()
hanBang.data_list()