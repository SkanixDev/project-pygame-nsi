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


background_textures = ["assets/backgrounds/fond_2.png",
                "assets/backgrounds/fond_1.png"]
objects_textures = ["assets/objects/vide.png",
                "assets/objects/obsatcle_1.png"]
items_textures = ["assets/objects/pierre_1.png"]              
enemies_textures = ["assets/enemies/black_fly.png"]

# Text 
font = pg.font.Font(None, 36)

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

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if create_level_button.is_clicked():
            game_status = "editor"


        if game_status == "editor":
            editor()


        pg.display.flip()

    pg.quit()

def editor():
    global game_status
    global running
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

    # Layer button
    background = [
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
    ]
    objects = [
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
    ]
    items = []
    enemy= []

    # Add text section
    title_section_layer = font.render("Couches", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 50))

    selected_layer = 0 # 0: background 1: object 

    # add all backgrounds button
    title_section_layer = font.render("Fonds", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 90))

    background_buttons = []
    selected_background_layer = 0
    for i in range(len(background_textures)):
        background_buttons.append(Button(background_textures[i], screen_width-tile*4+i*tile, 150))
        background_buttons[i].draw()
        if selected_background_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 150, tile, tile), 3)

    # add all objects button
    title_section_layer = font.render("Objets", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 300))

    objects_buttons = []
    selected_objects_layer = 0
    for i in range(len(objects_textures)):
        objects_buttons.append(Button(objects_textures[i], screen_width-tile*4+i*tile, 350))
        objects_buttons[i].draw()
        if selected_objects_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 350, tile, tile), 3)

    # add all items button
    title_section_layer = font.render("Items", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 500))

    items_buttons = []
    selected_items_layer = 0
    for i in range(len(items_textures)):
        items_buttons.append(Button(items_textures[i], screen_width-tile*4+i*tile, 550))
        items_buttons[i].draw()
        if selected_items_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 550, tile, tile), 3)

    # add all enemies button
    title_section_layer = font.render("Ennemis", True, (0,0,0))
    screen.blit(title_section_layer, (screen_width-tile*4, 700))

    enemies_buttons = []
    selected_enemies_layer = 0
    for i in range(len(enemies_textures)):
        enemies_buttons.append(Button(enemies_textures[i], screen_width-tile*4+i*tile, 750))
        enemies_buttons[i].draw()
        if selected_enemies_layer == i:
            pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 750, tile, tile), 3)

    # add collision for each tile
    background_tiles_editor = []
    for x in range(0, tile*game_size, tile):
        for y in range(0, tile*game_size, tile):
            rect = pg.Rect(x, y, tile, tile)
            background_tiles_editor.append(rect)    

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Choice background
        for i in range(len(background_buttons)):
            if background_buttons[i].is_clicked():
                selected_background_layer = i
                selected_layer = 0
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 150, tile, tile), 3)
                for j in range(len(background_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+j*tile, 150, tile, tile), 3)

        # Choice objects
        for i in range(len(objects_buttons)):
            if objects_buttons[i].is_clicked():
                selected_objects_layer = i
                selected_layer = 1
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 350, tile, tile), 3)
                for j in range(len(objects_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+j*tile, 350, tile, tile), 3)

        # Choice items
        for i in range(len(items_buttons)):
            if items_buttons[i].is_clicked():
                selected_items_layer = i
                selected_layer = 2
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 550, tile, tile), 3)
                for j in range(len(items_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+j*tile, 550, tile, tile), 3)

        # Choice enemies
        for i in range(len(enemies_buttons)):
            if enemies_buttons[i].is_clicked():
                selected_enemies_layer = i
                selected_layer = 3
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 750, tile, tile), 3)
                for j in range(len(enemies_buttons)):    
                    if j != i:
                        pg.draw.rect(screen, (200,200,200), (screen_width-tile*4+j*tile, 750, tile, tile), 3)
        

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
                                "y": y
                            })
                        else:
                            items = [item for item in items if not (item["x"] == x and item["y"] == y)]
        
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

        # Add grid (just for 16*16 rows)
        tiles = []
        for x in range(0, tile*game_size, tile):
            pg.draw.line(screen, (0,0,0), (x, 0), (x, tile*16))
            for y in range(0, tile*game_size, tile):
                pg.draw.line(screen, (0,0,0), (0, y), (tile*16, y))
                rect = pg.Rect(x, y, tile, tile)
                tiles.append(rect)

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

if __name__ == "__main__":
    main()
