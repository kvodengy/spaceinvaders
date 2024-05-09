import pygame
from random import randint
import time
import os
import sys 


pygame.font.init()
pygame.mixer.init()

FPS = pygame.time.Clock()
win_width = 1280
win_height = 660
p_size = 75
enemies = []
bullets = []

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Space Invaders")


class Settings():           #Клас для зображень
    def __init__(self, image, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Label:            #Клас для тексту
    def __init__(self,size,color):
        self.size = size
        self.color = color
    def set_text(self, text):
        self.text = pygame.font.SysFont('Verdana', self.size).render(text,True,self.color)
    def draw(self, x, y):
        window.blit(self.text, (x,y))

class Button(Label):            #Клас для кнопок
    def __init__(self,image,size,color,x,y,w,h):
        super().__init__(size,color)
        self.rect = pygame.Rect(x,y,w,h)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
    
    def draw(self,x,y):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.text, (self.rect.x + x, self.rect.y + y))

class Player(Settings):
    
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h)
        self.speed = s
        self.bullets = []
        self.hp = 3
        self.image_hp = pygame.transform.scale(pygame.image.load("heart.png"), (100,100))

    def draw_hp(self):
        for h in range(self.hp):
            window.blit(self.image_hp, (h*100,0))

    def move(self):
        self.draw_hp()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x<win_width-self.rect.width:
            self.rect.x += self.speed 

    def bulletshoot(self):
        global shoot
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and shoot:
            shoot = False
            bullets.append(Bullet("bullet.png", self.rect.centerx-20, self.rect.centery//1.25, 50, 100, 20))
            
class Enemy(Player):
    def __init__(self, image, x, y, w, h, s, hp):
        super().__init__(image, x, y, w, h, s)
        self.hp = hp
        
    def move(self):
        global player, enemies, finish, game
        self.rect.x += self.speed
        if self.rect.colliderect(player.rect) and self in enemies:
            damagesound.play()
            enemies.remove(self)
            pygame.mixer.music.stop()
            losesound.play()
            lose.draw()
            pygame.display.flip()
            finish = True
            pygame.time.delay(3000)
            pygame.mixer.music.play()
            game = False
        if self.rect.x > win_width - p_size or self.rect.x < 0:
            for self in enemies:
                self.rect.y = self.rect.y + 1.5*p_size
                self.speed = self.speed * -1

def levels():
    global enemies, num_enemies, start, num_level, boss
    if start == True and num_level==1:
        num_enemies = 5
        rows = 1
        x = 10
        y = 100
        for row in range(rows):
            for enemy in range(num_enemies):
                enemies.append(Enemy("alien.png", x, y, p_size, p_size, 1, 1))
                x +=1.5*p_size
            y += 1.5* p_size
        start = False
        boss = Boss("boss.png", win_width//4, -500, win_width//2, 400, 5, 3)

    elif start == True and num_level == 2:
        num_enemies = 5
        rows = 2
        x = 10
        y = 100
        for row in range(rows):
            for enemy in range(num_enemies):
                enemies.append(Enemy("alien.png", x, y, p_size, p_size, 2, 1))
                x +=1.5*p_size
            x = 10
            y += 1.5* p_size
        start = False
        boss = Boss("boss.png", win_width//4, -500, win_width//2, 400, 5, 1)

class Bullet(Player):
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h, s)

    def move(self):
        global enemies, bullets
        self.rect.y -= self.speed
        if self.rect.y < -10:
            bullets.remove(bullet)
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and self in bullets and enemy.hp>0:
                enemy.hp -= 1
                enemies.remove(enemy)
                bullets.remove(bullet)
            elif enemy.hp <=0:
                enemies.remove(enemy)
        if self.rect.colliderect(boss.rect) and self in bullets:
                    boss.hp -= 1
                    bullets.remove(self)
    def b_shoot(self):
        global player, boss, enemies
        self.rect.y += self.speed
        if self.rect.y > win_height and self in boss.boss_bullets:
            boss.boss_bullets.remove(self)
        if self.rect.colliderect(player.rect) and self in boss.boss_bullets:
            damagesound.play()
            player.hp -= 1
            boss.boss_bullets.remove(self)
        
class Boss(Player):
    def __init__(self, image, x, y, w, h, s, hp):
        super().__init__(image, x, y, w, h, s)
        self.start = False
        self.boss_bullets = []
        self.hp = hp
        self.hp1 = self.hp
        self.rect_hp = pygame.Rect(self.rect.x, 0, self.rect.width, 20)

    def move(self):
        self.show_hp()
        if self.rect.y<20:
            self.rect.y += self.speed
        else:
            self.start = True


    def show_hp(self):
        w = self.hp * self.rect.width/self.hp1

        self.rect_hp2 = pygame.Rect(self.rect.x, 0, w, 20)
        pygame.draw.rect(window, "red", self.rect_hp)
        pygame.draw.rect(window, "green", self.rect_hp2)

    def shootboss(self):
        if self.start == True and len(self.boss_bullets)==0:
            for i in range(randint(1,5)):
                x=randint(320, 960)
                self.boss_bullets.append(Bullet("bullet.png", x, self.rect.y+self.rect.height//2, 20, 40, 5))
                self.start = False
        elif self.start == False and len(self.boss_bullets)==0:
            self.start = True
        
player = Player("rocket.png", win_width//2.05, win_height//1.25, p_size, p_size, 10) 
bg = Settings("background.png", 0, 0, win_width, win_height)        #Фон
title = Settings("title.png", win_width//9, win_height//15, win_width//1.5, win_height//2.5)        #Назва гри
win = Settings("win.jpg",-50,0,win_width+50,win_height)
lose = Settings("lose.jpg",0,0,win_width, win_height)

winsound = pygame.mixer.Sound("win.mp3")
shootsound = pygame.mixer.Sound("shootsfx.mp3")
losesound = pygame.mixer.Sound("gameover.wav")
damagesound = pygame.mixer.Sound("explosion.mp3")
pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.play()

menu_buttons = [Button("button.png", 30, (255,255,255), win_width//2.4, win_height//1.8, 150, 75),       #Список кнопок меню
           Button("button.png", 30, (255,255,255), win_width//2.6, win_height//1.8+85, 225, 75),
           Button("button.png", 30, (255,255,255), win_width//2.4, win_height//1.8+170, 150, 75)]

menu_buttons[0].set_text("PLAY")             #Задання тексту для кнопок
menu_buttons[1].set_text("SETTINGS")
menu_buttons[2].set_text("EXIT")

settings_buttons = [Button("button.png", 30, (255,255,255), win_width//2.4, win_height//1.8, 150, 75),       #Список кнопок налаштувань
           Button("button.png", 30, (255,255,255), win_width//2.6, win_height//1.8+85, 225, 75),
           Button("button.png", 30, (255,255,255), win_width//2.4, win_height//1.8+170, 150, 75)]

menu = True         #Змінна рівня меню
game = False        #Змінна рівня гри
settings = False        #Змінна рівня налаштувань
finish = False
start = True
num_level = 2
current = time.time()
shoot = True

while menu:
    for event in pygame.event.get():       #Закривання гри на хрестик
        if event.type == pygame.QUIT:
            menu = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos
            if menu_buttons[0].rect.collidepoint(x,y):       #Початок гри
                game=True
                finish = False
                num_level = 1
                start = True
                # player.hp = 3
            if menu_buttons[1].rect.collidepoint(x,y):       #Кнопка налаштувань
                settings = True
            if menu_buttons[2].rect.collidepoint(x,y):       #Кнопка EXIT
                menu = False
    if game != True:        #Рівень меню
        bg.draw()
        for b in menu_buttons:
            b.draw(35, 20)
        title.draw()
        pygame.display.flip()
        FPS.tick(60)
    else:
        while game == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    finish = True
                    title[0].set_text("CONTINUE")
                    status_menu = True
                    game = False
                    while status_menu:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                status_menu = False
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                x,y = event.pos
                                if title[0].rect.collidepoint(x,y):
                                    status_menu = False
                                    finish = False
                                    game = True
                                if title[1].rect.collidepoint(x,y):
                                    status_menu = False
                                    game = False
                        if game != True:
                            bg.draw()
                            for b in title:
                                b.draw(20,20)
                            pygame.display.flip()
                            FPS.tick(60)
                        else:
                            status_menu = True
                            title[0].set_text("PLAY")
                            break

            if finish != True:
                bg.draw()
                player.draw()
                player.move()
                player.bulletshoot()
                
                levels()

                if time.time()-current>0.5:
                    current = time.time()
                    shoot = True
            
                for enemy in enemies:
                    enemy.move()
                    enemy.draw()

                for bullet in bullets:
                    shootsound.play()
                    bullet.move()
                    bullet.draw()
                    
                if len(enemies) == 0:
                    boss.move()
                    if boss.rect.y >= 20:
                        boss.shootboss()
                    boss.draw()
                    for b in boss.boss_bullets:
                        b.b_shoot()
                        b.draw()

                    if boss.hp <= 0:
                        start = True
                        num_level += 1
                
                if player.hp <= 0:
                    pygame.mixer.music.stop()
                    losesound.play()
                    lose.draw()
                    pygame.display.flip()
                    finish = True
                    pygame.time.delay(3000)
                    pygame.mixer.music.play()
                    game = False


                if num_level > 2 and boss.hp<=0:
                    pygame.mixer.music.stop()
                    winsound.play()
                    win.draw()
                    pygame.display.flip()
                    finish = True
                    pygame.time.delay(3000)
                    pygame.mixer.music.play()
                    game = False  
            
            pygame.display.flip()
            FPS.tick(60)