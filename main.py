#importing modules
import random, pygame

#making game variables
lvl_elements = None
grass_background = pygame.image.load("assets/grass.png")

#define functions
load_sprite = lambda img, x = 80, y = 80: pygame.transform.scale(pygame.image.load(img), (x, y))

def colliding(x_1,y_1,x_2,y_2, x_size = 80, y_size = 80):
    x_range, y_range = range(x_2 + 1, x_2 + x_size), range(y_2 + 1, y_2 + y_size)
    if x_1 + 1 in x_range or x_1 + 80 in x_range:
        return y_1 + 1 in y_range or y_1 + 80 in y_range
    return x_1 < 0 or x_1 > 1200 or y_1 < 0 or y_1 > 640

def move_player_center():
    player.x, player.y = 640, 480

def load_lvl(load_lvl):
    move_player_center()
    file = open(load_lvl)
    file_content = file.read()
    print(f"loading {load_lvl}")
    file_content = "from main import load_lvl, lvl_element, load_sprite;global lvl_elements, player;" + file_content
    exec(file_content)
    del(file_content)
    file.close()
    print(f"{len(lvl_elements)} lvl elements loaded")

class lvl_element:
    def __init__(self, x, y, sprite, on_collision = None, x_size = 80, y_size = 80, persistent = False):
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
        print(f"Encounter started!")
        self.pre_encounter_coords = (player.x, player.y)
        self.pre_encounter_lvl_elements = lvl_elements
        load_lvl("levels/battle.py")
        self.x_size = 80
        self.y_size = 80
        self.on_collision = None

    def draw_health(self):
        self.health_anim += 1*(int(self.health-self.health_anim>0)-0.5)*2
        pygame.draw.rect(screen, ((200,100,100)), pygame.Rect(20, 60, 1240, 40))
        pygame.draw.rect(screen, ((100,200,100)), pygame.Rect(20, 60, 1240-(100-self.health_anim)*12.8, 40))
        if self.health_anim <= 0:
            global lvl_elements
            lvl_elements = self.pre_encounter_lvl_elements
            player.x, player.y = self.pre_encounter_coords

    def do_blit(self):
        screen.blit(self.sprite,(self.x,self.y))
        if self.health_anim != self.health:
            self.draw_health()
        else:
            player.speed = 1

    def heal(self, amount = 25):
        if self.health + amount > 100:
            self.health += (100-self.health)
        else:
            self.health += amount

    def damage(self, amount = 25, enemy_retaliates = True):
        if self.health - amount < 0:
            self.health = 0
        else:
            self.health -= amount
            if enemy_retaliates:
                player.speed = 0
                if random.getrandbits(2): #non 0 evaluates to True giving a 2 in 3 chance to damage player for 15-25 hp else use heal ability
                    player.damage(random.randint(15,25))
                else:
                    self.heal(random.randint(15,25))

class Player:
    def __init__(self, x, y, sprites, health = 100, inventory = [], speed = 1, x_speed = 0, y_speed = 0, direction = "down", x_size = 80, y_size = 80, badvar = None):
        self.x = x
        self.y = y
        self.sprites = sprites
        for k,v in self.sprites.items():
            self.sprites[k] = load_sprite(v)
        self.health = health
        self.inventory = inventory
        self.health_anim = health
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.speed = speed
        self.direction = direction
        self.x_size = x_size
        self.y_size = y_size
        self.badvar = badvar
        self.on_collision = None
        print(f"Player crated!")

    def draw_health(self):
        self.health_anim += 1*(int(self.health-self.health_anim>0)-0.5)*2
        pygame.draw.rect(screen, ((200,100,100)), pygame.Rect(20, 660, 1240, 40))
        pygame.draw.rect(screen, ((100,200,100)), pygame.Rect(20, 660, 1240-(100-self.health_anim)*12.8, 40))
        if self.health_anim <= 0:
            print("Player died")
            load_lvl("levels/game_over.py")

    def do_move(self):
        global lvl_elements
        prev_x = self.x
        prev_y = self.y
        self.x = int(round(self.x + self.x_speed / 2))
        self.y = int(round(self.y + self.y_speed / 2))
        for i in lvl_elements[:-1] + [self.badvar]:
            if colliding(self.x, self.y, i.x, i.y, i.x_size, i.y_size):
                self.damage(1)
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
        screen.blit(self.sprites[self.direction],(self.x,self.y))
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
            self.health -= amount

#initializing the pygame module
pygame.init()
#creating pygame variables
clock = pygame.time.Clock()
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
    "down":"assets/playerlmao/down.png",
    "up":"assets/playerlmao/up.png",
    "left":"assets/playerlmao/left.png",
    "right":"assets/playerlmao/right.png"},50)
player2 = Player(80, 80, {
    "down":"assets/player/down.png",
    "up":"assets/player/up.png",
    "left":"assets/player/left.png",
    "right":"assets/player/right.png"},50,badvar=player)
player.badvar=player2
load_lvl("levels/lvl_1.py")
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
                prior_level = lvl_elements 
                load_lvl("levels/pause.py")
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player.y_speed -= player.speed
    if pressed[pygame.K_DOWN]:
        player.y_speed += player.speed
    if pressed[pygame.K_RIGHT]:
        player.x_speed += player.speed
    if pressed[pygame.K_LEFT]:
        player.x_speed -= player.speed
    if pressed[pygame.K_w]:
        player2.y_speed -= player2.speed
    if pressed[pygame.K_s]:
        player2.y_speed += player2.speed
    if pressed[pygame.K_d]:
        player2.x_speed += player2.speed
    if pressed[pygame.K_a]:
        player2.x_speed -= player2.speed
    player.do_move()
    player.do_blit()
    player2.do_move()
    player2.do_blit()
    #render
    pygame.display.flip()
    #fps stuff
    clock.tick(90)
    pygame.display.set_caption(f"Gam fps:{round(clock.get_fps())}")