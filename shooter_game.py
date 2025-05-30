#Создай собственный Шутер!

from pygame import *
from random import randint


win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('MOUSE')
background = (win_width,win_height)
x1,y1 = 100,100

false = False

lost = 0
goal = 10
life = 3

speed = 5
score = 0
max_lost = 100

game = True
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            if self.rect.x > 0: 
                self.rect.x -= speed
        if keys[K_RIGHT]:
            if self.rect.x < 640: 
                self.rect.x  += speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,-15,15,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def move(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(30,win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def move(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def move(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(30,win_width - 80)
            self.rect.y = 0


background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
player = Player('rocket.png',5,win_height-80,10,65,65)
#monster = Enemy('ufo.png',win_height - 80,0,2)



play = True
font.init()
font = font.SysFont('Arial',80)

monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(80,win_width - 80),-40,randint(1,5),65,65)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png',randint(80,win_width - 80),-40,randint(1,5),65,65)
    asteroids.add(asteroid)



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()



    if play:
        window.blit(background,(0,0))


        player.draw()
        player.move()

        for m in monsters:
            m.move()
            m.draw()

        for b in bullets:
            b.move()
            b.draw() 
            
        for a in asteroids:
            a.move()
            a.draw()

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png',randint(80,win_width - 80),-40,randint(1,5),65,65)
            monsters.add(monster)

        ydar = sprite.spritecollide(player,asteroids,True)
        for y in ydar:
            life -= 1
            asteroid = Asteroid('asteroid.png',randint(80,win_width - 80),-40,randint(1,5),65,65)
            asteroids.add(asteroid)
        
        
        
        if sprite.spritecollide(player,monsters,False) or lost >= max_lost:
            play = False
            finish_img = font.render('You Lose!!',True,(180,0,0))

        if sprite.spritecollide(player,asteroids,False) or life <= 0:
            play = False
            finish_img = font.render('You Lose!!',True,(180,0,0))
        
        if score >= goal:
            play = False
            finish_img = font.render('You WIN!!',True,(0, 255, 0))

    
       # monster.draw()
       # monster.move()
    else:
        score = 0 
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        window.blit(finish_img,(200,200))

       
    display.update()
    clock.tick(FPS)
