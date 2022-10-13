INFINITY = float("inf")
known_states = {}


def heuristic(state):
    tile_sum = 0
    tiles = 0
    for row in state:
        for col in row:
            if col != 0:
                tile_sum += col
                tiles += 1

    return tile_sum / tiles


def play_round(state):
    pass


def maximize(state, depth, maxdepth, alpha, beta, branch):
    pass


def minimize(state, depth, maxdepth, alpha, beta, branch):
    pass
