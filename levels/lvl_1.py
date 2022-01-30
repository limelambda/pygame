from main import load_lvl, lvl_element, load_sprite
global lvl_elements, player
print("Loading lvl_1!")
heart_sprite = load_sprite("assets/level_assets/heal.png")
wall_sprite = load_sprite("assets/level_assets/wall.png")
lvl_elements = [
lvl_element(0,320,wall_sprite),
lvl_element(80,320,wall_sprite),
lvl_element(160,320,wall_sprite),
lvl_element(240,320,wall_sprite),
lvl_element(320,320,wall_sprite),
lvl_element(160,400,wall_sprite),
lvl_element(320,400,wall_sprite),
lvl_element(320,480,wall_sprite),
lvl_element(80,400,heart_sprite,player.heal),
lvl_element(0,160,heart_sprite,player.heal),
lvl_element(0,0,load_sprite("assets/level_assets/battle.jpg"),lambda : Encounter(load_sprite("assets/enemyf1.png", 120, 120),50,)),
lvl_element(160,0,load_sprite("assets/level_assets/battle.jpg"),lambda : Encounter(load_sprite("assets/enemyf1.png", 120, 120),50,)),
lvl_element(480,0,load_sprite("assets/level_assets/temp.jpg"), lambda : load_lvl("levels/game_over.py")),
lambda : screen.blit(grass_background, (0, 0))
]