import pygame
#randint для рандомної кількості лазерів босса
from random import randint
#time для таймеру стрільби гравця (можна стріляти лише 2 рази в секунду)
import time


pygame.font.init()
pygame.mixer.init()

FPS = pygame.time.Clock()
win_width = 1280 #Ширина вікна
win_height = 660 #Висота вікна
p_size = 75 #Розмір прибульців
enemies = [] #Список прибульців
bullets = [] #Список куль гравця
powerups = []
first_enemy_x = 0 #х координата першого прибульця (надається в levels())
last_enemy_x = 0 #х координата останнього прибульця (надається в levels())
enemy_speed = 0 #швидкість прибульця (надається в levels())

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

class Player(Settings):     #Клас гравця
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h)
        self.speed = s
        self.bullets = []
        self.hp = 3
        self.image_hp = pygame.transform.scale(pygame.image.load("heart.png"), (100,100))
        self.counter = 0

    def draw_hp(self):          #Показ здоров'я
        for h in range(self.hp):
            window.blit(self.image_hp, (h*100,0))

    def move(self):        #рух
        self.draw_hp()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x>3*p_size:
            self.rect.x -= self.speed
            self.image = pygame.transform.scale(pygame.image.load("rocketleft.png"), (2*p_size, 2*p_size))
        elif keys[pygame.K_RIGHT] and self.rect.x<win_width-3*p_size:
            self.rect.x += self.speed 
            self.image = pygame.transform.scale(pygame.image.load("rocketright.png"), (2*p_size, 2*p_size))
        else:
            self.image = pygame.transform.scale(pygame.image.load("rocket.png"), (2*p_size, 2*p_size))

    def bulletshoot(self):      #Стрільба
        global shoot
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and shoot:
            shoot = False
            shootsound.play()
            bullets.append(Bullet("bullet.png", self.rect.centerx-20, self.rect.centery//1.25, 50, 100, 20))

    def powerupshoot(self):
        global powerup_ready
        if powerup_ready:
            powerup_ready = False
            powerups.append(Powerup("powerup.png", randint(0,win_width), -2*p_size, 2*p_size, 2*p_size, 10))
            
class Enemy(Player):        #Клас прибульців
    def __init__(self, image, x, y, w, h, s, hp):
        super().__init__(image, x, y, w, h, s)
        self.hp = hp
        self.start = False
        self.enemy_bullets = []  
        
    def move(self):     #Рух
        global player, enemies, finish, game, last_enemy_x, first_enemy_x, floor
        self.rect.x += self.speed  
        if self.rect.y > win_height-2*p_size and self in enemies:
            damagesound.play()
            enemies.clear()
            pygame.mixer.music.stop()
            losesound.play()
            lose.draw()
            pygame.display.flip()
            finish = True
            pygame.time.delay(3000)
            pygame.mixer.music.play()
            game = False
        if floor:       #Рух ворогів вниз
            for self in enemies:
                self.rect.y = self.rect.y + 1.5*p_size
                self.speed = self.speed * -1
            floor = False

def levels():       #Зміна для рівнів
    global enemies, num_enemies, start, num_level, boss, lf_speed, last_enemy_x, first_enemy_x
    if start == True and num_level==1:      #Перший рівень
        enemy_speed = 3
        lf_speed = enemy_speed
        num_enemies = 1
        rows = 1
        last_enemy_x = win_width//2 + num_enemies//2*p_size*1.5
        first_enemy_x = win_width//2 - num_enemies//2*1.5*p_size
        x = win_width//2 - num_enemies//2*1.5*p_size
        y = 100
        for row in range(rows):     #Поява ворогів
            for enemy in range(num_enemies):
                enemies.append(Enemy("alien.png", x, y, p_size, p_size, enemy_speed, 1))
                x +=1.5*p_size
            x = win_width//2 - num_enemies//2*1.5*p_size
            y += 1.5* p_size
        start = False
        boss = Boss("boss1.png", win_width//4, -500, win_width//2, 400, 3, 5)

    if start == True and num_level == 2:        #Другий рівень
        enemy_speed = 3
        lf_speed = enemy_speed
        num_enemies = 5
        rows = 2
        last_enemy_x = win_width//2 + num_enemies//2*p_size*1.5
        first_enemy_x = win_width//2 - num_enemies//2*1.5*p_size
        x = win_width//2 - num_enemies//2*1.5*p_size
        y = 100
        for row in range(rows):
            for enemy in range(num_enemies):
                enemies.append(Enemy("alien.png", x, y, p_size, p_size, enemy_speed, 1))
                x +=1.5*p_size
            x = win_width//2 - num_enemies//2*1.5*p_size
            y += 1.5* p_size
        start = False
        boss = Boss("boss2.png", win_width//4, -500, win_width//2, 400, 10, 10)

    elif start == True and num_level == 3:      #Третій рівень
        enemy_speed = 3
        lf_speed = enemy_speed
        num_enemies = 5
        rows = 3
        last_enemy_x = win_width//2 + num_enemies//2*p_size*1.5
        first_enemy_x = win_width//2 - num_enemies//2*1.5*p_size
        x = win_width//2 - num_enemies//2*1.5*p_size
        y = 0
        for row in range(rows):
            for enemy in range(num_enemies):
                enemies.append(Enemy("alien.png", x, y, p_size, p_size, enemy_speed, 1))
                x +=1.5*p_size
            x = win_width//2 - num_enemies//2*1.5*p_size
            y += 1.5* p_size
        start = False
        boss = Boss("boss3.png", win_width//4, -500, win_width//2, 400, 10, 15)

class Bullet(Player):       #Клас куль
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h, s)

    def move(self):     #Рух
        global enemies, bullets
        self.rect.y -= self.speed
        if self.rect.y < -10:
            bullets.remove(bullet)
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and self in bullets and enemy in enemies:
                enemies.remove(enemy)
                bullets.remove(bullet)
            elif enemy.hp <=0:
                enemies.remove(enemy)
        if self.rect.colliderect(boss.rect) and self in bullets:
                    boss.hp -= 1
                    bullets.remove(self)

    def b_shoot2(self):     #Стрільба другого боса
        global player, boss, enemies
        self.rect.y += self.speed
        if self.rect.y > win_height and self in boss.boss_bullets:
            boss.boss_bullets.remove(self)
        if self.rect.colliderect(player.rect) and self in boss.boss_bullets:
            damagesound.play()
            player.hp -= 1
            boss.boss_bullets.remove(self)

    def b_shoot3(self):     #Стрільба третього боса
        global player, boss, enemies
        self.rect.y += self.speed
        if self.rect.y > win_height and self in boss.boss_bullets:
            boss.boss_bullets.remove(self)
        if self.rect.colliderect(player.rect) and self in boss.boss_bullets:
            damagesound.play()
            player.hp -= 1
            boss.boss_bullets.remove(self)
      
class Boss(Player):     #Клас боса
    def __init__(self, image, x, y, w, h, s, hp):
        super().__init__(image, x, y, w, h, s)
        self.start = False
        self.boss_bullets = []
        self.enemy_bullets = []
        self.hp = hp
        self.hp1 = self.hp
        self.rect_hp = pygame.Rect(win_width//4, 0, self.rect.width, 20)

    def move1(self):    #Рух першого боса
        self.show_hp()
        self.rect.y += self.speed
        if self.rect.colliderect(player.rect):
            player.hp = 0

    def move2(self):    #Рух другого боса
        self.show_hp()
        if self.rect.y<20:
            self.rect.y += self.speed
        else:
            self.start = True

    def move3(self):    #Рух третього боса
        self.show_hp()
        if self.rect.y<20:
            self.rect.y += self.speed
        else:
            self.start = True
        
        

    def show_hp(self):  #Показ здоров'я боса
        w = self.hp * self.rect.width/self.hp1

        self.rect_hp2 = pygame.Rect(win_width//4, 0, w, 20)
        pygame.draw.rect(window, "red", self.rect_hp)
        pygame.draw.rect(window, "green", self.rect_hp2)

    def shootboss2(self):   #Стрільба другого боса
        if self.start == True and len(self.boss_bullets)==0:
            for i in range(randint(1,1)):
                x=randint(320, 960)
                self.boss_bullets.append(Bullet("bullet.png", x, self.rect.y+self.rect.height//2, 20, 40, 10))
                self.start = False
        elif self.start == False and len(self.boss_bullets)==0:
            self.start = True

    def shootboss3(self):       #Стрільба другого боса
        if self.start == True and len(self.boss_bullets)==0:
            for i in range(randint(3,5)):
                x=randint(320, 960)
                self.boss_bullets.append(Bullet("bullet.png", x, self.rect.y+self.rect.height//2, 20, 40, 5))
                self.start = False
        elif self.start == False and len(self.boss_bullets)==0:
            self.start = True

class Powerup(Player):
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h, s)

    def move(self):
        global powerup_active
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            powerups.remove(self)
        elif self.rect.colliderect(player.rect):
            powerups.remove(self)
            powerup_active = True
                
        
        
player = Player("rocket.png", win_width//2., win_height//1.3, 2*p_size, 2*p_size, 10)   #Гравець
bg = Settings("background.png", 0, 0, win_width, win_height)        #Фон
title = Settings("title.png", win_width//9, win_height//15, win_width//1.5, win_height//2.5)        #Назва гри
win = Settings("win.jpg",-50,0,win_width+50,win_height)     #Екран перемоги
lose = Settings("lose.jpg",0,0,win_width, win_height)       #екран програшу

winsound = pygame.mixer.Sound("win.mp3")
shootsound = pygame.mixer.Sound("shootsfx.mp3")
losesound = pygame.mixer.Sound("gameover.wav")
damagesound = pygame.mixer.Sound("explosion.mp3")
pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.play()

menu_buttons = [Button("button.png", 30, (255,255,255), win_width//2.4, win_height//1.8, 150, 75),       #Список кнопок меню
           Button("button.png", 30, (255,255,255), win_width//2.6, win_height//1.8+85, 225, 75),
           Button("button.png", 30, (255,255,255), win_width//2.4, win_height//1.8+170, 150, 75)]

menu_buttons[0].set_text("PLAY")             #Надання тексту для кнопок
menu_buttons[1].set_text("SETTINGS")
menu_buttons[2].set_text("EXIT")

settings_buttons = [Button("button.png", 30, (255,255,255), win_width//12.8, win_height//1.3, 225, 75),         #Список кнопок налаштувань
                    Button("settings.png", 30, (255,255,255), win_width//3, win_height//3, win_width//2, win_height//2)]       

settings_buttons[0].set_text("RETURN")      #Надання тексту до кнопок
settings_buttons[1].set_text(" ")

menu = True         #Змінна рівня меню
game = False        #Змінна рівня гри
settings = False        #Змінна рівня налаштувань
finish = False      #Змінна перевірки кінця гри
start = True        #Змінна перевірки початку гри
num_level = 1       #Змінна рівня
current = time.time()   #Змінна часу для таймера
current_p = time.time()
shoot = True        #Змінна перевірки стрільби
floor = False       #Змінна переходу ворогів вниз
powerup_active = False
powerup_ready = False

while menu:
    for event in pygame.event.get():       #Закривання гри на хрестик
        if event.type == pygame.QUIT:
            menu = False
        pos = pygame.mouse.get_pos()        
        for b in menu_buttons:      #Анімація кнопок
            if b.rect.collidepoint(pos):
                b.image = pygame.transform.scale(pygame.image.load("buttonpressed.png"), (b.rect.width, b.rect.height))
            else:
                b.image = pygame.transform.scale(pygame.image.load("button.png"), (b.rect.width, b.rect.height))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos
            if menu_buttons[0].rect.collidepoint(x,y):       #Початок гри
                game=True
                finish = False
                num_level = 1
                start = True
                player.hp = 3
            if menu_buttons[1].rect.collidepoint(x,y):      #Кнопка налаштувань
                settings = True      
            if menu_buttons[2].rect.collidepoint(x,y):       #Кнопка EXIT
                menu = False

    while settings:
        pos = pygame.mouse.get_pos()        #Анімація кнопок
        if settings_buttons[0].rect.collidepoint(pos):
            settings_buttons[0].image = pygame.transform.scale(pygame.image.load("buttonpressed.png"), (settings_buttons[0].rect.width, settings_buttons[0].rect.height))
        else:
            settings_buttons[0].image = pygame.transform.scale(pygame.image.load("button.png"), (settings_buttons[0].rect.width, settings_buttons[0].rect.height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos
                if settings_buttons[0].rect.collidepoint(x,y):
                    menu = True
                    settings = False
        if game != True:
            bg.draw()
            title = Settings("title.png", win_width//3.3, win_height//15, win_width//3, win_height//5)
            title.draw()
            for b in settings_buttons:
                b.draw(35, 20)                         
            pygame.display.flip()
            FPS.tick(60)
    if game != True:        #Рівень меню
        bg.draw()
        for b in menu_buttons:
            b.draw(35, 20)
        title = Settings("title.png", win_width//9, win_height//15, win_width//1.5, win_height//2.5)
        title.draw()
        pygame.display.flip()
        FPS.tick(60)
    else:
        while game == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                    menu = False
                if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:         #Кнопки, анімації під час паузи
                    finish = True
                    menu_buttons[0] = Button("button.png", 30, (255,255,255), win_width//2.6, win_height//1.8, 225, 75)
                    menu_buttons[0].set_text("CONTINUE")
                    menu = True
                    game = False
                    while menu:
                        pos = pygame.mouse.get_pos()
                        for b in menu_buttons:
                            if b.rect.collidepoint(pos):
                                b.image = pygame.transform.scale(pygame.image.load("buttonpressed.png"), (b.rect.width, b.rect.height))
                            else:
                                b.image = pygame.transform.scale(pygame.image.load("button.png"), (b.rect.width, b.rect.height))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                menu = False
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                x,y = event.pos
                                if menu_buttons[0].rect.collidepoint(x,y):
                                    menu = False
                                    finish = False
                                    game = True
                                if menu_buttons[1].rect.collidepoint(x,y):
                                    settings = True
                                if menu_buttons[2].rect.collidepoint(x,y):
                                    menu = False
                                    game = False
                        if game != True:
                            bg.draw()
                            title = Settings("title.png", win_width//9, win_height//15, win_width//1.5, win_height//2.5)
                            title.draw()
                            for b in menu_buttons:
                                b.draw(20,20)
                            pygame.display.flip()
                            FPS.tick(60)
                        else:
                            menu = True
                            menu_buttons[0] = Button("button.png", 30, (255,255,255), win_width//2.4, win_height//1.8, 150, 75)
                            menu_buttons[0].set_text("PLAY")
                            break
                        while settings:
                            pos = pygame.mouse.get_pos()
                            if settings_buttons[0].rect.collidepoint(pos):
                                settings_buttons[0].image = pygame.transform.scale(pygame.image.load("buttonpressed.png"), (settings_buttons[0].rect.width, settings_buttons[0].rect.height))
                            else:
                                settings_buttons[0].image = pygame.transform.scale(pygame.image.load("button.png"), (settings_buttons[0].rect.width, settings_buttons[0].rect.height))
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    settings = False
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    x,y = event.pos
                                    if settings_buttons[0].rect.collidepoint(x,y):
                                        title = Settings("title.png", win_width//9, win_height//15, win_width//1.5, win_height//2.5)
                                        menu = True
                                        settings = False
                            if game != True:
                                title = Settings("title.png", win_width//3.3, win_height//15, win_width//3, win_height//5)
                                bg.draw()
                                title.draw()
                                for b in settings_buttons:
                                    b.draw(35, 20)                         
                                pygame.display.flip()
                                FPS.tick(60)

            if finish != True:      #Початок гри
                bg.draw()
                player.draw()
                player.move()
                player.bulletshoot()
                player.powerupshoot()
                
                levels()

                last_enemy_x += lf_speed        
                first_enemy_x += lf_speed
                if last_enemy_x >= win_width -100 or first_enemy_x <= 0:      #Таймер для зниження ворогів  
                    floor = True
                    lf_speed *= -1

                if time.time()-current>0.5:     #Таймер стрільби
                    current = time.time()
                    shoot = True
                
                if time.time()-current_p>3:
                    powerup_ready = True
                    current_p = time.time()
                    

                for powerup in powerups:
                    powerup.move()
                    powerup.draw()


                for enemy in enemies:   #Вороги
                    enemy.move()
                    enemy.draw()

                for bullet in bullets:  #Кулі гравця
                    bullet.move()
                    bullet.draw()
                
                if len(enemies) == 0:   #Рівні
                    if num_level == 1:
                        boss.move1()
                        boss.draw()
                    if num_level == 2:
                        boss.move2() 
                        if boss.rect.y >= 20:
                            boss.shootboss2()
                        boss.draw()
                        for b in boss.boss_bullets:
                            b.b_shoot2()
                            b.draw()
                    if num_level == 3:
                        boss.move3()
                        if boss.rect.y >= 20:
                            boss.shootboss3()
                        boss.draw()
                        for b in boss.boss_bullets:
                            b.b_shoot3()
                            b.draw()
                    if boss.hp <= 0:
                        start = True
                        num_level += 1

                if player.hp <= 0:  #Програш
                    pygame.mixer.music.stop()
                    losesound.play()
                    lose.draw()
                    pygame.display.flip()
                    finish = True
                    pygame.time.delay(3000)
                    pygame.mixer.music.play()
                    game = False  

                if num_level > 3 and boss.hp<=0:    #Перемога
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