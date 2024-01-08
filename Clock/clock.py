try:
    from Tkinter import *
except:
    from tkinter import *
from math import cos
from math import sin
from math import pi
from math import fabs
import time

def readTimeZone(): # Read time info from text file
    f = open("TimeZone.txt","r")
    fileContents = f.readlines()
    allTimeZone = [] # [timeZone0 , timeZone1 , timeZone2 , ...]
    timeZone = [] # [location , DSTstr , UTCstr]
    for line in fileContents:
        if line == "\n":
            allTimeZone.append(timeZone)
            timeZone = []
        else:
            line = line.replace("\n","")
            timeZone.append(line)
    return allTimeZone #return a 2D list containing info about time as string

def processDSTAndUTC(timeInfoStr): # change DSTstr into DSTHr, DSTMin and UTCstr into UTCHr, UTCMin
    timeInfo =[]
    for locationIndex in range(len(timeInfoStr)):
        
        locTimeInfo =[]
        locTimeInfo.append(timeInfoStr[locationIndex][0]) # append location name

        dstDiff = timeInfoStr[locationIndex][1].split(" ") # find DST val
        for timeIndex in range (len(dstDiff)):
            locTimeInfo.append(int(dstDiff[timeIndex]))
        
        utcDiff = timeInfoStr[locationIndex][2].split(" ") # find UTC val
        for timeIndex in range (len(utcDiff)):
            locTimeInfo.append(int(utcDiff[timeIndex]))

        
        timeInfo.append(locTimeInfo)
    return timeInfo # return time info as [location,DSTHr,DSTMinm,UTCHr,UTCMin]

class Clock:
    def __init__(self,timeInfo,xStart,yStart):
        self.timeInfo = timeInfo
        self.xStart = xStart
        self.yStart = yStart
        self.CLOCKRAD = 100
        self.xClockCen = self.xStart + self.CLOCKRAD
        self.yClockCen = self.yStart + self.CLOCKRAD

    def drawClock(self):
        canvas.create_oval(self.xStart,self.yStart,self.xStart+2*(self.CLOCKRAD),self.yStart+2*(self.CLOCKRAD),outline="black",fill="black",width=5)
        for pos in range(1,61):
            self.angle = (pi/30) * pos
            if pos % 5 ==0:
                self.startXCo = self.xClockCen + 7*(self.CLOCKRAD/10) * cos(self.angle)
                self.startYCo = self.yClockCen + 7*(self.CLOCKRAD/10) * sin(self.angle)
            else:
                self.startXCo = self.xClockCen + 8*(self.CLOCKRAD/10) * cos(self.angle)
                self.startYCo = self.yClockCen + 8*(self.CLOCKRAD/10) * sin(self.angle)
            self.endXCo = self.xClockCen + (self.CLOCKRAD * cos(self.angle))
            self.endYCo = self.yClockCen + (self.CLOCKRAD * sin(self.angle))
            canvas.create_line(self.startXCo,self.startYCo,self.endXCo,self.endYCo,width=3,fill="white")

    def getTime(self): # read UTC time (NOT local)
        self.curTime = time.strftime("%H %M %S",time.gmtime()).split(" ") #curTime = ["Hr","Min","Sec"]
        self.curSecTime = int(self.curTime[2])
        self.curMinTime = int(self.curTime[1])
        self.curHrTime = int(self.curTime[0])

    def drawSecHand(self):
        self.startXCo = self.xClockCen
        self.startYCo = self.yClockCen
        self.angle = ((pi/30)*self.curSecTime)-pi/2 #calculate the angle of the sec hand
        self.endXCo = self.xClockCen + 7*(self.CLOCKRAD/10) * cos(self.angle) # length of hand = 7/10 of clock rad
        self.endYCo = self.yClockCen + 7*(self.CLOCKRAD/10) * sin(self.angle)
        canvas.create_line(self.startXCo,self.startYCo,self.endXCo,self.endYCo,width=3,fill="red")

    def drawMinHand(self):
        self.startXCo = self.xClockCen
        self.startYCo = self.yClockCen
        self.angle = ((pi/30)*(self.curMinTime+self.timeInfo[2]+self.timeInfo[4]))-pi/2 # curMin + DSTMin+ UTCMin 
        self.endXCo = self.xClockCen + 6*(self.CLOCKRAD/10) * cos(self.angle) # length of hand = 6/10 of clock rad
        self.endYCo = self.yClockCen + 6*(self.CLOCKRAD/10) * sin(self.angle)
        canvas.create_line(self.startXCo,self.startYCo,self.endXCo,self.endYCo,width=4,fill="white")
    
    def drawHrHand(self):
        self.startXCo = self.xClockCen
        self.startYCo = self.yClockCen
        self.angle = (((pi/6)*(self.curHrTime+self.timeInfo[1]+self.timeInfo[3]))-pi/2) #CurHr + DSTHr + UTCHr
        self.angle = self.angle + ((pi/360) * (self.curMinTime+self.timeInfo[2]+self.timeInfo[4])) # +CurMin +DSTMin+UTCMin
        self.endXCo = self.xClockCen + (5*(self.CLOCKRAD/10) * cos(self.angle)) # length of hand = 5/10 of clock rad
        self.endYCo = self.yClockCen + (5*(self.CLOCKRAD/10) * sin(self.angle))
        canvas.create_line(self.startXCo,self.startYCo,self.endXCo,self.endYCo,width=4,fill="white")

    def showLocation(self): # add label to the bottom of the clock to show location
        self.location = self.timeInfo[0] #location name
        self.text = Label(root,text = self.location,bg ="white")
        self.text.place(x=self.xStart+75,y=self.yStart+220) # position of the label

    def showTime(self): # add label to the bottom of the clock to show numeric time
        self.curTimeStr =str(self.curHrTime+self.timeInfo[1]+self.timeInfo[3])+":"+str(self.curMinTime+self.timeInfo[2]+self.timeInfo[4])+":"+str(self.curSecTime)
        self.text = Label(root,text = self.curTimeStr,bg ="white")
        self.text.place(x=self.xStart+75,y=self.yStart+250) # position of the label
        

#End of Class
    

def runClock(): # procedure to display the clock
    while True:
        locationIndex=0
        for myClock in clockLocLst: # iterate for number of location
            myClock = Clock(timeInfo[locationIndex],10+(locationIndex * 250),10)
            myClock.drawClock()
            myClock.getTime()
            myClock.drawSecHand()
            myClock.drawMinHand()
            myClock.drawHrHand()
            myClock.showLocation()
            myClock.showTime()
            time.sleep(0.5) 
            locationIndex += 1
        root.update()
    root.mainloop()
        

if __name__ == "__main__":   
    timeInfoStr = readTimeZone() # read the text file
    timeInfo = processDSTAndUTC(timeInfoStr) # process dst and utc time
    clockLocLst =[] #[location1,location2,location3]
    for locIndex in range(len(timeInfo)):
        clockLocLst.append(timeInfo[locIndex][0])

    root = Tk()  # set up tkinter
    canvas = Canvas(root, width = 1000, height = 300, bg = "white")    
    canvas.pack()
    runClock() #start displaying the clock

 