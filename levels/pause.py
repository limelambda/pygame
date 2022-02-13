player.x, player.y = 640, 480
wall_sprite = load_sprite("assets/level_assets/wall.png")
lvl_elements = [
lvl_element(560,240,wall_sprite),
lvl_element(560,560,wall_sprite),
lvl_element(640,240,wall_sprite),
lvl_element(640,560,wall_sprite),
lvl_element(720,240,wall_sprite),
lvl_element(720,560,wall_sprite),
lvl_element(800,240,wall_sprite),
lvl_element(800,320,wall_sprite),
lvl_element(800,400,wall_sprite),
lvl_element(800,480,wall_sprite),
lvl_element(800,560,wall_sprite),
lvl_element(480,240,wall_sprite),
lvl_element(480,320,wall_sprite),
lvl_element(480,400,wall_sprite),
lvl_element(480,480,wall_sprite),
lvl_element(480,560,wall_sprite),
lvl_element(640,340,load_sprite("assets/level_assets/again.jpg", 80, 80), lambda : load_lvl("levels/lvl_1.py"), 80, 80, True),
lambda : screen.fill((0,0,0))
]