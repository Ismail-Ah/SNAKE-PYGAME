import pygame
from sys import exit
from random import randint
from PIL import Image
pygame.init()
hight=300
width=500
screen=pygame.display.set_mode((width,hight))
clock=pygame.time.Clock()

class snake(pygame.sprite.Sprite):
    global hight,width,vitesse
    def __init__(self):
        super().__init__()
        self.pos_x=randint(10,width-10)
        self.pos_y=randint(10,hight-10)
        image_path="photo/Solid_green.png"
        self.image=pygame.image.load(image_path).convert_alpha()
        self.rect=self.image.get_rect(center=(self.pos_x,self.pos_y))
        self.direction=0
    def update(self):
        self.move()
    def move(self):
        a=False
        if len(parents)>1:
            a=True
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction=0
            if a and parents[1].rect.y<self.rect.y and parents[1].rect.x==self.rect.x: 
                self.direction=1
        elif keys[pygame.K_DOWN]:
            self.direction=1
            if a and parents[1].rect.y>self.rect.y and parents[1].rect.x==self.rect.x: 
                self.direction=0
        elif keys[pygame.K_LEFT]:
            self.direction=2
            if a and parents[1].rect.x<self.rect.x and parents[1].rect.y==self.rect.y: 
                self.direction=3
        elif keys[pygame.K_RIGHT]:
            self.direction=3
            if a and parents[1].rect.x>self.rect.x and parents[1].rect.y==self.rect.y: 
                self.direction=2
        if self.direction==0:self.up()
        elif self.direction==1:self.down()
        elif self.direction==2:self.left()
        else : self.right()
    def up(self):
        self.rect.y-=vitesse
        if self.rect.bottom<0:
            self.rect.top=hight
    def down(self):
        self.rect.y+=vitesse
        if self.rect.top>hight:
            self.rect.bottom=0
    def left(self):
        self.rect.x-=vitesse
        if self.rect.right<0:
            self.rect.left=width
    def right(self):
        self.rect.x+=vitesse
        if self.rect.left>width:
            self.rect.right=0
class eat(pygame.sprite.Sprite):
    global hight,width
    def __init__(self):
        super().__init__()
        self.posi_x=randint(10,width-10)
        self.posi_y=randint(10,hight-10)
        self.image=pygame.image.load("photo/food1.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(10,10))
        self.rect=self.image.get_rect(center=(self.posi_x,self.posi_y))

class taillesnake(snake):
    global vitesse
    def __init__(self,par,espace):
        super().__init__()
        self.rect.x=par.rect.x
        self.rect.y=par.rect.y
        if par.direction == 0: self.rect.y+=espace
        elif par.direction == 1: self.rect.y-=espace
        elif par.direction == 2: self.rect.x+=espace
        else : self.rect.x-=espace
        self.pos_x=self.rect.x
        self.pos_y=self.rect.y
        self.direction=par.direction
        self.directions=[]
        self.tim=0
        self.espace=espace
    def update(self,par,l,parent):
        self.collisio(parent,l)
        self.move(par,l)
    def collisio(self,parent,l):
        if l!=0:
            if parent.direction == 0: head=parent.rect.midtop
            elif parent.direction == 1: head=parent.rect.midbottom
            elif parent.direction == 2: head=parent.rect.midleft
            else : head=parent.rect.midright
            if self.rect.collidepoint(head):
                collision(True)
    def move(self,par,l):
        x1=par.rect.x
        y1=par.rect.y
        if par.direction == 0: y1+=self.espace
        elif par.direction == 1: y1-=self.espace
        elif par.direction == 2: x1+=self.espace
        else : x1-=self.espace
        x=self.rect.x
        y=self.rect.y
        if x!=x1 and y!=y1:
            dir=par.direction
            if dir==0:
                if x!=x1:
                    if self.rect.x>par.rect.x: self.rect.x-=vitesse
                    else : self.rect.x+=vitesse
                if y==y1: self.rect.y+=vitesse
            elif dir==1:
                    if x!=x1:
                        if x>x1: self.rect.x-=vitesse
                        else : self.rect.x+=vitesse
                    if y==y1: self.rect.y-=vitesse
            elif dir==2:
                    if y!=y1:
                        if y>y1: self.rect.y-=vitesse
                        else : self.rect.y+=vitesse
                    if x==x1: self.rect.x+=vitesse
            else:
                    if y!=y1:
                        if y>y1: self.rect.y-=vitesse
                        else : self.rect.y+=vitesse
                    if x==x1: self.rect.x-=vitesse
        else:
            self.direction=par.direction
            if self.direction==0:self.up()
            elif self.direction==1:self.down()
            elif self.direction==2:self.left()
            else : self.right()
        
snake1=pygame.sprite.GroupSingle()
snake1.add(snake())

text_font=pygame.font.Font(None,40)
score_text=text_font.render("0",False,"Green")
score_rect=score_text.get_rect(midtop=(width/2,10))

bg=pygame.image.load("photo/bg.jpg").convert_alpha()

start_game=pygame.image.load("photo/snake.jpg").convert_alpha()
start_text = text_font.render("SNAKE GAME",False,"White")
start_text_rect=start_text.get_rect(midtop=(width/2,20))
start_text2 = text_font.render("PRESS SPACE TO START",False,"Black")
start_text_rect2=start_text2.get_rect(midtop=(width/2,100))

#over
game_over=text_font.render("GAME OVER",False,"Red")
over_rect=game_over.get_rect(midtop=(width/2,20))


parents=[snake1.sprite]
lensnake=pygame.sprite.Group()
food=pygame.sprite.GroupSingle()
food.add(eat())
scor=0
vitesse=1
def score():
    global scor
    score_text=text_font.render(str(scor),False,"Green")
    return score_text

def collision(collis):
    global parents,scor,start,vites
    if collis:
        start=False
        parents=[snake1.sprite]
        lensnake.empty()
        vites=60
    """
    for elem in lensnake.sprites():
        if snake1.sprite.midtop in [elem.midright,elem.midleft,elem.midbottom]:
            pygame.quit()
            exit()
    """
def eatfood():
    global parents,scor,vites    
    if pygame.sprite.spritecollide(snake1.sprite,food,False):
        food.empty()
        if len(parents)==1:
            lensnake.add(taillesnake(parents[-1],20))
        else : lensnake.add(taillesnake(parents[-1],15))
        #music_eat.play()
        food.add(eat())
        vites+=2
        scor+=1
        parents.append(lensnake.sprites()[-1])
music_eat=pygame.mixer.Sound("music/eat.mp3")
music_game=pygame.mixer.Sound("music/snake.mp3")
music_game.play(loops=-1)
start=False
play=False
time_text=0
vites=60
#time_eat=pygame.USEREVENT+1
#pygame.time.set_timer(time_eat,1500)
while (True):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

        #if event.type == time:
        if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
            start=True
            play=True
            scor=0

    if start:
        play=True
        screen.blit(bg,(0,0))
        food.draw(screen)
        food.update()
        snake1.draw(screen)
        lensnake.draw(screen)
        for i in range(0,len(parents)-1):
            lensnake.sprites()[i].update(parents[i],i,snake1.sprite)
            if start==False:
                break
        score_text=score()
        screen.blit(score_text,score_rect)
        snake1.update()
        eatfood()
    else:
        screen.blit(start_game,(0,0))
        if time_text>=1:
            if time_text>=2:
                time_text=0
            else:time_text+=0.1
            start_text2 = text_font.render("PRESS SPACE TO START",False,"White")
        else:
            time_text+=0.1
            start_text2 = text_font.render("PRESS SPACE TO START",False,"Black")
        if play:
            fil=open("score.txt","r")
            highscore=fil.readline()
            fil.close()
            if int(highscore)<scor:
                highscore=scor
                fil=open("score.txt","w")
                fil.write(str(highscore))
                fil.close()
            endscore=text_font.render(" Your Score : "+str(scor)+" / HighScore : "+str(highscore),False,"Red")
            screen.blit(game_over,over_rect)
            screen.blit(endscore,endscore.get_rect(midtop=(width/2,50)))
        else:
            screen.blit(start_text,start_text_rect)
        screen.blit(start_text2,start_text_rect2)
    pygame.display.update()
    clock.tick(100)