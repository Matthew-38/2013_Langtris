#!/usr/bin/python2.7
# encoding: UTF-8
'''Created on 15 Jul 2013
@author: Matthew
'''
import pygame, sys,random,json,codecs
from pygame.locals import *
pygame.init()
NEVER=0
RARE=5
OCCASIONAL=10
FREQUENT=33
ABUNDANT=100
SCOREMOD=10
MAXWORDLENGTH=12
HEADSTARTSIZE=7
WIDTH=510
HEIGHT=530
GRIDHEIGHT=500
GRIDWIDTH=400
CELLWIDTH=20
CELLHEIGHT=25
XCELLS=int(GRIDWIDTH/CELLWIDTH)-1
YCELLS=int(GRIDHEIGHT/CELLHEIGHT)-1
XCENTREOFFSET=10 #To centre in a cell
YCENTREOFFSET=13 #To centre in a cell
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
TRANSPARENT=(0,0,0,0)
speed=20
DISPLAYSURF= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Langtris')
fpsClock=pygame.time.Clock()
class Game():
    """"""
    def __init__(self):
        #global DISPLAYSURF
        nearWhite=(250,250,250)
        fontObj_score = pygame.font.Font('freesansbold.ttf', 20)
        textSurfaceObj = fontObj_score.render("F1:Help  F2:New Game  F3:QUIT   F5:Save   F6:Load", True, nearWhite)
        DISPLAYSURF.blit(textSurfaceObj, (5,GRIDHEIGHT+7.5))
    def quit(self):
        gridData.printData()
        sys.exit()
    def save(self):
        fout=codecs.open("Save.json",'w',encoding="UTF8")
        json.dump(obj=([words.filename,score.foundWords,gridData.data,words.sortedWordList,score.score]), fp=fout, ensure_ascii=False)
        fout.close()
        print("Game saved!")
    def load(self):
        print("Loading game...")
        score.__init__()
        gridData.__init__()
        grid.__init__()
        words.__init__() #TODO: make it so it will select correct dictionary
        fin=codecs.open("Save.json",encoding="UTF8")
        tmpData=json.load(fp=fin)
        words.__init__(filename=tmpData[0])
        score.foundWords,gridData.data,words.sortedWordList,score.score=tmpData[1:] #FIXME: letters not drawing background!
        grid.updateGridFromData()
        print("Game loaded successfully")
        words.newLetter()
    def help(self):
        pass
    def newGame(self):
        myDict="testdict.txt"
        hsSize=20
        fin=codecs.open("settings.ini",encoding="UTF8")
        for line in fin:
            if 'dictionary' in line: myDict=line.split('=')[1].strip()
            if 'starting letters' in line: hsSize=int(line.split('=')[1].strip())
            global speed
            if 'speed' in line: speed=int(line.split('=')[1].strip())
        score.__init__(score=0, foundWords=list())
        gridData.__init__()
        grid.__init__()
        words.__init__(filename=myDict)
        words.makeHeadstart(headstartSize=hsSize)
        words.newLetter()
    def keyHandler(self,event):
        if event.key==pygame.K_LEFT:
            grid.hMoveInterLetter('left')
        elif event.key==pygame.K_RIGHT:
            grid.hMoveInterLetter('right')
        elif event.key==pygame.K_DOWN:
            grid.dropLetter()
        elif event.key==pygame.K_F1: self.help()
        elif event.key==pygame.K_F2: self.newGame()
        elif event.key==pygame.K_F3: self.quit()
        elif event.key==pygame.K_F5: self.save()
        elif event.key==pygame.K_F6: self.load()
        else: print(event.key, event.scancode,event)
class Score():
    """"""
    score=0
    foundWords=[]
    def __init__(self,score=0, foundWords=[]):
        self.score=score
        self.foundWords=foundWords
        print('should be empty: '+str(foundWords))
        self.drawScore()
    def scoreWords(self,word):
        freq=0
        words=[item[0] for item in self.foundWords]
        if word in words:
            freq=self.foundWords[words.index(word)][1]
            self.foundWords[words.index(word)][1]+=1
        else:
            self.foundWords.append([word,1])
        self.score+=(len(word)*SCOREMOD)/(freq+1)
        self.sortFoundWords()
        self.drawScore()
    def sortFoundWords(self):
        self.foundWords=sorted(self.foundWords,key=lambda freq:freq[1])
    def drawScore(self):
        global DISPLAYSURF
        grey=(50,50,50)
        nearWhite=(250,250,250)
        pygame.draw.rect(DISPLAYSURF, grey,(GRIDWIDTH, 0, 110, GRIDHEIGHT))
        pygame.draw.rect(DISPLAYSURF, nearWhite,(GRIDWIDTH+5, 35, 100, GRIDHEIGHT-40)) # wordlist
        pygame.draw.rect(DISPLAYSURF, nearWhite,(GRIDWIDTH+10, 5, 90, 25))#score
        fontObj_score = pygame.font.Font('freesansbold.ttf', 25)
        textSurfaceObj = fontObj_score.render(str(int(self.score))+ " pts.", True, grey)
        DISPLAYSURF.blit(textSurfaceObj, (GRIDWIDTH+15,7.5))
        items=0
        for word,freq in self.foundWords:
            if items>20: break #Stop the list being overfilled
            items+=1
            fontObj_word=pygame.font.Font('freesansbold.ttf', 14)
            textSurfaceObj = fontObj_score.render(str(word+' : '+str(freq)), True, grey)
            DISPLAYSURF.blit(textSurfaceObj, (GRIDWIDTH+10,15+21*items))
class Words():
    """"""
    allchar=''
    dictionary={}
    sortedWordList=[[[]],[[]],[[]]]
    filename=''
    def __init__(self, filename="testdict.txt", seperator='-'):
        self.filename=filename
        self.allchar=''
        self.dictionary={}
        self.sortedWordList=[[[]],[[]],[[]]]
        fin=codecs.open(filename, encoding="UTF-8")
        for line in fin:
            line=line.strip()
            if len(line)>=3 and not '#' in line:
                line=line.split(' ')
                word=''
                if len(line[0])>=3: word=line[0]
                elif len(line)>1: word=line[1] #Some dictionaries have a space at the beginning of the line
                if(len(word)>1):#make sure it is not a dummy line 
                    word=word.strip()
                    word=word.lower() #normalize to lower case
                    if len(word)>=3: #just to be sure it wasn't all stripped away!
                        self.allchar+=word
                        self.dictionary[word]=line
        self.sortDict()
    def testValidDict(self, hsSize):
        if hsSize>=len(self.allchar):
            print("Critical Error: Dictionary too small or not valid")
            game.quit()
    def sortDict(self):
        """Sets it up only for Freq 0"""
        for word in self.dictionary.keys():
            if len(word)>=3 and len(word)<=MAXWORDLENGTH:
                while len(word)>len(self.sortedWordList)-1:
                    self.sortedWordList.append([[]])
                self.sortedWordList[len(word)][0].append(word) #0 refers to fact it was never found
        print(self.sortedWordList)
    def makeHeadstart(self,headstartSize=HEADSTARTSIZE):
        self.testValidDict(headstartSize)
        for i in range(headstartSize): #@UnusedVariable
            letter=self.allchar[random.randint(0,len(self.allchar))-1]
            x=random.randint(0,len(gridData.data)-1) #select position
            if gridData.data[x][0]!="":
                print("End of Game") # Do more from here later
            else:
                gridData.data[x][0]=letter
            gridData.fallLetters()
    def newLetter(self):
        letter=self.allchar[random.randint(0,len(self.allchar))-1]
        x=random.randint(0,len(gridData.data)-1)
        if gridData.data[x][0]!="":
            print("End of Game") # Do more from here later
        else:
            grid.setInterLetter(letter,x)
    def search4Words(self):
        foundwords={}
        foundhwords={}
        for x in range(len(gridData.data)): #looking for vertical words
            letters=''
            wordfound=False
            for y in range(len(gridData.data[0])-2): #2 letter words are ignored, so don't bother searching
                if gridData.data[x][y]!='':
                    letters=''.join(gridData.data[x][y:])
                    break
            for length in range(min(len(letters),len(self.sortedWordList)-1),2,-1):
                for freq in range(len(self.sortedWordList[length])):
                    for word in self.sortedWordList[length][freq]:
                        if word in letters: #Note: don't need to search for additional words, as only one letter could have been added, anyway, it will be found in next second
                            foundwords[x]=[word, letters.index(word)+y, letters.index(word)+y+len(word)]
                            wordfound=True
                            break
                    if wordfound: break
                if wordfound: break
        for y in range(len(gridData.data[0])): #looking for horizontal words
            letters=''
            letterSets=[]
            wordfound2=False
            x=0
            while(x<len(gridData.data)-2):
                if gridData.data[x][y]!='':
                    letters=gridData.data[x][y]
                    for i in range(x+1, len(gridData.data),1):
                        if gridData.data[i][y]!='':
                            letters+=gridData.data[i][y]
                        else:
                            if len(letters)>=3: 
                                letterSets.append([letters,x])
                            letters=''
                            break
                    if len(letters)>=3: letterSets.append([letters,x]) #final letters, if present
                    x=i-1 #skip on to next space
                x+=1
            for letters,x in letterSets:
                for length in range(min(len(letters),len(self.sortedWordList)-1),2,-1):
                    for freq in range(len(self.sortedWordList[length])):
                        for word in self.sortedWordList[length][freq]:
                            if word in letters:
                                foundhwords[y]=[word, letters.index(word)+x, letters.index(word)+x+len(word)]
                                wordfound2=True
                                break
                    if wordfound2: break
        print(foundwords,foundhwords)
        """For now I am going to simplify things and say that all words are taken; I can always come back to this later"""
        for x in foundwords.keys():
            score.scoreWords(foundwords[x][0])
            for y in range(foundwords[x][1], foundwords[x][2]):
                gridData.data[x][y]='' #remove letters
        for y in foundhwords.keys():
            score.scoreWords(foundhwords[y][0])
            for x in range(foundhwords[y][1], foundhwords[y][2]):
                gridData.data[x][y]=''
        return max(len(foundwords),len(foundhwords))!=0
class GridData():
    """"""
    data=[]
    def __init__(self):
        self.data=[]
        for i in range(XCELLS+1):
            self.data.append([])
            for j in range(YCELLS+1):
                self.data[i].append('')
    def printData(self):
        for line in self.data:
            line2=[]
            for item in line:
                if item=='' or item==' ':
                    line2.append("_")
                else:
                    line2.append(item)
            print(" ".join(line2))
    def checkPosFree(self, xcell,ycell):
        """Returns true if really free - i.e. equal to ''"""
        return self.data[xcell][ycell]==''
    def instateLetterAtPos(self,letter,xcell,ycell):
        self.data[xcell][ycell]=letter
        self.search4Words()
    def search4Words(self):
        if(words.search4Words()): self.fallLetters()
    def fallLetters(self):
        for x in range(len(self.data)):
            repeat=True
            while repeat==True:
                repeat=False
                spacebelow=False
                for y in range(len(self.data[x])-1,-1,-1): #counting backward
                    if self.data[x][y]=='':
                        spacebelow=True
                    elif spacebelow==True:
                        self.data[x][y+1]=self.data[x][y] #copy letter down
                        self.data[x][y]='' #clear current space
                        repeat=True
        grid.updateGridFromData()
class Grid():
    """Initialises a grid based on the input, and allows interaction with it"""
    backCol=(200,200,200)
    lineCol=(0,55,9)
    interLetter=['',0,0,'',0]
    defaultFallRate=7 #i.e. 7 turns before it falls - really slow! 1=fastest
    currentFallRate=defaultFallRate #is sped up during drop
    timeTilNextFall=currentFallRate
    defaultMovesPerTick=3
    movesLeftInThisTick=3
    letters=[]
    def __init__(self):
        self.drawgrid()
    def drawgrid(self,x=0,y=0):
        global DISPLAYSURF
        pygame.draw.rect(DISPLAYSURF, self.backCol, (x, y, GRIDWIDTH,GRIDHEIGHT))
        for i in range(0,GRIDWIDTH,CELLWIDTH):
            pygame.draw.line(DISPLAYSURF, self.lineCol, (i,y), (i,GRIDHEIGHT),1)
        for j in range(0,GRIDHEIGHT,CELLHEIGHT):
            pygame.draw.line(DISPLAYSURF, self.lineCol, (x,j), (GRIDWIDTH,j),1)
    def drawLetter(self,letter, xcell,ycell,col=(255,255,255)):
        fontObj = pygame.font.Font('freesansbold.ttf', 22)
        textSurfaceObj = fontObj.render(letter, True, col)
        DISPLAYSURF.fill(BLUE,textSurfaceObj.get_rect(width=CELLWIDTH-1, height=CELLHEIGHT-1, center=self.coord2cell(xcell,ycell)))
        textRectObj = textSurfaceObj.get_rect(center=self.coord2cell(xcell,ycell))
        return [textSurfaceObj,textRectObj]
    def drawStaticLetter(self,letter,xcell,ycell):
        self.letters.append(self.drawLetter(letter,xcell,ycell,GREEN))
    def drawInterLetter(self):
        if self.interLetter[0]!='':
            self.interLetter[3],self.interLetter[4]=self.drawLetter(self.interLetter[0],self.interLetter[1],self.interLetter[2],WHITE)
    def coord2cell(self,xcell,ycell):
        x=(xcell*CELLWIDTH)+XCENTREOFFSET
        y=(ycell*CELLHEIGHT)+YCENTREOFFSET
        return x,y
    def moveInterLetter(self,xcell,ycell,absol=False):
        if absol:
            self.interLetter[1]=xcell
            self.interLetter[2]=ycell
        else:
            self.interLetter[1]+=xcell
            self.interLetter[2]+=ycell
        self.drawInterLetter()
    def hMoveInterLetter(self,sense):
        if(sense=='left' and self.interLetter[1]>0 and gridData.checkPosFree(self.interLetter[1]-1, self.interLetter[2])):
            if self.movesLeftInThisTick>0: 
                DISPLAYSURF.fill(self.backCol,self.interLetter[3].get_rect(width=19, height=24, center=self.coord2cell(self.interLetter[1],self.interLetter[2])))#self.interLetter[4])
                self.moveInterLetter(-1,0)
        if (sense=='right' and self.interLetter[1]<XCELLS and gridData.checkPosFree(self.interLetter[1]+1, self.interLetter[2])):
            if self.movesLeftInThisTick>0: 
                DISPLAYSURF.fill(self.backCol,self.interLetter[3].get_rect(width=19, height=24, center=self.coord2cell(self.interLetter[1],self.interLetter[2])))#self.interLetter[4])
                self.moveInterLetter(1,0)
        self.movesLeftInThisTick-=1
    def setInterLetter(self,letter,xcell):
        self.interLetter=[letter,xcell,0,0,0]
        self.drawInterLetter()
    def resetInterLetter(self):
        self.interLetter=['',0,0,'','']
    def staticifyLetter(self):
        letter,x,y=self.interLetter[0],self.interLetter[1],self.interLetter[2]
        self.resetInterLetter()
        self.drawStaticLetter(letter,x,y)
        gridData.instateLetterAtPos(letter,x,y)
        self.currentFallRate=self.defaultFallRate
        words.newLetter()
    def letterFall(self):
        if self.timeTilNextFall>0: self.timeTilNextFall-=1
        else:
            self.timeTilNextFall=self.currentFallRate
            self.movesLeftInThisTick=self.defaultMovesPerTick  
            if(self.interLetter[2]<YCELLS and gridData.checkPosFree(self.interLetter[1], self.interLetter[2]+1)):
                if self.interLetter[4]!='': DISPLAYSURF.fill(self.backCol,self.interLetter[3].get_rect(width=19, height=24, center=self.coord2cell(self.interLetter[1],self.interLetter[2]))) #need if, otherwise it will try at the beginning
                self.moveInterLetter(0, 1)
            else: self.staticifyLetter()
    def dropLetter(self):
        self.currentFallRate-=3
    def updateGridFromData(self):
        self.letters=[]
        self.drawgrid()
        for x in range(len(gridData.data)):
            for y in range(len(gridData.data[x])):
                letter=gridData.data[x][y]
                if letter!='': self.drawStaticLetter(letter, x, y)

if __name__ == '__main__':
    game=Game()
    words=Words()
    gridData=GridData()
    grid=Grid()
    score=Score()
    words.makeHeadstart()
    words.newLetter()

while True:
    # main game loop
    for surf,rect in grid.letters:
        DISPLAYSURF.blit(surf,rect)
    if(grid.interLetter[4]!=0 and grid.interLetter[4]!=''):
        DISPLAYSURF.blit(grid.interLetter[3], grid.interLetter[4])
    for event in pygame.event.get():    
        if event.type == 12: game.quit()#=QUIT
        elif event.type==2: game.keyHandler(event) #2=keydown
    pygame.display.update()
    fpsClock.tick(speed)
    grid.letterFall()
