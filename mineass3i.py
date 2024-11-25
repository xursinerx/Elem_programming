def count_ninjas(initial_x, initial_y, init_room):
    """
    Counts the ninjas surrounding one tile in the given room and
    returns the result. The function assumes the selected tile does
    not have a ninja in it - if it does, it counts that one as well.
    """
    ninjas = 0
    #print("len(init_room): ", len(init_room))
    #print("len(init_room[0])): ", len(init_room[0]))
    #rows = len(room) - 1
    #columns = len(room[0]) - 1
    luku1 = initial_x - 1
    luku2 = initial_x + 2
    luku1y = initial_y - 1
    luku2y = initial_y + 2
    
    #print("kalakukko: ", room[initial_y][initial_x])
    #print("rows: ", rows, "columns: ", columns, "luku1: ", luku1, "luku2: ", luku2, "luku1y: ", luku1y, "luku2y: ", luku2y)
    
    for y in range(luku1y, luku2y):
        for x in range(luku1, luku2):
            rows = len(init_room) - 1
            columns = len(init_room[0]) - 1
            if 0 <= y <= rows and 0 <= x <= columns:
                ninjas += (init_room[y][x] == 'N')
    return ninjas

room = [
    ['N', ' ', ' ', ' ', ' '],
    ['N', 'N', 'N', 'N', ' '],
    ['N', ' ', 'N', ' ', ' '],
    ['N', 'N', 'N', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ']
]

print(" ", "- " * 5)
for row in room:
    print("|", " ".join(row), "|")
print(" ", "- " * 5)

user_x = int(input("Input x coordinate: "))
user_y = int(input("Input y coordinate: "))

ninjas_around = count_ninjas(user_x, user_y, room)
print(f"The tile is surrounded by {ninjas_around} ninjas")
