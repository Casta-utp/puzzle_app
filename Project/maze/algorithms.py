import time
from utils import Queue, MinHeap
from maze.heuristics import *

# Algoritmos adaptados para laberinto
def maze_bfs(initial_state, goal_state):
    queue = Queue()
    visited = set()
    nodes_expanded = 0
    
    queue.enqueue(initial_state)
    visited.add(initial_state.position)
    
    start_time = time.time()
    
    while not queue.is_empty():
        current = queue.dequeue()
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_maze_path(current), nodes_expanded, end_time - start_time
        
        for neighbor in current.get_neighbors():
            if neighbor.position not in visited:
                visited.add(neighbor.position)
                queue.enqueue(neighbor)
    
    return None, nodes_expanded, time.time() - start_time

def maze_a_star(initial_state, goal_state, heuristic):
    heap = MinHeap()
    visited = set()
    nodes_expanded = 0
    
    initial_f = heuristic(initial_state, goal_state)
    heap.push((initial_f, 0, initial_state))
    
    start_time = time.time()
    
    while not heap.is_empty():
        f_score, g_score, current = heap.pop()
        
        if current.position in visited:
            continue
            
        visited.add(current.position)
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_maze_path(current), nodes_expanded, end_time - start_time
        
        for neighbor in current.get_neighbors():
            if neighbor.position not in visited:
                g = current.moves + 1
                h = heuristic(neighbor, goal_state)
                f = g + h
                heap.push((f, g, neighbor))
    
    return None, nodes_expanded, time.time() - start_time

def maze_greedy(initial_state, goal_state, heuristic):
    heap = MinHeap()
    visited = set()
    nodes_expanded = 0
    
    h = heuristic(initial_state, goal_state)
    heap.push((h, initial_state))
    
    start_time = time.time()
    
    while not heap.is_empty():
        h, current = heap.pop()
        
        if current.position in visited:
            continue
        
        visited.add(current.position)
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_maze_path(current), nodes_expanded, end_time - start_time
        
        for neighbor in current.get_neighbors():
            if neighbor.position not in visited:
                h = heuristic(neighbor, goal_state)
                heap.push((h, neighbor))
    
    return None, nodes_expanded, time.time() - start_time

def reconstruct_maze_path(state):
    path = []
    current = state
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]