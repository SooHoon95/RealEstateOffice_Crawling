import pandas as pd
import os
class InitTest:
    
    # def contain_check(self):
        
    #     strA = "시 /군 /구     "
    #     strB = "시 /군 /구"
        
    #     if strB in strA :
    #         print("yes")
    #     else:
    #         print("No")
    
    def make_exel(self):
        data_list = []
        
        for i in range(0, 10) :
            
            office_list = {
                "region": i,
                "name": i + 1,
                "owner": i + 2,
                "phone": i + 3,
                "address": i + 4,
            }
            data_list.append(office_list)
            
        try:
            df = pd.json_normalize(
                data_list)
            if not os.path.exists('sheetTest.xlsx'):
                with pd.ExcelWriter('sheetTest.xlsx', mode='w', engine='openpyxl') as writer:
                    print('not path')
                    df.to_excel(writer, index=False)
            else:
                with pd.ExcelWriter('sheetTest.xlsx', mode='a', engine='openpyxl') as writer:
                    print("here")
                    name = "{}번"
                    df.to_excel(writer, index=False, sheet_name=name.format(i))    
                    # df.to_excel("sheetTest.xlsx", sheet_name='시트1')
            # df.to_excel("sheetTest.xlsx", sheet_name='시트1')
            # df.to_excel("sheetTest.xlsx", sheet_name='시트 ')
        except Exception as e:
            print(e)
            pass
        
    # def __init__(self):
    #     self.init_int = 0
        
    #     self.sido_data = {
    #         "idxValue" : 0,
    #         "sidoText" : "",
    #     }
        
    #     self.data = []
    
    # def testDef(self):
        
    #     for idx in range(0, 10):
    #         print("idx : " , idx , "🔥🔥🔥🔥🔥")
            
    #         self.sido_data = {
    #         "idxValue" : 0,
    #         "sidoText" : "",
    #     }
            
    #         self.sido_data["idxValue"] =  self.sido_data["idxValue"] + idx
    #         self.sido_data["sidoText"] = self.sido_data["sidoText"] + "plus   "
            
    #         self.data.append(self.sido_data)
            
    #         print(self.data)
            

test = InitTest()
# test.testDef()
test.make_exel()
# test.contain_check()