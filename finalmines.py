import random
import sweeperlib as lib
import math

state = {
    "field": [],
    "field_2_see": []
}

font = "Microsoft Sans Serif"


def place_mines(minefield, tiles, mines):
    """
    Randomize a specific amount of mines into the minefield
    """

    for _ in range(mines):
        usedtile = random.choice(tiles)
        x, y = usedtile
        minefield[y][x] = "x"
        tiles.remove(usedtile)
    return minefield


def place_numbers(minefield):
    """
    Prepares the rest of the field by placing either numbers
    or empty tiles into the mineless tiles
    """
    # if something doesn't work then it's probably this
    # the tiles around the selected tiles
    neighbor = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for y, row in enumerate(minefield):
        for x, tile in enumerate(minefield[y]):
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

    lib.clear_window()
    lib.draw_background()
    for y in range(len(state["field"])):
        for x in range(len(state["field"][0])):
            lib.prepare_sprite(state["field_2_show"][y][x], y * tile_size, x * tile_size)

    lib.draw_sprites()


def starting_field(hidden_field):
    """
    Hides all tiles at the beginning of the game
    """
    for j, row in enumerate(hidden_field):
        for i, tile in enumerate(row):
            hidden_field[j][i] = " "
    return hidden_field


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


def handle_mouse_start(x, y, button, modkey):
    """
    Handler function, needed to make it possible to mark flags
    and open mines without the wrong thing happening :p
    """
    buttons = {
        lib.MOUSE_LEFT: "left",
        lib.MOUSE_MIDDLE: "middle",
        lib.MOUSE_RIGHT: "right"
    }
    
    btn_name = buttons.get(button, "")
    if btn_name == "left":
        if y in range(340, 420):
            if x in range(250, 550):
                game_menu()
        if y in range(240, 320):
            if x in range(250, 550):
                stats()
        if y in range(140, 220):
            if x in range(250, 550):
                lib.close()

 
def draw_btn(name, x, y, width, height, color, txt_x, txt_y, txt_color=(0, 0, 0, 255), size=32):
    """
    makes creating buttons a bit easier
    """
    lib.prepare_rectangle(x, y, width, height, color)
    lib.draw_text(name, txt_x, txt_y, txt_color, font, size)


def start_menu_draw():
    """
    Prepares the buttons for start menu
    """
    lib.clear_window()
    lib.draw_background()
    # name of the game duh
    lib.draw_text("Minesweeper", 250, 500, (0, 0, 0, 255), font, 36)

    # start button
    draw_btn("start", 250, 340, 300, 80, (200, 255, 200, 255), 345, 357, font)

    # stat button
    draw_btn("stat", 250, 240, 300, 80, (200, 200, 255, 255), 345, 257, font)

    # quit button
    draw_btn("quit", 250, 140, 300, 80, (255, 200, 200, 255), 350, 157, font)

    lib.draw_sprites()


def start_menu():
    """
    Opens the start menu
    """
    lib.create_window()
    lib.set_draw_handler(start_menu_draw)
    lib.set_mouse_handler(handle_mouse_start)
    lib.start()


def stats():
    """
    Holds the record of the games played before;
    the difficulty level and if the user won the game
    """
    lib.clear_window()


def game_menu_draw():
    """
    Prepares buttons for the game menu
    """
    lib.clear_window()
    lib.draw_background()
    # easy, 10 mines
    draw_btn("easy (10)", 33, 316, 350, 250, (200, 255, 200, 255), 135, 440, size=30)
    lib.draw_text("9x9", 170, 400, (0, 0, 0, 255), font, 27)

    # normal, 20 mines
    draw_btn("normal (20)", 416, 316, 350, 250, (200, 200, 255, 255), 500, 440, size=30)
    lib.draw_text("9x15", 543, 400, (0, 0, 0, 255), font, 27)

    # hard, 55 mines
    draw_btn("hard (55)", 33, 33, 350, 250, (255, 200, 200, 255), 135, 157, size=30)
    lib.draw_text("15x15", 150, 117, (0, 0, 0, 255), font, 27)

    # crazy, 170 mines
    draw_btn("crazy (170)", 416, 33, 350, 250, (255, 150, 150, 255), 500, 157, size=30)
    lib.draw_text("34x17", 543, 117, (0, 0, 0, 255), font, 27)

    lib.draw_sprites()


def handle_mouse_game_menu(x, y, button, modkey):
    """
    Handles the mouse in the game menu
    """
    buttons = {
        lib.MOUSE_LEFT: "left",
        lib.MOUSE_MIDDLE: "middle",
        lib.MOUSE_RIGHT: "right"
    }

    btn_name = buttons.get(button, "")
    if btn_name == "left":
        if y in range(316, 566):
            if x in range(33, 383):
                game_screen(9, 9, 10)
        if y in range(316, 566):
            if x in range(416, 766):
                game_screen(9, 15, 20)
        if y in range(33, 283):
            if x in range(33, 383):
                game_screen(15, 15, 55)
        if y in range(33, 283):
            if x in range(416, 766):
                game_screen(34, 17, 170)


def game_menu():
    """
    Holds four options for game difficulties:
    easy, normal, hard and crazy
    each of them will have a different size and amount of mines
    """
    lib.create_window()
    lib.set_draw_handler(game_menu_draw)
    lib.set_mouse_handler(handle_mouse_game_menu)
    lib.start()


def handle_mouse_game(x, y, button, modkey):
    """
    Handles the mouse in the game
    """
    buttons = {
        lib.MOUSE_LEFT: "left",
        lib.MOUSE_MIDDLE: "middle",
        lib.MOUSE_RIGHT: "right"
    }

    field = state["field"]

    btn_name = buttons.get(button, "")
    x_coord = math.ceil(x / 40) - 1
    y_coord = math.ceil(y / 40) - 1
    if btn_name == "left":
        if field[y_coord][x_coord] == "x":
            print("MINE, close it")
            lib.close()
        else:
            floodfill(field, x_coord, y_coord)
            lib.set_draw_handler(draw_field)


def game_screen(x, y, mines):
    """
    As the name says, the game screen. This will hopefully show
    the awesome, groundbreaking, never seen before minesweeper
    """
    lib.clear_window()
    lib.resize_window(x * 40, y * 40)
    lib.load_sprites("/home/ursa/Documents/Elem_programming/sprites")
    # "C:\\Users\\msinu\\OneDrive\\Documents\\GitHub\\Elem_programming\\sprites"
    # "/home/ursa/Documents/Elem_programming/sprites"

    field = []
    for row in range(y):
        field.append([])
        for col in range(x):
            field[-1].append(" ")

    state["field"] = field
    state["x_tiles"] = len(field[0])
    state["y_tiles"] = len(field)

    available = []
    for i in range(x):
        for j in range(y):
            available.append((i, j))

    field = place_mines(field, available, mines)
    field = place_numbers(field)
    # starting_field(field, x, y)
    lib.set_draw_handler(draw_field)
    lib.set_mouse_handler(handle_mouse_game)
    lib.start()


start_menu()
