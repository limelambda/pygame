#importing modules
import pygame
import time

def main():

    #making things just so I can nonlocal them
    lvl_elements = None

    #making game variables
    inventory = []
    health = 0

    def draw_health():
        global health
        pygame.draw.rect(screen, ((200,100,100)), pygame.Rect(16, 16, 1248, 32))
        pygame.draw.rect(screen, ((100,200,100)), pygame.Rect(16, 16, 1248, 32))

    def load_sprite(img, size = 64):
        return pygame.transform.scale(pygame.image.load(img), (size, size))
    
    def colliding(x_1,y_1,x_2,y_2):
        x_range = range(x_2, x_2 + 64)
        y_range = range(y_2, y_2 + 64)
        if x_1 in x_range or x_1 + 64 in x_range:
            return y_1 in y_range or y_1 + 64 in y_range

    def blit_lvl_1():
        nonlocal lvl_elements
        _0_256 = Basic_lvl_element(0,256,"assets/level_assets/wall_s.png")
        _64_256 = Basic_lvl_element(64,256,"assets/level_assets/wall_s.png")
        _128_256 = Basic_lvl_element(128,256,"assets/level_assets/wall_s.png")
        _192_256 = Basic_lvl_element(192,256,"assets/level_assets/wall_s.png")
        _96_320 = Item_lvl_element(96,320,"assets/level_assets/heal.png","health potion")
        lvl_elements = [_0_256,_64_256,_128_256,_192_256,_96_320]


    class Basic_lvl_element:
        def __init__(self, x, y, sprite):
            print(f"Basic lvl element crated using sprite {sprite}!")
            self.x = x
            self.y = y
            self.sprite = load_sprite(sprite) 

        def do_blit(self):
            screen.blit(self.sprite,(self.x,self.y))

    class Item_lvl_element:
        def __init__(self, x, y, sprite, function):
            print(f"Item lvl element crated using sprite {sprite}!")
            self.x = x
            self.y = y
            self.sprite = load_sprite(sprite)
            self.function = function

        def do_blit(self):
            screen.blit(self.sprite,(self.x,self.y))

        def on_collision(self):
            nonlocal inventory, lvl_elements
            self.function()
            lvl_elements.remove(self)

    class Entity:
        def __init__(self, x, y, sprites, x_speed = 0, y_speed = 0, direction = "down"):
            self.x_speed = x_speed
            self.y_speed = y_speed
            self.x = x
            self.y = y
            self.sprites = sprites
            self.direction = direction
            print(f"Entity crated using sprites {sprites}!")
        
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
                    except:
                        print(f"no speical collision funstion triggered for {i.__class__.__name__}")
                    else:
                        print(f"speical collision funstion triggered for {i.__class__.__name__}")
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
            screen.blit(load_sprite(self.sprites[self.direction]), (self.x,self.y))

    #initializing the pygame module
    pygame.init()
    #load icon
    pygame.display.set_caption("Gam")
    #creating 240 x 180 screen surface
    screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
    #define a variable to control the main loop
    running = True
    #do da audio
    pygame.mixer.init()
    pygame.mixer.music.load("assets/song.mp3")
    #make player
    player = Entity(128, 128, {
        "down":"assets/player/down.png", 
        "up":"assets/player/up.png", 
        "left":"assets/player/left.png", 
        "right":"assets/player/right.png"})
    blit_lvl_1()
    while running:
        for i in lvl_elements:
            i.do_blit()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        screen_width, screen_height = pygame.display.get_surface().get_size()
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
        draw_health()
        pygame.display.flip()
        screen.fill((200,200,0))
        #fps limiter
        time.sleep(0.01)

if __name__=="__main__":
    #call the main function
    main()
