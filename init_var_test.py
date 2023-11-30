class InitTest:
    def __init__(self):
        self.init_int = 0
        
        self.sido_data = {
            "idxValue" : 0,
            "sidoText" : "",
        }
        
        self.data = []
    
    def testDef(self):
        
        for idx in range(0, 10):
            print("idx : " , idx , "🔥🔥🔥🔥🔥")
            
            self.sido_data = {
            "idxValue" : 0,
            "sidoText" : "",
        }
            
            self.sido_data["idxValue"] =  self.sido_data["idxValue"] + idx
            self.sido_data["sidoText"] = self.sido_data["sidoText"] + "plus   "
            
            self.data.append(self.sido_data)
            
            print(self.data)
            

test = InitTest()
test.testDef()