def get_empty_uniques(grid):
    topmost = len(grid) - 1
    bottommost = 0
    leftmost = len(grid[0]) - 1
    rightmost = 0

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] != 0:
                if x < topmost:
                    topmost = x
                if x > bottommost:
                    bottommost = x
                if y < leftmost:
                    leftmost = y
                if y > rightmost:
                    rightmost = y

    # print(f"topmost: {topmost}\nbottommost: {bottommost}\nleftmost: {leftmost}\nrightmost: {rightmost}")

    topleft_empty = (topmost - 1, leftmost - 1)
    bottomleft_empty = (bottommost + 1, leftmost - 1)
    topright_empty = (topmost - 1, rightmost + 1)
    bottomright_empty = (bottommost + 1, rightmost + 1)

    empty_slots = [topleft_empty, bottomleft_empty, topright_empty, bottomright_empty]

    # print(f"Going over vertical, rows from {topmost} to {bottommost}")
    # print(f"   Columns from 0 to {leftmost - 1}")
    for x in range(topmost, bottommost + 1):
        for y in range(0, leftmost):
            print(f"{x},{y}")
            empty_slots.append((x, y))

    # print("Going over horizontal")
    for x in range(4):
        for y in range(leftmost, rightmost + 1):
            if grid[x][y] == 0:
                print(f"{x},{y}")
                empty_slots.append((x, y))

    constrained_empty_slots = []

    for slot in empty_slots:
        if slot[0] < len(grid) and slot[1] < len(grid[0]):
            constrained_empty_slots.append(slot)

    return constrained_empty_slots


grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2], [0, 0, 2, 4]]
print(get_empty_uniques(grid))
