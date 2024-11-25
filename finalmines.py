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

def draw_field():
    """
    A handler function for drawing the two-dimensional list - will be called
    whenever a screen update is needed.
    """
    tile_size = 40
    # for sprites
    field = state["field"]

    sweeperlib.clear_window()
    sweeperlib.draw_background()

    for y, row in enumerate(field):
        for x, column in enumerate(row):
            tile = field[y][x]

            if tile == "x":
                sweeperlib.prepare_sprite("x", x * tile_size, y * tile_size)

            if tile == " ":
                sweeperlib.prepare_sprite(" ", x * tile_size, y * tile_size)
            
            if tile == "f":
                sweeperlib.prepare_sprite("f", x * tile_size, y * tile_size)

    sweeperlib.draw_sprites()