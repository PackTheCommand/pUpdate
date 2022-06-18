import time
import sys
from termcolor import colored, cprint
class LodingBar:
    def __init__(self):
        self.procet=0
        self.end=False
        self.last_Bar=""
    def add(self,procendToAdd,AditionalInfo=""):
        if(self.procet+procendToAdd>100):
            self.procet=100
        else:
            self.procet+=procendToAdd
        a=False
        count=0
        t=0
        ret_bar_2=""
        ret_bar_1="▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
        for c in range(0,100):
            if(count<=self.procet)&(a):
                t+=1
                ret_bar_1=ret_bar_1.replace("▒","",1)
                ret_bar_2+="█"
            if(a):
                a=False
            else:
                a=True
            count+=1
        
        BarPart_1 = ret_bar_1
        BarPart_2 = ret_bar_2
        final_Bar="║"+ret_bar_2+ret_bar_1+"║ "+str(self.procet)+"%"
        self.last_Bar=final_Bar
        return "║"+BarPart_2+BarPart_1+"║ "+str(self.procet)+"%"+" "+AditionalInfo
    def error(self,ErrorMessage):

        return self.last_Bar,"red"
    def getLoad(self):
        return self.procet
    def pause(self):
        return self.last_Bar
        
    


