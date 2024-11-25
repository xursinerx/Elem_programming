import sweeperlib as lib

def handle_mouse(x, y, button, modkey):
    """
    This function is called when a mouse button is clicked inside the game window.
    Prints the position and clicked button of the mouse to the terminal.
    """
    buttons = {
        lib.MOUSE_LEFT: "left",
        lib.MOUSE_MIDDLE: "middle",
        lib.MOUSE_RIGHT: "right"
    }
    buttonname = buttons.get(button, "")
    print(f"The {buttonname} mouse button was pressed at {x}, {y}")

def main():
    """
    Creates a game window and sets a handler for mouse clicks.
    Starts the game.
    """
    lib.create_window()
    lib.set_mouse_handler(handle_mouse)
    lib.start()

if __name__ == "__main__":
    main()
