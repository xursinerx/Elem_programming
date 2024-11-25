import sweeperlib

state = {
    "planet": []
}


def floodfill(planet1, x1, y1):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """
    if x1 < 0 or x1 >= len(planet1[0]) or y1 < 0 or y1 >= len(planet1):
        return

    if planet1[y1][x1] == "x":
        return

    unknown_tiles = [(y1, x1)]
    while True:
        tile = unknown_tiles.pop(0)
        planet1[tile[0]][tile[1]] = "0"

        for y in range(tile[0] - 1, tile[0] + 2):
            for x in range(tile[1] - 1, tile[1] + 2):
                rows = len(planet1) - 1
                columns = len(planet1[0]) - 1
                if 0 <= y <= rows and 0 <= x <= columns:
                    if planet1[y][x] == "x":
                        continue
                    if planet1[y][x] != "0" and (y, x) not in unknown_tiles:
                        unknown_tiles.append((y, x))
        if len(unknown_tiles) == 0:
            break
    state["planet"] = planet1


def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    tile_size = 40
    # for sprites
    planeetta = state["planet"]

    sweeperlib.clear_window()
    sweeperlib.draw_background()

    for y, row in enumerate(planeetta):
        for x, column in enumerate(row):
            tile = planeetta[y][x]

            flipped = len(planeetta) - y - 1
            # picture is flipped for some reason

            if tile == "x":
                sweeperlib.prepare_sprite("x", x * tile_size, flipped * tile_size)

            if tile == "0":
                sweeperlib.prepare_sprite(" ", x * tile_size, flipped * tile_size)

    sweeperlib.draw_sprites()


def main(planeetta):
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    sweeperlib.load_sprites("/home/ursa/Documents/progrexer/minesweeper/sprites")

    sweeperlib.create_window(len(planet[0]) * 40, len(planet) * 40)

    state["planet"] = planeetta

    floodfill(planeetta, 3, 13)

    # state["field"] = field

    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.start()


planet = [
    [" ", " ", "x", "x", " ", " ", " ", "x", " ", " ", " ", "x", " "],
    [" ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x", " "],
    [" ", "x", "x", " ", " ", " ", " ", "x", " ", " ", "x", "x", " "],
    ["x", "x", "x", "x", "x", " ", " ", "x", " ", "x", " ", " ", " "],
    ["x", "x", "x", "x", " ", " ", " ", " ", "x", " ", "x", " ", " "],
    [" ", " ", "x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " "]
]


if __name__ == "__main__":
    main(planet)
