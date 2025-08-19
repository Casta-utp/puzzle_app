# Heurísticas adaptadas para laberinto
def maze_manhattan_distance(state, goal):
    return abs(state.position[0] - goal.position[0]) + abs(state.position[1] - goal.position[1])

def maze_euclidean_distance(state, goal):
    dx = state.position[0] - goal.position[0]
    dy = state.position[1] - goal.position[1]
    return (dx*dx + dy*dy) ** 0.5

def maze_chebyshev_distance(state, goal):
    return max(abs(state.position[0] - goal.position[0]), abs(state.position[1] - goal.position[1]))