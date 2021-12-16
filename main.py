#importing modules
import pygame
import time

def main():

    #making game variables
    lvl_elements = []

    def load_sprite(img, size = 80):
        return pygame.transform.scale(pygame.image.load(img), (size, size))
    
    def colliding(x_1,y_1,x_2,y_2):
        x_range = range(x_2, x_2 + 80)
        y_range = range(y_2, y_2 + 80)
        if x_1 in x_range or x_1 + 80 in x_range:
            return y_1 in y_range or y_1 + 80 in y_range

    class Basic_lvl_element:
        def __init__(self, x, y, sprite):
            print(f"Basic lvl element crated using sprite {sprite}!")
            self.x = x
            self.y = y
            self.sprite = sprite 

        def do_blit(self):
            screen.blit(self.sprite,(self.x,self.y))

    class Interactable_lvl_element:
        def __init__(self, x, y, sprite, function):
            print(f"Item lvl element crated using sprite {sprite}!")
            self.x = x
            self.y = y
            self.sprite = sprite
            self.function = function

        def do_blit(self):
            screen.blit(self.sprite,(self.x,self.y))

        def on_collision(self):
            nonlocal lvl_elements
            self.function()
            lvl_elements.remove(self)

    class Encounter:
        def __init__(self, x, y, sprite, health):
            self.x = x
            self.y = y
            self.sprite = sprite
            self.health = health
            print(f"Encounter started using sprite {sprite}!")
            #
            pre_encounter_coords = (player.x, player.y)
            player.x = 660
            lvl_elements.append()
        

    class Player:
        def __init__(self, x, y, sprites, health = 100, inventory = [], x_speed = 0, y_speed = 0, direction = "down"):
            self.x = x
            self.y = y
            self.sprites = sprites
            self.health = health
            self.inventory = inventory
            self.health_anim = 50
            self.x_speed = x_speed
            self.y_speed = y_speed
            self.direction = direction
            print(f"Player crated using sprites {sprites}!")

        def attack(self,move):
            if move == "blunt":
                print(f"")
            elif move == "slice":
                pass
            elif move == "magic":
                pass
            else:
                pass

        def draw_health(self):
            tuple_subtraction = lambda a,b:tuple(map(lambda a,b:a-b, a, b))
            self.health_anim = (self.health_anim + self.health) / 2
            pygame.draw.rect(screen, ((200,100,100)), pygame.Rect(20, 20, 1240, 40))
            pygame.draw.rect(screen, ((100,200,100)), pygame.Rect(20, 20, 1240-(100-self.health_anim)*12.8, 40))

        def do_move(self):
            nonlocal lvl_elements
            prev_x = self.x
            prev_y = self.y
            self.x = int(round(self.x + self.x_speed / 2))
            self.y = int(round(self.y + self.y_speed / 2))
            for i in lvl_elements:
                if colliding(self.x, self.y, i.x, i.y):
                    print(f"at coordinates {self.x, self.y} collision occoured at speed {self.x_speed, self.y_speed}")
                    try:
                        i.on_collision() 
                    except AttributeError:
                        print(f"no speical collision function triggered for {i.__class__.__name__}")
                    else:
                        print(f"speical collision function triggered for {i.__class__.__name__}")
                    self.x = prev_x
                    self.y = prev_y
                    self.x_speed = 0
                    self.y_speed = 0
                    print(f"Position now {self.x, self.y}")
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

    def load_lvl_1():
        nonlocal lvl_elements, player
        for i in lvl_elements:
            del i
        wall_sprite = load_sprite("assets/level_assets/wall.png")
        heart_sprite = load_sprite("assets/level_assets/heal.png")
        wall = lambda x,y:Basic_lvl_element(x*80,y*80,wall_sprite)
        
        lvl_elements = [
        wall(0,4),
        wall(1,4),
        wall(2,4),
        wall(3,4),
        wall(15,4),
        Interactable_lvl_element(80,400,heart_sprite,player.heal),
        Interactable_lvl_element(0,160,heart_sprite,player.heal),
        Interactable_lvl_element(0,0,load_sprite("assets/level_assets/heal.png"),lambda : player.attack("blunt"))
        ]

    #initializing the pygame module
    pygame.init()
    #load icon
    pygame.display.set_caption("Gam")
    #creating 240 x 180 screen surface
    screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
    #define a variable to control the main loop
    running = True
    #do da audio
    music = True
    if music:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/song.mp3")
    #make player
    player = Player(80, 80, {
        "down":"assets/player/down.png", 
        "up":"assets/player/up.png", 
        "left":"assets/player/left.png", 
        "right":"assets/player/right.png"},50)
    load_lvl_1()
    while running:
        for i in lvl_elements:
            i.do_blit()
        if music:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
        #handle events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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
        screen.fill((200,200,0))
        #fps limiter
        pygame.time.Clock().tick(45)

if __name__=="__main__":
    #call the main function
    main()