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
    #if something doesn't work then it's probably this
    #viereiset laatat:
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

    tiles = [(y, x)]
    for j in range(tiles[0] - 1, tiles[0] + 2):
        for i in range(tiles[1] - 1, tiles[1] + 2):
            for y_j in range(j - 1, j + 2):
                for x_i in range(i - 1, i + 2):
                    rows = len(minefield) - 1
                    columns = len(minefield[0]) - 1
                    if 0 <= y_j <= rows and 0 <= x_i <= columns:
                        mineamount += (minefield[y_j][x_i] == "x")
                        tiles[j][i] = mineamount

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
            
            #en oo tästä seuraavasta ny varma sos
            for i in range(9):
                if tile == "{i}":
                    lib.prepare_sprite("{i}", x * tile_size, y * tile_size)

    lib.draw_sprites()

def startingfield(minefield, x, y):
    """
    Hides all tiles at the beginning of the game
    """
    
    hidden_tiles = [(y, x)]
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
    #buttonname = buttons.get(button, "")
    #mitää bittua nyt taasss???
    return buttons.get(button, "")

def start_menu():
    """
    Creates the start menu at the beginning, will contain three buttons
    for either looking at the past games, quitting and starting a new game
    """
    lib.create_window()
    lib.set_mouse_handler(handle_mouse)

    #name of the game duh
    lib.draw_text("Minesweeper", 48, 200, (0, 0, 0, 255), "serif", 64)

    #start button
    lib.prepare_rectangle(250, 340, 300, 80, (255, 240, 240, 255))
    lib.draw_text("start", 320, 364)

    #stat button
    lib.prepare_rectangle(250, 340, 300, 80, (240, 255, 240, 255))
    lib.draw_text("stats", 320, 464)

    #quit button
    lib.prepare_rectangle(250, 340, 300, 80, (240, 240, 255, 255))
    lib.draw_text("quit", 336, 564)

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
    #easy
    lib.prepare_rectangle(100, 250, 250, 150, (255, 240, 240, 255))
    lib.draw_text("easy", 205, 155, (0, 0, 0, 255), "serif", 30)
    lib.draw_text("9x9", 220, 190, (0, 0, 0, 255), "serif", 27)
    #normal
    lib.prepare_rectangle(450, 250, 250, 150, (255, 240, 240, 255))
    lib.draw_text("normal", 540, 155, (0, 0, 0, 255), "serif", 30)
    lib.draw_text("9x15", 565, 190, (0, 0, 0, 255), "serif", 27)
    #hard
    lib.prepare_rectangle(100, 700, 250, 150, (255, 240, 240, 255))
    lib.draw_text("hard", 205, 605, (0, 0, 0, 255), "serif", 30)
    lib.draw_text("15x25", 220, 640, (0, 0, 0, 255), "serif", 27)
    #crazy
    lib.prepare_rectangle(450, 700, 250, 150, (255, 240, 240, 255))
    lib.draw_text("crazy", 540, 605, (0, 0, 0, 255), "serif", 30)
    lib.draw_text("25x25", 565, 640, (0, 0, 0, 255), "serif", 27)

def game_screen(x, y, mines):
    lib.clear_window()
    lib.resize_window(x + 80, y + 80)
    lib.load_sprites(r"C:\Users\msinu\OneDrive\Documents\GitHub\Elem_programming\sprites")

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
#maybebaby tähän alan rakentamaan tota pelin toimintaa? perchance...?
 