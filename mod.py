import pygame as pg
import json

# Variables
tile = 46
size_screen = 17
game_size = 16
screen_width = tile*size_screen+tile*4
screen_height = tile*size_screen
screen = pg.display.set_mode((screen_width, screen_height))

pg.init()
pg.display.set_caption('Level Editor')
timer = pg.time.Clock()
running = True
game_status = "menu"
editor_filename = None


background_textures = ["assets/backgrounds/fond_2.png",
                "assets/backgrounds/fond_1.png",
                "assets/backgrounds/fond_3.png",
                "assets/backgrounds/fond_gem.png",
                "assets/backgrounds/fond_glace.png",
                "assets/backgrounds/fond_lave.png",]
objects_textures = ["assets/objects/vide.png",
                "assets/objects/obsatcle_1.png",
                "assets/objects/obstacle_vert1.png",
                "assets/objects/obstacle_vert2.png",
                "assets/objects/obstacle_gem.png",
                "assets/objects/obstacle_glace.png",
                "assets/objects/obstacle_lave.png",]
items_textures = ["assets/objects/pierre_1.png"]              
enemies_textures = ["assets/enemies/black_fly.png"]

# Text 
font = pg.font.Font(None, 36)
xs_font = pg.font.Font(None, 24)

def main():
    global game_status
    global running

    # add background
    # background = pg.image.load("assets/backgrounds/fond_menu.png")
    # screen.blit(background, (0, 0))
    screen.fill((200,200,200))

    # Add title centered
    title = pg.image.load("assets/images/titre.png")
    pos_x_title = screen_width/2 - title.get_width()/2
    screen.blit(title, (pos_x_title, 150))
    # Add subtitle centered
    subtitle = pg.image.load("assets/mod/images/EDITOR.png")
    screen.blit(subtitle, (pos_x_title+title.get_width() - subtitle.get_width()/1.5, 130+title.get_height()))

    create_level_button = Button("assets/mod/buttons/CREER-UN-NIVEAU.png", screen_width/2 - 100, 400)
    create_level_button.draw()
    select_level_button = Button("assets/mod/buttons/liste-des-niveaux.png", screen_width/2 - 110, 500)
    select_level_button.draw()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if create_level_button.is_clicked():
            game_status = "create_level"
        elif select_level_button.is_clicked():
            game_status = "select_level"

        if game_status == "editor":
            editor(0)
        elif game_status == "create_level":
            create_level()
        elif game_status == "select_level":
            select_level()

        pg.display.flip()

    pg.quit()

def select_level():
    global running
    global game_status

    screen = pg.display.set_mode((screen_width, screen_height))
    screen.fill((200,200,200))

    # Add title centered
    title = pg.image.load("assets/images/titre.png")
    pos_x_title = screen_width/2 - title.get_width()/2
    screen.blit(title, (pos_x_title, 150))
    # Add subtitle centered
    subtitle = pg.image.load("assets/mod/images/EDITOR.png")
    screen.blit(subtitle, (pos_x_title+title.get_width() - subtitle.get_width()/1.5, 130+title.get_height()))

    # Load level
    with open("data.json", "r") as file:
        content = json.load(file)
        levels = content["levels"]

    # Add levels
    levels_buttons = []
    for i in range(len(levels)):
        if levels[i]["locked"] == False:
            button_level = Button("assets/mod/buttons/LEVEL.png", 20, 400 + i*50)
            levels_buttons.append({
                "button": button_level,
                "level": levels[i]
            })
            button_level.draw()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        for i in range(len(levels_buttons)):
            if levels_buttons[i]["button"].is_clicked():
                editor(levels_buttons[i]["level"]["id"])
                # game_status = "editor"

        pg.display.flip()


def create_level():
    global running
    global editor_filename

    running_create_level = True
    pg.display.set_mode((tile*7, tile*4))

    # add background
    screen.fill((200,200,200))

    title = font.render("Nom du niveau", True, (0,0,0))
    screen.blit(title, (tile, 10))

    # Input text 
    input_text = pg.Rect(tile, 50, tile*5, tile)
    color = (255,255,255)
    active = False
    text = ""

    # create button
    create_button = Button("assets/mod/buttons/CREER.png", tile*3, tile*3)
    create_button.draw()

    while running_create_level:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if input_text.collidepoint(event.pos):
                    active = True
                else:
                    active = False  

            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 10:
                            text += event.unicode

        if active:
            color = (255,255,255)
        else:
            color = (150, 150, 150) 
        
        pg.draw.rect(screen, color, input_text)

        txt_surface = font.render(text, True, (0,0,0))
        screen.blit(txt_surface, (input_text.x+5, input_text.y+5))

        if create_button.is_clicked():
            with open("data.json", "r+") as file:
                content = json.load(file)
                levels = content["levels"]
                level_found = False
                for level in levels:
                    if level["name"] == text:
                        level_found = True
                if level_found == True:
                    error_msg = xs_font.render("Ce niveau existe déjà !", True, (240,0,0))
                    screen.blit(error_msg, (tile, tile*2+20))
                else:
                    print("AJOUTER")
                    levels.append({
                    "id": len(levels),
                    "name": text,
                    "description": "Niveau créé par l'éditeur",
                    "textures_map": 0,
                    "locked": False,
                    "player_coordinates": [1,1],
                    "background" : [
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    ],
                    "objects": [
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                    ],
                    "items" : [],
                    "enemy": [] 
                })
                file.seek(0) 
                json.dump(content, file)
                file.truncate()
                running_create_level = False
                editor(len(levels)-1)
        pg.display.flip()

def editor(idlevel):
    global game_status
    global running

    screen = pg.display.set_mode((screen_width, screen_height))
    screen.fill((200,200,200))

    # Add title centered
    title = pg.image.load("assets/images/titre.png")
    pos_x_title = screen_width/2 - title.get_width()/2
    screen.blit(title, (pos_x_title, 150))
    # Add subtitle centered
    subtitle = pg.image.load("assets/mod/images/EDITOR.png")
    screen.blit(subtitle, (pos_x_title+title.get_width() - subtitle.get_width()/1.5, 130+title.get_height()))

    # Draw border around
    pg.draw.rect(screen, (0,0,0), (0, 0, tile*16, tile*16), 3)

    # Load level
    background = []
    objects = []
    items = []
    enemies = [] 
    player = []
    with open("data.json", "r") as file:
        content = json.load(file)
        levels = content["levels"]
        for level in levels:
            if level["id"] == idlevel:
                background = level["background"]
                objects = level["objects"]
                items = level["items"]
                enemies = level["enemy"]
                player = level["player_coordinates"]
                print("FOUND")

    # Button events
    save_button = Button("assets/mod/buttons/SAUVEGARDER.png", tile*1, screen_height-tile*1)
    save_button.draw()

    back_button = Button("assets/mod/buttons/RETOUR.png", tile*3, screen_height-tile*1)
    back_button.draw()

    # Add text section
    title_section_layer = font.render("Couches", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 50))

    selected_layer = 0 # 0: background 1: object 2: item 3: enemy 4: player

    # add all backgrounds button
    title_section_layer = font.render("Fonds", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 90))

    background_buttons = []
    selected_background_layer = 0
    for i in range(len(background_textures)):

        pos_x_background_layer = i % 4
        pos_y_background_layer = i // 4

        background_buttons.append(Button(background_textures[i], screen_width-tile*4+pos_x_background_layer*tile, 130+pos_y_background_layer*tile))
        background_buttons[i].draw()
        if selected_background_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+pos_x_background_layer*tile, 130+pos_y_background_layer*tile, tile, tile), 3)

    # add all objects button
    title_section_layer = font.render("Objets", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 300))

    objects_buttons = []
    selected_objects_layer = 0
    for i in range(len(objects_textures)):

        pos_x_objects_layer = i % 4
        pos_y_objects_layer = i // 4 
    
        objects_buttons.append(Button(objects_textures[i], screen_width-tile*4+pos_x_objects_layer*tile, 330+pos_y_objects_layer*tile))
        objects_buttons[i].draw()
        if selected_objects_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+pos_x_objects_layer*tile, 330+pos_y_objects_layer*tile, tile, tile), 3)

    # add all items button
    title_section_layer = font.render("Items", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 500))

    items_buttons = []
    selected_items_layer = 0
    for i in range(len(items_textures)):
        
        pos_x_items_layer = i % 4
        pos_y_items_layer = i // 4

        items_buttons.append(Button(items_textures[i], screen_width-tile*4+pos_x_items_layer*tile, 530+pos_y_items_layer*tile))
        items_buttons[i].draw()
        if selected_items_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+pos_x_items_layer*tile, 530+pos_y_items_layer*tile, tile, tile), 3)

    # add all enemies button
    title_section_layer = font.render("Ennemis", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 600))

    enemies_buttons = []
    selected_enemies_layer = 0
    first_enemy_position = (0,0)
    second_enemy_position = (0,0)
    
    for i in range(len(enemies_textures)):
        enemies_buttons.append(Button(enemies_textures[i], screen_width-tile*4+i*tile, 630))
        enemies_buttons[i].draw()
        if selected_enemies_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 630, tile, tile), 3)

    # Add player button
    player_button = Button("assets/player/perso_d2.png", tile*5, screen_height-tile*1)
    player_button.draw()


    # add collision for each tile
    background_tiles_editor = []
    for x in range(0, tile*game_size, tile):
        for y in range(0, tile*game_size, tile):
            rect = pg.Rect(x, y, tile, tile)
            background_tiles_editor.append(rect)    

    # Boucle de jeu de l'editeur
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Choice background
        for i in range(len(background_buttons)):
            if background_buttons[i].is_clicked():
                selected_background_layer = i
                selected_layer = 0
                line = i // 4
                column = i % 4
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+column*tile, 130+line*tile, tile, tile), 3)
                for j in range(len(background_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+(j%4)*tile, 130+(j//4)*tile, tile, tile), 3)

        # Choice objects
        for i in range(len(objects_buttons)):
            if objects_buttons[i].is_clicked():
                selected_objects_layer = i
                selected_layer = 1
                line = i // 4
                column = i % 4
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+column*tile, 330+line*tile, tile, tile), 3)
                for j in range(len(objects_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+(j%4)*tile, 330+(j//4)*tile, tile, tile), 3)

        # Choice items
        for i in range(len(items_buttons)):
            if items_buttons[i].is_clicked():
                selected_items_layer = i
                selected_layer = 2
                line = i // 4
                column = i % 4
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+column*tile, 530+line*tile, tile, tile), 3)
                for j in range(len(items_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+(j%4)*tile, 530+(j//4)*tile, tile, tile), 3)

        # Choice enemies
        for i in range(len(enemies_buttons)):
            if enemies_buttons[i].is_clicked():
                selected_enemies_layer = i
                selected_layer = 3
                line = i // 4
                column = i % 4
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+column*tile, 630+line*tile, tile, tile), 3)
                for j in range(len(items_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+(j%4)*tile, 630+(j//4)*tile, tile, tile), 3)

        # Choice player
        if player_button.is_clicked():
            selected_layer = 4

        # Detect click on background and draw it
        if selected_layer == 0:
            for rect in background_tiles_editor:
                if rect.collidepoint(pg.mouse.get_pos()):
                    if pg.mouse.get_pressed()[0] == 1:
                        x = rect.x//tile
                        y = rect.y//tile
                        background[y][x] = selected_background_layer
        elif selected_layer == 1:
            for rect in background_tiles_editor:
                if rect.collidepoint(pg.mouse.get_pos()):
                    if pg.mouse.get_pressed()[0] == 1:
                        x = rect.x//tile
                        y = rect.y//tile
                        objects[y][x] = selected_objects_layer
        elif selected_layer == 2:
            for rect in background_tiles_editor:
                if rect.collidepoint(pg.mouse.get_pos()):
                    if pg.mouse.get_pressed()[0] == 1:
                        x = rect.x//tile
                        y = rect.y//tile
                        
                        if not any(item["x"] == x and item["y"] == y for item in items):
                            items.append({
                                "type": selected_items_layer,
                                "x": x,
                                "y": y,
                                "image": "assets/objects/pierre_1.png"
                            })
                        else:
                            items = [item for item in items if not (item["x"] == x and item["y"] == y)]
        elif selected_layer == 3:
            for rect in background_tiles_editor:
                if rect.collidepoint(pg.mouse.get_pos()):
                    if pg.mouse.get_pressed()[0] == 1:
                        print("CLICKED ENEMY")
                        x = rect.x//tile
                        y = rect.y//tile
                        if first_enemy_position == (0,0):
                            first_enemy_position = (x,y)
                        else:
                            second_enemy_position = (x,y)
                            # Check if enemy already exists
                            enemy_exists = False
                            for enemy in enemies:
                                if enemy["x"] == first_enemy_position[0] and enemy["y"] == first_enemy_position[1]:
                                    enemy_exists = True
                                    break
                            if not enemy_exists:
                                enemies.append({
                                    "type": "black_fly",
                                    "x": first_enemy_position[0],
                                    "y": first_enemy_position[1],
                                    "speed": 1,
                                    "from_x": first_enemy_position[0],
                                    "from_y": first_enemy_position[1],
                                    "to_x": second_enemy_position[0],
                                    "to_y": second_enemy_position[1]
                                })
                                print("ENEMY ADDED")
                            else:
                                print("ENEMY ALREADY EXISTS")
                            first_enemy_position = (0,0)
                            second_enemy_position = (0,0)
        elif selected_layer == 4:
            pg.draw.rect(screen, (255,0,0), (tile*5, screen_height-tile*1, tile, tile), 3)
            for rect in background_tiles_editor:
                if rect.collidepoint(pg.mouse.get_pos()):
                    if pg.mouse.get_pressed()[0] == 1:
                        x = rect.x//tile
                        y = rect.y//tile
                        player = [x,y]

        # Draw background
        for y in range(len(background)):
            for x in range(len(background[y])):
                screen.blit(pg.image.load(background_textures[background[y][x]]), (x*tile, y*tile))

        # Draw objects
        for y in range(len(objects)):
            for x in range(len(objects[y])):
                image = pg.image.load(objects_textures[objects[y][x]])
                if selected_layer != 1:
                    image.set_alpha(120)
                screen.blit(image, (x*tile, y*tile))

        # Draw items
        for item in items:
            screen.blit(pg.image.load(items_textures[item["type"]]), (item["x"]*tile, item["y"]*tile))

        # Draw enemies
        for enemy in enemies:
            # draw enemy with case red and green color (from and to)
            pg.draw.rect(screen, (255,0,0), (enemy["from_x"]*tile, enemy["from_y"]*tile, tile, tile), 3)
            pg.draw.rect(screen, (0,255,0), (enemy["to_x"]*tile, enemy["to_y"]*tile, tile, tile), 3)
            screen.blit(pg.image.load(enemies_textures[0]), (enemy["x"]*tile, enemy["y"]*tile))

        # Draw player
        screen.blit(pg.image.load("assets/player/perso_d2.png"), (player[0]*tile, player[1]*tile))

        # Add grid (just for 16*16 rows)
        tiles = []
        for x in range(0, tile*game_size, tile):
            pg.draw.line(screen, (0,0,0), (x, 0), (x, tile*16))
            for y in range(0, tile*game_size, tile):
                pg.draw.line(screen, (0,0,0), (0, y), (tile*16, y))
                rect = pg.Rect(x, y, tile, tile)
                tiles.append(rect)

        if save_button.is_clicked():
            with open("data.json", "r+") as file:
                content = json.load(file)
                levels = content["levels"]
                for level in levels:
                    if level["id"] == idlevel:
                        level["background"] = background
                        level["objects"] = objects
                        level["items"] = items
                        level["enemy"] = enemies
                        level["player_coordinates"] = player
                file.seek(0) 
                json.dump(content, file)
                file.truncate()

        if back_button.is_clicked():
            game_status = "menu"
            main()

        pg.display.flip()


class Button():
    def __init__(self, image, x, y) -> None:
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_clicked(self):
        action = False

        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

    def get_width(self):
        return self.image.get_width()
    
    def get_position(self):
        return self.rect.x, self.rect.y

if __name__ == "__main__":
    main()
