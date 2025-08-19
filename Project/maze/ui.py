import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from maze.state import MazeState
from puzzle.ui import ResultPopup

# You'll also need to import your maze solving algorithms and classes
# Assuming they're in separate files:
from maze.algorithms import (
    maze_bfs, 
    maze_a_star, 
    maze_greedy,
    maze_manhattan_distance,
    maze_euclidean_distance,
    maze_chebyshev_distance
)

class MazeCell(Button):
    def __init__(self, cell_type, maze_grid, row, col, **kwargs):
        super().__init__(**kwargs)
        self.cell_type = cell_type  # 0=camino, 1=pared, 2=inicio, 3=meta
        self.maze_grid = maze_grid
        self.row = row
        self.col = col
        self.text = ""
        self.update_appearance()
        
    def update_appearance(self):
        if self.cell_type == 0:  # Camino
            self.background_color = (1, 1, 1, 1)
        elif self.cell_type == 1:  # Pared
            self.background_color = (0.2, 0.2, 0.2, 1)
        elif self.cell_type == 2:  # Inicio
            self.background_color = (0.2, 0.8, 0.2, 1)
            self.text = "S"
        elif self.cell_type == 3:  # Meta
            self.background_color = (0.8, 0.2, 0.2, 1)
            self.text = "G"
        elif self.cell_type == 4:  # Camino de solución
            self.background_color = (0.2, 0.6, 1, 1)
    
    def on_press(self):
        self.maze_grid.cell_pressed(self)

class MazeGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 10
        self.cols = 10
        self.spacing = 2
        self.padding = 10
        self.cells = []
        self.maze = [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.start_pos = (0, 0)
        self.goal_pos = (9, 9)
        self.edit_mode = 0  # 0=camino, 1=pared
        self.create_cells()
        
    def create_cells(self):
        self.clear_widgets()
        self.cells = []
        
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if (i, j) == self.start_pos:
                    cell_type = 2
                elif (i, j) == self.goal_pos:
                    cell_type = 3
                else:
                    cell_type = self.maze[i][j]
                
                cell = MazeCell(cell_type, self, i, j)
                cell.size_hint = (1, 1)
                self.add_widget(cell)
                row.append(cell)
            self.cells.append(row)
    
    def cell_pressed(self, pressed_cell):
        if (pressed_cell.row, pressed_cell.col) not in [self.start_pos, self.goal_pos]:
            self.maze[pressed_cell.row][pressed_cell.col] = self.edit_mode
            pressed_cell.cell_type = self.edit_mode
            pressed_cell.update_appearance()
    
    def clear_solution(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].cell_type == 4:
                    if (i, j) == self.start_pos:
                        self.cells[i][j].cell_type = 2
                    elif (i, j) == self.goal_pos:
                        self.cells[i][j].cell_type = 3
                    else:
                        self.cells[i][j].cell_type = self.maze[i][j]
                    self.cells[i][j].update_appearance()
    
    def show_solution(self, path):
        self.clear_solution()
        if path:
            for state in path[1:-1]:  # Excluir inicio y meta
                row, col = state.position
                self.cells[row][col].cell_type = 4
                self.cells[row][col].update_appearance()

class MazeApp(App):
    def build(self):
        self.title = "Maze Solver"
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Título
        title = Label(
            text='Maze Solver',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height='50dp',
            color=(0.2, 0.2, 0.8, 1)
        )
        
        # Grid del laberinto
        self.maze_grid = MazeGrid(size_hint_y=None, height='400dp')
        
        # Controles
        controls_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height='250dp')
        
        # Selector de algoritmo
        algorithm_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        algorithm_label = Label(text='Algoritmo:', size_hint_x=None, width='100dp')
        self.maze_algorithm_spinner = Spinner(
            text='BFS',
            values=[
                'BFS',
                'A* Manhattan',
                'A* Euclidean',
                'A* Chebyshev',
                'Greedy Manhattan',
                'Greedy Euclidean',
                'Greedy Chebyshev'
            ],
            size_hint_x=None,
            width='200dp'
        )
        algorithm_layout.add_widget(algorithm_label)
        algorithm_layout.add_widget(self.maze_algorithm_spinner)
        algorithm_layout.add_widget(Widget())
        
        # Modo de edición
        edit_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        edit_label = Label(text='Modo:', size_hint_x=None, width='100dp')
        self.edit_spinner = Spinner(
            text='Camino',
            values=['Camino', 'Pared'],
            size_hint_x=None,
            width='150dp'
        )
        self.edit_spinner.bind(text=self.on_edit_mode_change)
        edit_layout.add_widget(edit_label)
        edit_layout.add_widget(self.edit_spinner)
        edit_layout.add_widget(Widget())
        
        # Botones de control
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='50dp')
        
        solve_btn = Button(
            text='Resolver',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='16sp'
        )
        solve_btn.bind(on_press=self.solve_maze)
        
        clear_btn = Button(
            text='Limpiar Solución',
            background_color=(0.8, 0.6, 0.2, 1),
            font_size='16sp'
        )
        clear_btn.bind(on_press=self.clear_solution)
        
        reset_btn = Button(
            text='Reiniciar Laberinto',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='16sp'
        )
        reset_btn.bind(on_press=self.reset_maze)
        
        buttons_layout.add_widget(solve_btn)
        buttons_layout.add_widget(clear_btn)
        buttons_layout.add_widget(reset_btn)
        
        # Barra de progreso
        self.maze_progress_bar = ProgressBar(max=100, size_hint_y=None, height='20dp')
        
        # Status label
        self.maze_status_label = Label(
            text='Edita el laberinto y presiona Resolver',
            size_hint_y=None,
            height='30dp',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        # Instrucciones
        instructions = Label(
            text='Toca las celdas para editar. S=Inicio, G=Meta',
            size_hint_y=None,
            height='30dp',
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        
        # Ensamblar layout
        controls_layout.add_widget(algorithm_layout)
        controls_layout.add_widget(edit_layout)
        controls_layout.add_widget(buttons_layout)
        controls_layout.add_widget(self.maze_progress_bar)
        controls_layout.add_widget(self.maze_status_label)
        controls_layout.add_widget(instructions)
        
        main_layout.add_widget(title)
        main_layout.add_widget(self.maze_grid)
        main_layout.add_widget(controls_layout)
        
        return main_layout
    
    def on_edit_mode_change(self, spinner, text):
        self.maze_grid.edit_mode = 0 if text == 'Camino' else 1
    
    def solve_maze(self, instance):
        self.maze_status_label.text = 'Resolviendo laberinto...'
        self.maze_progress_bar.value = 0
        
        thread = threading.Thread(target=self._solve_maze_in_background)
        thread.daemon = True
        thread.start()
    
    def _solve_maze_in_background(self):
        initial_state = MazeState(self.maze_grid.start_pos, self.maze_grid.maze)
        goal_state = MazeState(self.maze_grid.goal_pos, self.maze_grid.maze)
        
        algorithm = self.maze_algorithm_spinner.text
        
        Clock.schedule_once(lambda dt: setattr(self.maze_progress_bar, 'value', 25), 0.1)
        
        try:
            if algorithm == 'BFS':
                path, nodes, exec_time = maze_bfs(initial_state, goal_state)
            elif algorithm == 'A* Manhattan':
                path, nodes, exec_time = maze_a_star(initial_state, goal_state, maze_manhattan_distance)
            elif algorithm == 'A* Euclidean':
                path, nodes, exec_time = maze_a_star(initial_state, goal_state, maze_euclidean_distance)
            elif algorithm == 'A* Chebyshev':
                path, nodes, exec_time = maze_a_star(initial_state, goal_state, maze_chebyshev_distance)
            elif algorithm == 'Greedy Manhattan':
                path, nodes, exec_time = maze_greedy(initial_state, goal_state, maze_manhattan_distance)
            elif algorithm == 'Greedy Euclidean':
                path, nodes, exec_time = maze_greedy(initial_state, goal_state, maze_euclidean_distance)
            elif algorithm == 'Greedy Chebyshev':
                path, nodes, exec_time = maze_greedy(initial_state, goal_state, maze_chebyshev_distance)
            
            Clock.schedule_once(lambda dt: self._show_maze_results(algorithm, path, nodes, exec_time), 0.3)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._show_maze_error(str(e)), 0.1)
    
    def _show_maze_results(self, algorithm, path, nodes, exec_time):
        self.maze_progress_bar.value = 0
        
        if path:
            result_text = f"¡Camino encontrado!\n\n"
            result_text += f"Algoritmo: {algorithm}\n"
            result_text += f"Longitud del camino: {len(path) - 1}\n"
            result_text += f"Nodos expandidos: {nodes}\n"
            result_text += f"Tiempo: {exec_time:.4f} segundos"
            
            self.maze_status_label.text = f'Camino encontrado ({len(path) - 1} pasos)'
            self.maze_grid.show_solution(path)
        else:
            result_text = "No se encontró camino para este laberinto."
            self.maze_status_label.text = 'Sin solución'
        
        popup = ResultPopup("Resultado del Laberinto", result_text)
        popup.open()
    
    def _show_maze_error(self, error_msg):
        self.maze_progress_bar.value = 0
        self.maze_status_label.text = 'Error al resolver'
        popup = ResultPopup("Error", f"Error: {error_msg}")
        popup.open()
    
    def clear_solution(self, instance):
        self.maze_grid.clear_solution()
        self.maze_status_label.text = 'Solución eliminada'
    
    def reset_maze(self, instance):
        self.maze_grid.maze = [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.maze_grid.create_cells()
        self.maze_status_label.text = 'Laberinto reiniciado'
