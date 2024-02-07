import pygame as pg
import json

# Variables
tile = 46
size_screen = 20
game_size = 16
screen_width = tile*size_screen
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
items_textures = ["assets/items/coin.png"]              

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

        for i in range(len(background_buttons)):
            if background_buttons[i].is_clicked():
                selected_background_layer = i
                pg.draw.rect(screen, (255,0,0), (screen_width-tile*4+i*tile, 150, tile, tile), 3)
                
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
