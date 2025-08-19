# Clases para el laberinto
class MazeState:
    def __init__(self, position, maze, moves=0, parent=None):
        self.position = position  # (row, col)
        self.maze = maze
        self.moves = moves
        self.parent = parent
    
    def get_neighbors(self):
        neighbors = []
        row, col = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < len(self.maze) and 
                0 <= new_col < len(self.maze[0]) and 
                self.maze[new_row][new_col] != 1):  # 1 = pared
                new_pos = (new_row, new_col)
                neighbors.append(MazeState(new_pos, self.maze, self.moves + 1, self))
        
        return neighbors
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __hash__(self):
        return hash(self.position)
    
    def __lt__(self, other):
        return self.moves < other.moves