import os, random, time
path=os.getcwd()

class Block:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.img = loadImage(path+"/images/block.png")
        self.dim = 20                                                    #dimension of a block is 20 x 20
        
    def display(self):
        image(self.img,self.x,self.y)
            
class Pellet:
    def __init__(self,x,y): 
        self.x=x
        self.y=y
        self.img = loadImage(path+"/images/pellet.png")
        
    
    def display(self):
        image(self.img,self.x+8,self.y+8,5,5)
        

class Watermelon:                                                        #special pellets that cause sprites to be ghosts
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.status= False                                               #False to show sprites, True to show ghosts
        self.img = loadImage(path+"/images/watermelon.png")
        
    def eaten(self):
        if self.x == g.pacman.x and self.y == g.pacman.y:
            self.status = True 
        
    def display(self):
        image(self.img,self.x,self.y,20,20)


class Board:
    def __init__(self):
        self.blocks = []
        self.pellet = []
        self.watermelon = []
        inputFile = open(path+"/PacMan-board.csv","r")
        row = 0
        for line in inputFile:
            line = line.strip().split(",")
            
            col = 0
            for i in line:
                if i == '#':
                    self.blocks.append(Block(col*20,row*20))
                elif i == '.':
                    self.pellet.append(Pellet(col*20,row*20))
                elif i == '*':
                    self.watermelon.append(Watermelon(col*20,row*20))
                col+=1
            row+=1
        
    def display(self):
        for block in self.blocks:
            block.display()
        for pellet in self.pellet:
            pellet.display()
        for watermelon in self.watermelon:
            watermelon.display()
            
    def getBoard(self,x,y): 
        for b in blocks:
            col = self.x//self.dim
            row = self.y//self.dim 
            return col, row

class Creature:
    def __init__(self,x,y,v=1):
        self.x=x
        self.y=y
        self.v=v
        self.dir = "RIGHT"  
        
    def teleport(self):
        if self.x == -20 and self.y == 260 and self.dir == 'LEFT':
            self.x = 520
        if self.x == 540 and self.y == 260 and self.dir == 'RIGHT':
            self.x = 0
        
        
class Ghosts(Creature):
    def __init__(self,x,y,img):
        Creature.__init__(self,x,y)
        self.img=img
        self.vx=20
        self.vy=0
        self.dim = 20 
        self.sprite=0
        self.status=True                                                               # if Watermelon returns True, sprites = False  
        self.ghostright1 = loadImage(path+'/images/'+self.img+'ghostright1.png')
        self.ghostright2 = loadImage(path+'/images/'+self.img+'ghostright2.png')
        self.ghostleft1 = loadImage(path+'/images/'+self.img+'ghostleft1.png')
        self.ghostleft2 = loadImage(path+'/images/'+self.img+'ghostleft2.png')
        self.ghostup1 = loadImage(path+'/images/'+self.img+'ghostup1.png')
        self.ghostup2 = loadImage(path+'/images/'+self.img+'ghostup2.png')
        self.ghostdown1 = loadImage(path+'/images/'+self.img+'ghostdown1.png')
        self.ghostdown2 = loadImage(path+'/images/'+self.img+'ghostdown2.png')
        self.imgs = [self.ghostright1,self.ghostright2]
        self.dead = loadImage(path+'/images/flash1.png')
        
        # if Watermelon returns True, sprites = False 
        
    def update(self):
        leftSafe = self.checkLEFTTile()
        rightSafe = self.checkRIGHTTile()
        upSafe = self.checkUPTile()
        downSafe = self.checkDOWNTile()

        change = random.randint(1,2)
        
        if change == 1:
            self.dirChange(leftSafe, rightSafe, upSafe, downSafe)
        
        if self.dir == 'RIGHT' and rightSafe == True:
            self.vx = 20
            self.vy = 0
            
        elif self.dir == 'LEFT' and leftSafe == True:
            self.vx = -20
            self.vy = 0
            
        elif self.dir == 'UP' and upSafe == True:
            self.vx = 0
            self.vy = -20
            
        elif self.dir == 'DOWN' and downSafe == True:
            self.vx = 0
            self.vy = 20
        else:
            self.dirChange(leftSafe, rightSafe, upSafe, downSafe)
            self.vx = 0
            self.vy = 0    
        
        self.x += self.vx
        self.y += self.vy

        
    def dirChange(self, leftSafe, rightSafe, upSafe, downSafe):
        choice = random.randint(1,2)

        if self.dir == 'RIGHT' or self.dir == 'LEFT':
            if choice == 1:
                if downSafe == True:
                    self.dir = 'DOWN'
                    self.imgs = [self.ghostdown1, self.ghostdown2]
                elif upSafe == True:
                    self.dir = 'UP'
                    self.imgs = [self.ghostup1, self.ghostup2]
            else:
                if upSafe == True:
                    self.dir = 'UP'
                    self.imgs = [self.ghostup1, self.ghostup2]
                elif downSafe == True:
                    self.dir = 'DOWN'
                    self.imgs = [self.ghostdown1, self.ghostdown2]
                    
        elif self.dir == 'UP' or self.dir == 'DOWN':
            if choice == 1:
                if rightSafe == True:
                    self.dir = 'RIGHT'
                    self.imgs = [self.ghostright1, self.ghostright2]
                elif leftSafe == True:
                    self.dir = 'LEFT'
                    self.imgs = [self.ghostleft1, self.ghostleft2]
            else:
                if leftSafe == True:
                    self.dir = 'LEFT'
                    self.imgs = [self.ghostleft1, self.ghostleft2]
                elif rightSafe == True:
                    self.dir = 'RIGHT'
                    self.imgs = [self.ghostright1, self.ghostright2]
                    

    def checkLEFTTile(self):
        
        for b in g.board.blocks:
            if self.y == b.y and self.x-20 == b.x:
                return False
        return True
            
    def checkRIGHTTile(self):

        for b in g.board.blocks:
            if self.y == b.y and self.x+20 == b.x:
                return False
        return True        
    
    def checkUPTile(self):
        for b in g.board.blocks:
            if self.x == b.x and self.y-20 == b.y:
                return False
        return True   
    
    def checkDOWNTile(self):
        for b in g.board.blocks:
            if self.x == b.x and self.y+20 == b.y:
                return False
        return True   
        
    
    def display(self):
        self.sprite = (self.sprite + 1) % 2
        self.update()
        self.teleport()
        if self.status == True:
            image(self.imgs[self.sprite],self.x,self.y,self.dim,self.dim)
        elif self.status == False:
            image(self.dead,self.x,self.y,self.dim,self.dim)
        #self.sprite = (self.sprite + 1) % 2
        #self.update() 

        

        
class PacMan(Creature):
    def __init__(self,x,y):
        Creature.__init__(self,x,y)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        self.vx=0
        self.vy=0
        self.dim = 20
        self.sprite = 0
        self.left1 = loadImage(path+'/images/pacmanleft1.png')
        self.left2 = loadImage(path+'/images/pacmanleft2.png')
        self.right1 = loadImage(path+'/images/pacmanright1.png')
        self.right2 = loadImage(path+'/images/pacmanright2.png')
        self.up1 = loadImage(path+'/images/pacmanup1.png')
        self.up2 = loadImage(path+'/images/pacmanup2.png')
        self.down1 = loadImage(path+'/images/pacmandown1.png')
        self.down2 = loadImage(path+'/images/pacmandown2.png')
        self.imgs = [self.right1, self.right2]
        self.time_check = False

    
        
    def update(self):
        if self.keyHandler[LEFT]:
            self.vx = -20
            self.vy = 0
            self.dir = 'LEFT'
            self.imgs = [self.left1, self.left2]
        elif self.keyHandler[RIGHT]:
            self.vx = 20
            self.vy = 0
            self.dir = 'RIGHT'
            self.imgs = [self.right1, self.right2]
        else:
            self.vx = 0 
        
        if self.keyHandler[UP]:
            self.vx = 0
            self.vy = -20
            self.dir = 'UP'
            self.imgs = [self.up1, self.up2]
        elif self.keyHandler[DOWN]:
            self.vx = 0
            self.vy = 20
            self.dir = 'DOWN'
            self.imgs = [self.down1, self.down2]
        else:
            self.vy = 0
        
                                                                                 # before we add the velocities, check if PacMan is in a square that lets him move to the next block
        nextBlockSafe = self.checkNextTile()
        if nextBlockSafe == True:
            self.x += self.vx
            self.y += self.vy
        
        for p in g.board.pellet:
            if self.x == p.x and self.y == p.y:
                g.board.pellet.remove(p)
        for s in g.board.watermelon:
            if self.x == s.x and self.y == s.y:
                g.board.watermelon.remove(s)
                # for i in range (30):
                timePeriod = 6
                self.start_time = time.time()
                g.ghost1.status = False 
                g.ghost2.status = False 
                g.ghost3.status = False 
                g.ghost4.status = False
                self.time_check = True
            if (self.time_check and (time.time()-self.start_time>=6)):
                g.ghost1.status = True 
                g.ghost2.status = True 
                g.ghost3.status = True 
                g.ghost4.status = True 
                self.time_check = False
            
    

    def display(self):
        self.sprite = (self.sprite + 1) % 2
        self.update() 
        self.teleport()
        image(self.imgs[self.sprite],self.x,self.y,self.dim,self.dim)
        
        if self.x == g.ghost1.x and self.y == g.ghost1.y and g.ghost1.status == True:
            g.__init__(540,540)
        elif self.x == g.ghost1.x and self.y == g.ghost1.y and g.ghost1.status == False:
            g.ghost1.x = 220
            g.ghost1.y = 220
            g.ghost1.display()
        if self.x == g.ghost2.x and self.y == g.ghost2.y and g.ghost2.status == True:
            g.__init__(540,540)
        elif self.x == g.ghost2.x and self.y == g.ghost2.y and g.ghost2.status == False:
            g.ghost2.x = 240
            g.ghost2.y = 220
            g.ghost2.display()
        if self.x == g.ghost3.x and self.y == g.ghost3.y and g.ghost3.status == True:
            g.__init__(540,540)
        elif self.x == g.ghost3.x and self.y == g.ghost3.y and g.ghost3.status == False:
            g.ghost3.x = 260
            g.ghost3.y = 220
            g.ghost3.display()
        if self.x == g.ghost4.x and self.y == g.ghost4.y and g.ghost4.status == True:
            g.__init__(540,540)
        elif self.x == g.ghost4.x and self.y == g.ghost4.y and g.ghost4.status == False:
            g.ghost4.x = 280
            g.ghost4.y = 220
            g.ghost4.display()
            
        

    def checkNextTile(self):                                                                             # True if moveable, False if block

        fill(255)
        
        if self.keyHandler[LEFT] or self.keyHandler[RIGHT]:
            for b in g.board.blocks:
                if self.y == b.y and self.x+self.vx == b.x:
                    self.vx = 0
                    self.vy = 0
                    return False
            
        if self.keyHandler[UP] or  self.keyHandler[DOWN]:
            for b in g.board.blocks:
                if self.x == b.x and self.y+self.vy == b.y:
                    self.vy = 0
                    self.vx = 0
                    return False
        return True   
        
class Game:
    def __init__(self,w,h):
        self.w=w
        self.h=h
        self.pacman=PacMan(260,500)
        self.ghost1=Ghosts(160,180,'red')
        self.ghost2=Ghosts(360,180,'yellow')
        self.ghost3=Ghosts(160,140,'teal')
        self.ghost4=Ghosts(360,140,'pink')
        self.board = Board()
        self.win = loadImage(path+'/images/win.png')
        
    def display(self):
        self.board.display()
        self.pacman.display()
        self.ghost1.display()
        self.ghost2.display()
        self.ghost3.display()
        self.ghost4.display()
        
    def displayWin(self):
        image(self.win,0,0,self.w,self.h)
            
g = Game(540,540)

def setup():
    frameRate(7)
    size(g.w,g.h)
    fill(255, 0, 0)
    
def draw():
    background(0)
    if len(g.board.pellet) != 0:
        g.display()
    else:
        g.displayWin()
    

def keyPressed():
    if keyCode == LEFT:
        g.pacman.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.pacman.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.pacman.keyHandler[UP] = True
    elif keyCode == DOWN:
        g.pacman.keyHandler[DOWN] = True
    if key == 'x':
        g.pacman.checkNextTile()
        
def keyReleased():
    if keyCode == LEFT:
        g.pacman.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        g.pacman.keyHandler[RIGHT] = False
    elif keyCode == UP:
        g.pacman.keyHandler[UP] = False
    elif keyCode == DOWN:
        g.pacman.keyHandler[DOWN] = False
