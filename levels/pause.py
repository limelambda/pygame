("assets/level_assets/wall.png")
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
lvl_element(664,320,load_sprite("assets/weapons/katana.png", 16, 80), lambda : [i() for i in [lambda : active_encounter.damage(random.randint(15,25)),  move_player_center,]], 16, 80, True),
active_encounter,
lambda : screen.fill((0,0,0))
]