#importing modules
from fileinput import close
import pygame
 
#making game variables
lvl_elements = None
grass_background = pygame.image.load("assets/grass.png")

 #define functions
load_sprite = lambda img, x = 80, y = 80: pygame.transform.scale(pygame.image.load(img), (x, y))

def colliding(x_1,y_1,x_2,y_2, x_size = 80, y_size = 80):
    x_range = range(x_2 + 1, x_2 + x_size)
    y_range = range(y_2 + 1, y_2 + y_size)
    if x_1 + 1 in x_range or x_1 + 80 in x_range:
        return y_1 + 1 in y_range or y_1 + 80 in y_range
    return x_1 < 0 or x_1 > 1280 or y_1 < 0 or y_1 > 720

class lvl_element:
    def __init__(self, x, y, sprite, on_collision = None, x_size = 80, y_size = 80, persistent = False):
        print(f"Item lvl element crated using sprite {sprite}!")
        self.x = x
        self.y = y
        self.sprite = sprite
        self.on_collision = on_collision
        self.x_size = x_size
        self.y_size = y_size
        self.persistent = persistent

    def do_blit(self):
        screen.blit(self.sprite,(self.x,self.y))

class Encounter:
    def __init__(self, sprite, health, x = 610, y = 120):
        global active_encounter
        active_encounter = self
        self.x = x
        self.y = y
        self.sprite = sprite
        self.health = health
        self.health_anim = health
        print(f"Encounter started using sprite {sprite}!")
        self.pre_encounter_coords = (player.x, player.y)
        self.pre_encounter_lvl_elements = lvl_elements
        self.load_battle()
        self.x_size = 80
        self.y_size = 80

    def draw_health(self):
        self.health_anim += 1*(int(self.health-self.health_anim>0)-0.5)*2
        pygame.draw.rect(screen, ((200,100,100)), pygame.Rect(20, 60, 1240, 40))
        pygame.draw.rect(screen, ((100,200,100)), pygame.Rect(20, 60, 1240-(100-self.health_anim)*12.8, 40))
        if self.health_anim == 0:
            global lvl_elements
            lvl_elements = self.pre_encounter_lvl_elements
            player.x, player.y = self.pre_encounter_coords

    def do_blit(self):
        screen.blit(self.sprite,(self.x,self.y))
        if self.health_anim != self.health:
            self.draw_health()

    def heal(self, amount = 25):
        if self.health + amount > 100:
            self.health += (100-self.health)
        else:
            self.health += amount

    def damage(self, amount = 25):
        if self.health - amount < 0:
            self.health = 0
        else:
            self.health -= 25

    def load_battle(self):
        load_lvl("levels/battle")

class Player:
    def __init__(self, x, y, sprites, health = 100, inventory = [], x_speed = 0, y_speed = 0, direction = "down"):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.health = health
        self.inventory = inventory
        self.health_anim = health
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.direction = direction
        print(f"Player crated using sprites {sprites}!")

    def draw_health(self):
        self.health_anim += 1*(int(self.health-self.health_anim>0)-0.5)*2
        pygame.draw.rect(screen, ((200,100,100)), pygame.Rect(20, 660, 1240, 40))
        pygame.draw.rect(screen, ((100,200,100)), pygame.Rect(20, 660, 1240-(100-self.health_anim)*12.8, 40))

    def do_move(self):
        global lvl_elements
        prev_x = self.x
        prev_y = self.y
        self.x = int(round(self.x + self.x_speed / 2))
        self.y = int(round(self.y + self.y_speed / 2))
        for i in lvl_elements[:-1]:
            if colliding(self.x, self.y, i.x, i.y, i.x_size, i.y_size):
                print(f"at coordinates {self.x, self.y} collision occoured at speed {self.x_speed, self.y_speed}")
                if i.on_collision != None:
                    print(f"speical collision function triggered for {i.__class__.__name__}")
                    if not i.persistent:
                        lvl_elements.remove(i)
                    prev_x, prev_y = (self.x, self.y)
                    i.on_collision()
                else:
                    self.x, self.y = prev_x, prev_y
                self.x_speed, self.y_speed = 0, 0
        self.x_speed = round(self.x_speed/1.1, 4)
        self.y_speed = round(self.y_speed/1.1, 4)

    def do_blit(self):
        if abs(self.x_speed) < 0.0006:
            self.x_speed = 0
        if abs(self.y_speed) < 0.0006:
            self.y_speed = 0
        if self.x_speed != self.y_speed:
            if abs(self.x_speed) > abs(self.y_speed):
                if self.x_speed < 0:
                    self.direction = "left"
                else:
                    self.direction = "right"
            else:
                if self.y_speed < 0:
                    self.direction = "up"
                else:
                    self.direction = "down"
        screen.blit(load_sprite(self.sprites[self.direction]),(self.x,self.y))
        if self.health_anim != self.health:
            self.draw_health()

    def heal(self, amount = 25):
        if self.health + amount > 100:
            self.health += (100-self.health)
        else:
            self.health += amount

    def damage(self, amount):
        if self.health - amount < 0:
            self.health = 0
        else:
            self.health -= 25

def load_lvl(load_lvl):
    global lvl_elements, player, lvl_element
    file = open(load_lvl)
    exec(file.read())
    file.close()

 #initializing the pygame module
pygame.init()
#load icon
pygame.display.set_caption("Gam")
#creating 240 x 180 screen surface
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
#define a variable to control the main loop
running = True
#do da audio
music = False
if music:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/song.mp3")
#make player
player = Player(80, 80, {
    "down":"assets/player/down.png",
    "up":"assets/player/up.png",
    "left":"assets/player/left.png",
    "right":"assets/player/right.png"},50)
load_lvl("levels/lvl_1")
while True:
    #blit level
    lvl_elements[-1]()
    for i in lvl_elements[:-1]:
        i.do_blit()
    if music:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #change the value to False, to exit the main loop
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player.y_speed -= 1
    if pressed[pygame.K_DOWN]:
        player.y_speed += 1
    if pressed[pygame.K_RIGHT]:
        player.x_speed += 1
    if pressed[pygame.K_LEFT]:
        player.x_speed -= 1
    player.do_move()
    player.do_blit()
    #render
    pygame.display.flip()
    #fps limiter
    pygame.time.Clock().tick(60)