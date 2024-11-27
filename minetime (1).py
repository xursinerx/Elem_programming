import random
import sweeperlib


state = {
    "field": []
}


def place_mines(minefield, tiles, mines):
    """
    Places N mines to a field in random tiles.
    """

    for _ in range(mines):
        usedtile = random.choice(tiles)
        x, y = usedtile
        minefield[y][x] = "x"
        tiles.remove(usedtile)


def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
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

    sweeperlib.draw_sprites()


def main():
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    sweeperlib.load_sprites("C:\\Users\\msinu\\OneDrive\\Documents\\GitHub\\Elem_programming\\sprites")
    #r"C:\Users\msinu\OneDrive\Documents\GitHub\Elem_programming\sprites"
    #"/home/ursa/Documents/coding/sprites"
    sweeperlib.create_window(600, 400)

    field = []
    for row in range(11):
        field.append([])
        for col in range(19):
            field[-1].append(" ")

    state["field"] = field

    available = []
    for x in range(19):
        for y in range(11):
            available.append((x, y))

    place_mines(field, available, 35)

    # state["field"] = field

    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.start()


if __name__ == "__main__":
    main()
