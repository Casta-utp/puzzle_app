import time
from utils import Stack, Queue, MinHeap
from puzzle.heuristics import manhattan_distance, misplaced_tiles, linear_conflict

# Algoritmos de búsqueda
def bfs(initial_state, goal_state):
    queue = Queue()
    visited = set()
    nodes_expanded = 0
    
    queue.enqueue(initial_state)
    visited.add(hash(str(initial_state.board)))
    
    start_time = time.time()
    
    while not queue.is_empty():
        current = queue.dequeue()
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_path(current), nodes_expanded, end_time - start_time
        
        for neighbor in current.get_neighbors():
            state_hash = hash(str(neighbor.board))
            if state_hash not in visited:
                visited.add(state_hash)
                queue.enqueue(neighbor)
    
    return None, nodes_expanded, time.time() - start_time

def a_star(initial_state, goal_state, heuristic):
    heap = MinHeap()
    visited = set()
    nodes_expanded = 0
    
    initial_f = heuristic(initial_state, goal_state)
    heap.push((initial_f, 0, initial_state))
    
    start_time = time.time()
    
    while not heap.is_empty():
        f_score, g_score, current = heap.pop()
        
        if hash(str(current.board)) in visited:
            continue
            
        visited.add(hash(str(current.board)))
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_path(current), nodes_expanded, end_time - start_time
        
        for neighbor in current.get_neighbors():
            state_hash = hash(str(neighbor.board))
            if state_hash not in visited:
                g = current.moves + 1
                h = heuristic(neighbor, goal_state)
                f = g + h
                heap.push((f, g, neighbor))
    
    return None, nodes_expanded, time.time() - start_time

def dfs(initial_state, goal_state, max_depth=50):
    stack = Stack()
    visited = set()
    nodes_expanded = 0
    
    stack.push((initial_state, 0))  # (estado, profundidad)
    visited.add(hash(str(initial_state.board)))
    
    start_time = time.time()
    
    while not stack.is_empty():
        current, depth = stack.pop()
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_path(current), nodes_expanded, end_time - start_time
        
        if depth < max_depth:  # límite para evitar ciclos infinitos
            for neighbor in current.get_neighbors():
                state_hash = hash(str(neighbor.board))
                if state_hash not in visited:
                    visited.add(state_hash)
                    stack.push((neighbor, depth + 1))
    
    return None, nodes_expanded, time.time() - start_time

def ucs(initial_state, goal_state):
    heap = MinHeap()
    visited = set()
    nodes_expanded = 0
    
    heap.push((0, initial_state))  # (costo acumulado, estado)
    
    start_time = time.time()
    
    while not heap.is_empty():
        g, current = heap.pop()
        
        if hash(str(current.board)) in visited:
            continue
        
        visited.add(hash(str(current.board)))
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_path(current), nodes_expanded, end_time - start_time
        
        for neighbor in current.get_neighbors():
            state_hash = hash(str(neighbor.board))
            if state_hash not in visited:
                heap.push((g + 1, neighbor))
    
    return None, nodes_expanded, time.time() - start_time

def greedy(initial_state, goal_state, heuristic):
    heap = MinHeap()
    visited = set()
    nodes_expanded = 0
    
    h = heuristic(initial_state, goal_state)
    heap.push((h, initial_state))
    
    start_time = time.time()
    
    while not heap.is_empty():
        h, current = heap.pop()
        
        if hash(str(current.board)) in visited:
            continue
        
        visited.add(hash(str(current.board)))
        nodes_expanded += 1
        
        if current == goal_state:
            end_time = time.time()
            return reconstruct_path(current), nodes_expanded, end_time - start_time
        
        for neighbor in current.get_neighbors():
            state_hash = hash(str(neighbor.board))
            if state_hash not in visited:
                h = heuristic(neighbor, goal_state)
                heap.push((h, neighbor))
    
    return None, nodes_expanded, time.time() - start_time

def ida_star(initial_state, goal_state, heuristic):
    start_time = time.time()
    bound = heuristic(initial_state, goal_state)
    path = [initial_state]
    
    def search(path, g, bound):
        current = path[-1]
        f = g + heuristic(current, goal_state)
        
        if f > bound:
            return f
        if current == goal_state:
            return "FOUND"
        
        min_bound = float('inf')
        for neighbor in current.get_neighbors():
            if neighbor not in path:  # evitar ciclos
                path.append(neighbor)
                t = search(path, g + 1, bound)
                if t == "FOUND":
                    return "FOUND"
                if t < min_bound:
                    min_bound = t
                path.pop()
        return min_bound
    
    nodes_expanded = 0
    while True:
        t = search(path, 0, bound)
        nodes_expanded += 1
        if t == "FOUND":
            end_time = time.time()
            return path[:], nodes_expanded, end_time - start_time
        if t == float('inf'):
            return None, nodes_expanded, time.time() - start_time
        bound = t

def weighted_a_star(initial_state, goal_state, heuristic, weight=1.5):
    heap = MinHeap()
    # best_g guarda el mejor costo g visto para un estado; evita re-expandir peores caminos
    best_g = {}
    nodes_expanded = 0

    g0 = 0
    h0 = heuristic(initial_state, goal_state)
    f0 = g0 + weight * h0
    heap.push((f0, g0, initial_state))
    best_g[hash(str(initial_state.board))] = 0

    start_time = time.time()

    while not heap.is_empty():
        f, g, current = heap.pop()
        nodes_expanded += 1

        if current == goal_state:
            end_time = time.time()
            return reconstruct_path(current), nodes_expanded, end_time - start_time

        for neighbor in current.get_neighbors():
            state_hash = hash(str(neighbor.board))
            g2 = g + 1
            # solo considerar si mejora el mejor g conocido
            if state_hash not in best_g or g2 < best_g[state_hash]:
                best_g[state_hash] = g2
                h2 = heuristic(neighbor, goal_state)
                f2 = g2 + weight * h2
                heap.push((f2, g2, neighbor))

    return None, nodes_expanded, time.time() - start_time

def rbfs(initial_state, goal_state, heuristic):
    start_time = time.time()
    nodes_expanded = [0]  # lista para poder mutar dentro de la función anidada

    # Nodo auxiliar que transporta (estado, g, f)
    class Node:
        __slots__ = ("state", "g", "f")
        def __init__(self, state, g, f):
            self.state = state
            self.g = g
            self.f = f

    def make_node(state, g):
        h = heuristic(state, goal_state)
        f = g + h
        return Node(state, g, f)

    def _rbfs(node, f_limit):
        nodes_expanded[0] += 1
        # Objetivo
        if node.state == goal_state:
            return node.state, node.f

        # Generar sucesores
        successors = []
        for child_state in node.state.get_neighbors():
            g2 = node.g + 1
            # f del hijo = max(g2 + h, f del padre) (truco de RBFS para monotonicidad)
            h2 = heuristic(child_state, goal_state)
            f2 = max(g2 + h2, node.f)
            successors.append(Node(child_state, g2, f2))

        if not successors:
            return None, float('inf')

        # Bucle principal RBFS
        while True:
            # Ordenar por f
            successors.sort(key=lambda n: n.f)
            best = successors[0]

            if best.f > f_limit:
                # No se puede mejorar dentro del límite
                return None, best.f

            # Segundo mejor para el nuevo límite alternativo
            alternative = successors[1].f if len(successors) > 1 else float('inf')

            # Recurre acotando por el mínimo entre el límite actual y el alternativo
            result, best.f = _rbfs(best, min(f_limit, alternative))
            if result is not None:
                return result, best.f
            # Si no hubo solución, el mejor vuelve con su f actualizada; se repite

    root = make_node(initial_state, 0)
    result_state, _ = _rbfs(root, float('inf'))

    if result_state is not None:
        end_time = time.time()
        # reconstrucción de path usando los parent ya mantenidos por PuzzleState
        # Nota: get_neighbors() ya asigna parent=self; el recorrido recursivo respetó esa cadena
        path = reconstruct_path(result_state)
        return path, nodes_expanded[0], end_time - start_time

    return None, nodes_expanded[0], time.time() - start_time

def bidirectional_search(initial_state, goal_state):
    from collections import deque
    start_time = time.time()

    # Colas de BFS desde ambos lados
    queue_start = deque([initial_state])
    queue_goal = deque([goal_state])

    # Visitados desde ambos lados
    visited_start = {hash(str(initial_state.board)): initial_state}
    visited_goal = {hash(str(goal_state.board)): goal_state}

    nodes_expanded = 0

    while queue_start and queue_goal:
        # Expandir desde el inicio
        if queue_start:
            current_start = queue_start.popleft()
            nodes_expanded += 1

            for neighbor in current_start.get_neighbors():
                hsh = hash(str(neighbor.board))
                if hsh not in visited_start:
                    visited_start[hsh] = neighbor
                    queue_start.append(neighbor)

                    # ¿Se encuentra con búsqueda desde goal?
                    if hsh in visited_goal:
                        # Reconstrucción de path
                        path_from_start = reconstruct_path(neighbor)
                        path_from_goal = reconstruct_path(visited_goal[hsh])
                        # unir (evitar repetir nodo de encuentro)
                        full_path = path_from_start[:-1] + path_from_goal[::-1]
                        return full_path, nodes_expanded, time.time() - start_time

        # Expandir desde el objetivo
        if queue_goal:
            current_goal = queue_goal.popleft()
            nodes_expanded += 1

            for neighbor in current_goal.get_neighbors():
                hsh = hash(str(neighbor.board))
                if hsh not in visited_goal:
                    visited_goal[hsh] = neighbor
                    queue_goal.append(neighbor)

                    # ¿Se encuentra con búsqueda desde inicio?
                    if hsh in visited_start:
                        path_from_start = reconstruct_path(visited_start[hsh])
                        path_from_goal = reconstruct_path(neighbor)
                        full_path = path_from_start[:-1] + path_from_goal[::-1]
                        return full_path, nodes_expanded, time.time() - start_time

    return None, nodes_expanded, time.time() - start_time

def compare_heuristics(initial_state, goal_state):
    heuristics = {
        "Manhattan": manhattan_distance,
        "Misplaced Tiles": misplaced_tiles,
        "Linear Conflict": linear_conflict
    }

    results = []
    for name, h in heuristics.items():
        path, nodes, exec_time = a_star(initial_state, goal_state, h)
        steps = len(path) - 1 if path else None
        results.append((name, nodes, exec_time, steps))

    return results

def reconstruct_path(state):
    path = []
    current = state
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]