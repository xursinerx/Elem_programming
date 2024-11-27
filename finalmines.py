import random
import sweeperlib as lib

state = {
    "field": []
}


def place_mines(minefield, tiles, mines):
    """
    Randomize a specific amount of mines into the minefield
    """

    for _ in range(mines):
        usedtile = random.choice(tiles)
        x, y = usedtile
        minefield[y][x] = "x"
        tiles.remove(usedtile)


def place_numbers(minefield):
    """
    Prepares the rest of the field by placing either numbers
    or empty tiles into the mineless tiles
    """
    # if something doesn't work then it's probably this
    # viereiset laatat:
    neighbor = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for y, row in enumerate(minefield):
        for x, tile in enumerate(minefield[0]):
            if tile == "x":
                continue
            
            mineamount = 0
            for j, i in neighbor:
                y_j, x_i = y + j, x + i
                if 0 <= y_j < len(minefield) and 0 <= x_i < len(minefield[0]) and minefield[y_j][x_i] == "x":
                    mineamount += 1
            minefield[y][x] = str(mineamount)
    return minefield


def draw_field():
    """
    A handler function for drawing the two-dimensional list - will be called
    whenever a screen update is needed.
    """
    tile_size = 40
    # for sprites
    field = state["field"]

    lib.clear_window()
    lib.draw_background()

    for y, row in enumerate(field):
        for x, column in enumerate(row):
            tile = field[y][x]

            if tile == "x":
                lib.prepare_sprite("x", x * tile_size, y * tile_size)

            if tile == " ":
                lib.prepare_sprite(" ", x * tile_size, y * tile_size)
            
            if tile == "f":
                lib.prepare_sprite("f", x * tile_size, y * tile_size)
            
            # en oo tästä seuraavasta ny varma sos
            for i in range(9):
                if tile == "{i}":
                    lib.prepare_sprite("{i}", x * tile_size, y * tile_size)

    lib.draw_sprites()


def starting_field(minefield, x, y):
    """
    Hides all tiles at the beginning of the game
    """
    
    hidden_tiles = (y, x)
    for j in range(hidden_tiles[0] - 1, hidden_tiles[0] + 2):
        for i in range(hidden_tiles[1] - 1, hidden_tiles[1] + 2):
            minefield[y][x] = " "


def floodfill(minefield, x, y):
    """
    Opens the tiles that don't contain mines around the pressed tile
    """
    if x < 0 or x >= len(minefield[0]) or y < 0 or y >= len(minefield):
        return

    if minefield[y][x] == "x":
        return

    unknown_tiles = [(y, x)]
    while True:
        tile = unknown_tiles.pop(0)
        minefield[tile[0]][tile[1]] = "0"

        for j in range(tile[0] - 1, tile[0] + 2):
            for i in range(tile[1] - 1, tile[1] + 2):
                rows = len(minefield) - 1
                columns = len(minefield[0]) - 1
                if 0 <= y <= rows and 0 <= x <= columns:
                    if minefield[j][i] == "x":
                        continue
                    if minefield[j][i] != " " and (j, i) not in unknown_tiles:
                        unknown_tiles.append((j, i))
        if len(unknown_tiles) == 0:
            break
    state["field"] = minefield


def handle_mouse(x, y, button, modkey):
    """
    Handler function, needed to make it possible to mark flags
    and open mines without the wrong thing happening :p
    """
    buttons = {
        lib.MOUSE_LEFT: "left",
        lib.MOUSE_MIDDLE: "middle",
        lib.MOUSE_RIGHT: "right"
    }
    # buttonname = buttons.get(button, "")
    # mitää bittua nyt taasss??? vittuuuuu auttakaa jo
    btn_location = [(y, x)]
    btn_name = buttons.get(button, "")
    return btn_location, btn_name

 
def draw_btn(name, x, y, width, height, color, txt_x, txt_y, txt_color=(0, 0, 0, 255), font="serif", size=32):
    """
    makes creating buttons a little bit easier
    """
    lib.prepare_rectangle(x, y, width, height, color)
    lib.draw_text(name, txt_x, txt_y, txt_color, font, size)


def start_menu():
    """
    Creates the start menu at the beginning, will contain three buttons
    for either looking at the past games, quitting and starting a new game
    """
    lib.create_window()
    # lib.set_mouse_handler(handle_mouse)

    # name of the game duh
    lib.draw_text("Minesweeper", 48, 200, (0, 0, 0, 255), "serif", 64)

    # start button
    draw_btn("start", 250, 340, 300, 80, (255, 240, 240, 255), 320, 364)

    # stat button
    draw_btn("stat", 250, 440, 300, 80, (240, 255, 240, 255), 320, 464)

    # quit button
    draw_btn("quit", 250, 540, 300, 80, (240, 240, 255, 255), 320, 564)

    lib.start()


def stats():
    """
    Holds the record of the games played before;
    the difficulty level and if the user won the game
    """
    lib.clear_window()


def game_menu():
    """
    Holds four options for game difficulties:
    easy, normal, hard and crazy
    each of them will have a different size and amount of mines
    """
    lib.clear_window()
    # easy, 10 mines
    draw_btn("easy", 100, 250, 250, 150, (255, 240, 240, 255), 205, 155, size=30)
    lib.draw_text("9x9", 220, 190, (0, 0, 0, 255), "serif", 27)

    # normal, 20 mines
    draw_btn("normal", 450, 250, 250, 150, (255, 240, 240, 255), 540, 155, size=30)
    lib.draw_text("9x15", 565, 190, (0, 0, 0, 255), "serif", 27)

    # hard, 75 mines
    draw_btn("hard", 100, 700, 250, 150, (255, 240, 240, 255), 205, 605, size=30)
    lib.draw_text("15x25", 220, 640, (0, 0, 0, 255), "serif", 27)

    # crazy, 155 mines
    draw_btn("crazy", 450, 700, 250, 150, (255, 240, 240, 255), 540, 605, size=30)
    lib.draw_text("25x25", 565, 640, (0, 0, 0, 255), "serif", 27)


def game_screen(x, y, mines):
    """
    As the name says, the game screen. This will hopefully show
    the awesome, groundbreaking, never seen before minesweeper
    """
    lib.clear_window()
    lib.resize_window(x + 80, y + 80)
    lib.load_sprites(r"C:\Users\msinu\OneDrive\Documents\GitHub\Elem_programming\sprites")
    # r"C:\Users\msinu\OneDrive\Documents\GitHub\Elem_programming\sprites"
    # "/home/ursa/Documents/coding/sprites"

    field = []
    for row in range(y):
        field.append([])
        for col in range(x):
            field[-1].append(" ")

    state["field"] = field

    available = []
    for i in range(x):
        for j in range(y):
            available.append((i, j))

    place_mines(field, available, mines)
    place_numbers(field)
    starting_field(field, x, y)
    lib.set_draw_handler(draw_field)


start_menu()
#if button clicked in sun perse:
#    lib.close()
#if button clicked in mun perse:
#    game_menu()
#if button clicked in sun mutsis:
#    stats()

#lib.set_mouse_handler(handle_mouse)
#if enumerate(btn_location) in range(mutsis)
#mitä paskaa mitä vittuauaaa
