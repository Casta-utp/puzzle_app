from puzzle.state import PuzzleState

# Heurísticas
def manhattan_distance(state, goal):
    distance = 0
    goal_positions = {}
    
    # Mapear posiciones objetivo
    for i in range(3):
        for j in range(3):
            goal_positions[goal.board[i][j]] = (i, j)
    
    # Calcular distancia Manhattan
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0:
                goal_i, goal_j = goal_positions[state.board[i][j]]
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance

def misplaced_tiles(state, goal):
    count = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0 and state.board[i][j] != goal.board[i][j]:
                count += 1
    return count

def linear_conflict(state, goal):
    # Primero: distancia Manhattan
    distance = manhattan_distance(state, goal)
    
    # Construir mapa de posiciones objetivo
    goal_positions = {}
    for i in range(3):
        for j in range(3):
            goal_positions[goal.board[i][j]] = (i, j)
    
    # Revisar conflictos lineales en filas
    for row in range(3):
        tiles_in_row = [tile for tile in state.board[row] if tile != 0]
        for i in range(len(tiles_in_row)):
            for j in range(i + 1, len(tiles_in_row)):
                tile1, tile2 = tiles_in_row[i], tiles_in_row[j]
                goal_row1, goal_col1 = goal_positions[tile1]
                goal_row2, goal_col2 = goal_positions[tile2]
                if goal_row1 == row and goal_row2 == row and goal_col1 > goal_col2:
                    distance += 2  # Conflicto en fila
    
    # Revisar conflictos lineales en columnas
    for col in range(3):
        tiles_in_col = [state.board[row][col] for row in range(3) if state.board[row][col] != 0]
        for i in range(len(tiles_in_col)):
            for j in range(i + 1, len(tiles_in_col)):
                tile1, tile2 = tiles_in_col[i], tiles_in_col[j]
                goal_row1, goal_col1 = goal_positions[tile1]
                goal_row2, goal_col2 = goal_positions[tile2]
                if goal_col1 == col and goal_col2 == col and goal_row1 > goal_row2:
                    distance += 2  # Conflicto en columna
    
    return distance

