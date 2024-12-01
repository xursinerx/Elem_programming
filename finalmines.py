import random
import sweeperlib as lib
import math
import time

state = {
    "field": [],
    "field_2_see": [],
    "clicks": 0,
    "ending": 0,
    "unopened": 0,
    "flags": 0,
    "mines": 0,
    "height": 0,
    "width": 0,
    "time": 0,
    "time_2_see": 0,
}

font = "DejaVu Serif"


def game_time():
    """
    makes the time spent on the game more readable
    """
    minutes = math.floor(state["time"] / 60)
    seconds = state["time"] % 60

    if minutes == 0:
        state["time_2_see"] = f"{state["time"]}s"
    else:
        state["time_2_see"] = f"{minutes}min {seconds}s"


def game_time_handler(time):
    """
    such a complicated handler function for the interval function
    """
    state["time"] += 1


def place_mines(minefield, tiles, mines):
    """
    Randomize a specific amount of mines into the minefield
    """

    for _ in range(mines):
        usedtile = random.choice(tiles)
        x, y = usedtile
        minefield[y][x] = "x"
        tiles.remove(usedtile)
    state["field"] = minefield


def place_numbers(minefield, x, y):
    """
    Prepares the rest of the field by placing either numbers
    or empty tiles into the mineless tiles
    """
    # if something doesn't work then it's probably this
    # the tiles around the selected tiles
    neighbor = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

    mineamount = 0

    for i, j in neighbor:
        if 0 <= j < len(minefield) and 0 <= i < len(minefield[0]) and minefield[j][i] == "x":
            mineamount += 1

    if mineamount > 0:
        state["field"][y][x] = f"{mineamount}"
        if state["field_2_see"][y][x] != "f":
            state["field_2_see"][y][x] = f"{mineamount}"


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
            tile = state["field_2_see"][y][x]
            if tile == "x":
                lib.prepare_sprite("x", x * tile_size, y * tile_size)

            if tile == " ":
                lib.prepare_sprite(" ", x * tile_size, y * tile_size)

            if tile == "f":
                lib.prepare_sprite("f", x * tile_size, y * tile_size)

            for i in range(9):
                if tile == f"{i}":
                    lib.prepare_sprite(f"{i}", x * tile_size, y * tile_size)

    lib.draw_sprites()


def floodfill(minefield, x, y):
    """
    Opens the tiles that don't contain mines around the pressed tile
    """
    if x < 0 or x >= len(minefield[0]) or y < 0 or y >= len(minefield):
        return

    if minefield[y][x] == "x":
        return

    unknown_tiles = [(y, x)]
    visited = set()
    while unknown_tiles:
        tile = unknown_tiles.pop(0)
        ty, tx = tile

        if tile in visited:
            continue
        visited.add(tile)

        minefield[ty][tx] = "0"
        if state["field_2_see"][ty][tx] != "f":
            state["field_2_see"][ty][tx] = "0"

        for j in range(ty - 1, ty + 2 ):
            for i in range(tx - 1, tx + 2):
                if 0 <= j < len(minefield) and 0 <= i < len(minefield[0]) and (j, i) not in visited:
                    place_numbers(state["field"], i, j)
                    if minefield[j][i] == " ":
                        unknown_tiles.append((j, i))


def handle_mouse_start(x, y, button, modkey):
    """
    Handler function, needed to make it possible to mark flags
    and open mines without the wrong thing happening :p
    """
    buttons = {
        lib.MOUSE_LEFT: "left"
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
    draw_btn("start", 250, 340, 300, 80, (200, 255, 200, 255), 345, 357)

    # stat button
    draw_btn("stat", 250, 240, 300, 80, (200, 200, 255, 255), 345, 257)

    # quit button
    draw_btn("quit", 250, 140, 300, 80, (255, 200, 200, 255), 350, 157)

    lib.draw_sprites()


def start_menu():
    """
    Opens the start menu
    """
    lib.create_window()
    lib.set_draw_handler(start_menu_draw)
    lib.set_mouse_handler(handle_mouse_start)
    lib.start()


def handle_mouse_stats(x, y, button, modkey):
    """
    handles the mouse in the stats screen
    """
    buttons = {
        lib.MOUSE_LEFT: "left"
    }

    btn_name = buttons.get(button, "")
    if btn_name == "left":
        if y in range(550, 600):
            if x in range(0, 150):
                start_menu()


def stats_draw():
    """
    prepares the stats screen
    """
    lib.clear_window()
    lib.draw_background()
    draw_btn("<---", 0, 550, 150, 50, (135,206,250,255), 20, 555)
    draw_btn(" ", 0, 470, 1300, 30, (135,206,250,255), 0, 0)

    with open("stats.txt", "r") as file:
        lines = file.readlines()

    x, y = 20, 470 - 50
    spacing = 30

    for line in lines:
        lib.draw_text(line, x, y, font=font, size=15)
        y -= spacing

    lib.draw_sprites()


def stats():
    """
    Holds the record of the games played before;
    the difficulty level, date, time and if the user won
    """
    lib.create_window(width=1300)
    lib.set_draw_handler(stats_draw)
    lib.set_mouse_handler(handle_mouse_stats)
    lib.start()


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
        lib.MOUSE_LEFT: "left"
    }

    btn_name = buttons.get(button, "")
    if btn_name == "left":
        if y in range(316, 566):
            if x in range(33, 383):
                state["height"] = 9
                state["width"] = 9
                state["mines"] = 10

        if y in range(316, 566):
            if x in range(416, 766):
                state["height"] = 15
                state["width"] = 9
                state["mines"] = 20

        if y in range(33, 283):
            if x in range(33, 383):
                state["height"] = 15
                state["width"] = 15
                state["mines"] = 55

        if y in range(33, 283):
            if x in range(416, 766):
                state["height"] = 17
                state["width"] = 34
                state["mines"] = 170
        game_screen(state["width"], state["height"], state["mines"])


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
        lib.MOUSE_RIGHT: "right"
    }

    field = state["field"]

    btn_name = buttons.get(button, "")
    x_coord = math.ceil(x / 40) - 1
    y_coord = math.ceil(y / 40) - 1

    if 0 <= x_coord < len(field[0]) and 0 <= y_coord < len(field):
        if btn_name == "left":
            state["clicks"] += 1
#           if field == state["field_2_see"]:
#                lib.set_draw_handler(draw_field)
            if field[y_coord][x_coord] == "x":
                state["ending"] = "lost"
                to_stats()
                lose()
            elif field[y_coord][x_coord] != "x" and state["field_2_see"][y_coord][x_coord] != "f":
                place_numbers(field, x_coord, y_coord)
                floodfill(field, x_coord, y_coord)
                lib.set_draw_handler(draw_field)

        if btn_name =="right":
            state["clicks"] += 1
            if field == state["field_2_see"]:
                lib.set_draw_handler(draw_field)
            elif state["field_2_see"][y_coord][x_coord] == "f":
                state["field_2_see"][y_coord][x_coord] = " "
                lib.set_draw_handler(draw_field)
                state["flags"] -= 1
            elif state["field_2_see"][y_coord][x_coord] == " ":
                state["field_2_see"][y_coord][x_coord] = "f"
                lib.set_draw_handler(draw_field)
                state["flags"] += 1

    check_win()


def win_screen_draw():
    """
    prepares the winning screen for drawing
    """
    lib.clear_window()
    lib.draw_background()
    lib.draw_text("YOU WIN!", 250, 500, (0, 0, 0, 255), font, 36)
    lib.draw_text(f"You found {state["mines"]} mines from a {state["width"]}x{state["height"]} field", 40, 400, (0, 0, 0, 255), font, 30)
    draw_btn("To start menu", 225, 250, 350, 80, (255, 255, 255, 200), 260, 265, size=30)
    draw_btn("To stats", 225, 150, 350, 80, (255, 255, 255, 200), 315, 165, size=30)
    lib.draw_sprites()


def handle_mouse_result(x, y, button, modkey):
    """
    handles the mouse in both result screens
    """
    buttons = {
        lib.MOUSE_LEFT: "left",
    }

    btn_name = buttons.get(button, "")
    if btn_name == "left":
        if y in range(250, 330):
            if x in range(225, 575):
                start_menu()

        if y in range(150, 230):
            if x in range(225, 575):
                stats()


def to_stats():
    """
    saves the statistic of the game to a stats file
    """
    game_time()
    current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    try:
        with open("stats.txt", "a") as file:
            file.write(f"{current_time}: Game time: {state["time_2_see"]}, minefield size: {state["width"]}x{state["height"]}, "
                       f"there were {state["mines"]} mines, you clicked {state["clicks"]} times and you {state["ending"]}!\n")
    except IOError:
        print("Saving failed, where are trying to save these stats?")


def win():
    """
    Shows the player the beautiful green screen of victory,
    congrats
    """
    lib.create_window(bg_color=(11, 218, 81, 255))
    lib.set_draw_handler(win_screen_draw)
    lib.set_mouse_handler(handle_mouse_result)
    lib.start()


def check_win():
    """
    Checks after each click if the player has won the game
    """
    unopened = sum(row.count(" ") for row in state["field_2_see"])
    flagged_correctly = sum(
        1 for y in range(len(state["field"]))
        for x in range(len(state["field"][0]))
        if state["field_2_see"][y][x] == "f" and state["field"][y][x] == "x"
    )
    if flagged_correctly == state["mines"] and unopened == 0:
        state["ending"] = "won"
        to_stats()
        win()


def lose_screen_draw():
    """
    Prepares the losing screen to be drawn
    """
    lib.clear_window()
    lib.draw_background()
    lib.draw_text("YOU LOSE!", 250, 500, (0, 0, 0, 255), font, 36)
    lib.draw_text("You stepped on a mine :(", 160, 400, (0, 0, 0, 255), font, 30)
    draw_btn("To start menu", 225, 250, 350, 80, (255, 255, 255, 200), 260, 265, size=30)
    draw_btn("To stats", 225, 150, 350, 80, (255, 255, 255, 200), 315, 165, size=30)
    lib.draw_sprites()



def lose():
    """
    Shows the user the red losing screen.
    shouldn't have lost...
    """
    lib.create_window(bg_color=(220,20,60,255))
    lib.set_draw_handler(lose_screen_draw)
    lib.set_mouse_handler(handle_mouse_result)
    lib.start()


def game_screen(x, y, mines):
    """
    As the name says, the game screen. This will hopefully show
    the awesome, groundbreaking, never seen before minesweeper
    """
    field = []
    field_2_see = []
    for row in range(y):
        field.append([])
        field_2_see.append([])
        for col in range(x):
            field[-1].append(" ")
            field_2_see[-1].append(" ")

    state["field"] = field
    state["field_2_see"] = field_2_see
    # state["x_tiles"] = len(field[0])
    # state["y_tiles"] = len(field)

    available = []
    for i in range(x):
        for j in range(y):
            available.append((i, j))

    place_mines(field, available, mines)

    lib.resize_window(x * 40, y * 40)
    lib.load_sprites("sprites")
    lib.set_draw_handler(draw_field)
    lib.set_mouse_handler(handle_mouse_game)
    lib.set_interval_handler(game_time_handler)
    lib.start()


start_menu()
