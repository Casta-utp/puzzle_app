import threading
import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.metrics import dp
from kivy.core.text import Label as CoreLabel

# Importar las funciones de algoritmos y heurísticas desde tus otros módulos
from puzzle.state import PuzzleState
from puzzle.algorithms import (
    bfs, dfs, ucs, greedy, ida_star, weighted_a_star, 
    rbfs, a_star, bidirectional_search
)
from puzzle.heuristics import (
    manhattan_distance, misplaced_tiles, linear_conflict
)
from puzzle.algorithms import compare_heuristics

class PuzzleTile(Button):
    def __init__(self, value, puzzle_grid, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.puzzle_grid = puzzle_grid
        self.text = str(value) if value != 0 else ""
        self.font_size = '20sp'
        self.bold = True
        self.update_appearance()
        
    def update_appearance(self):
        if self.value == 0:
            self.background_color = (0.9, 0.9, 0.9, 1)
            self.color = (0.9, 0.9, 0.9, 1)
        else:
            self.background_color = (0.2, 0.6, 1, 1)
            self.color = (1, 1, 1, 1)
    
    def on_press(self):
        self.puzzle_grid.tile_pressed(self)

class PuzzleGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.spacing = 5
        self.padding = 10
        self.tiles = []
        self.board = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
        self.create_tiles()
        
    def create_tiles(self):
        self.clear_widgets()
        self.tiles = []
        
        for i in range(3):
            row = []
            for j in range(3):
                tile = PuzzleTile(self.board[i][j], self)
                tile.size_hint = (1, 1)
                self.add_widget(tile)
                row.append(tile)
            self.tiles.append(row)
    
    def tile_pressed(self, pressed_tile):
        # Encontrar posición del tile presionado
        tile_pos = None
        blank_pos = None
        
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] == pressed_tile:
                    tile_pos = (i, j)
                if self.tiles[i][j].value == 0:
                    blank_pos = (i, j)
        
        if tile_pos and blank_pos:
            # Verificar si el tile está adyacente al espacio en blanco
            if self.is_adjacent(tile_pos, blank_pos):
                self.swap_tiles(tile_pos, blank_pos)
    
    def is_adjacent(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1
    
    def swap_tiles(self, pos1, pos2):
        # Intercambiar valores en el board
        self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = \
            self.board[pos2[0]][pos2[1]], self.board[pos1[0]][pos1[1]]
        
        # Actualizar tiles
        self.tiles[pos1[0]][pos1[1]].value = self.board[pos1[0]][pos1[1]]
        self.tiles[pos2[0]][pos2[1]].value = self.board[pos2[0]][pos2[1]]
        
        self.tiles[pos1[0]][pos1[1]].text = str(self.board[pos1[0]][pos1[1]]) if self.board[pos1[0]][pos1[1]] != 0 else ""
        self.tiles[pos2[0]][pos2[1]].text = str(self.board[pos2[0]][pos2[1]]) if self.board[pos2[0]][pos2[1]] != 0 else ""
        
        self.tiles[pos1[0]][pos1[1]].update_appearance()
        self.tiles[pos2[0]][pos2[1]].update_appearance()
    
    def set_board(self, new_board):
        self.board = [row[:] for row in new_board]
        self.create_tiles()
    
    def get_board(self):
        return [row[:] for row in self.board]
    
class ResultPopup(Popup):
    def __init__(self, title_text, result_text, **kwargs):
        super().__init__(**kwargs)
        self.title = title_text
        self.size_hint = (0.8, 0.6)
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        result_label = Label(
            text=result_text,
            text_size=(None, None),
            halign='center',
            valign='middle',
            font_size='16sp'
        )
        
        close_btn = Button(
            text='Cerrar',
            size_hint_y=None,
            height='48dp',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        close_btn.bind(on_press=self.dismiss)
        
        content.add_widget(result_label)
        content.add_widget(close_btn)
        
        self.content = content

class BarChart(Widget):
    def __init__(self, data, title, y_label, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.title = title
        self.y_label = y_label
        self.bind(size=self.draw_chart, pos=self.draw_chart)
    
    def draw_chart(self, *args):
        self.canvas.clear()
        if not self.data:
            return
            
        labels = [item[0] for item in self.data]
        values = [item[1] for item in self.data]
        max_value = max(values) if values else 1
        
        # Márgenes
        margin_left = dp(80)
        margin_bottom = dp(100)
        margin_top = dp(60)
        margin_right = dp(40)
        
        chart_width = self.width - margin_left - margin_right
        chart_height = self.height - margin_bottom - margin_top
        
        if chart_width <= 0 or chart_height <= 0:
            return
            
        bar_width = chart_width / len(values) * 0.6
        spacing = chart_width / len(values) * 0.4
        
        with self.canvas:
            # Fondo blanco
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # Ejes principales
            Color(0, 0, 0, 1)
            Line(points=[
                self.x + margin_left, self.y + margin_bottom,
                self.x + margin_left, self.y + self.height - margin_top
            ], width=2)
            Line(points=[
                self.x + margin_left, self.y + margin_bottom,
                self.x + self.width - margin_right, self.y + margin_bottom
            ], width=2)
            
            # Dibujar barras y textos
            for i, (label, value) in enumerate(self.data):
                bar_height = (value / max_value) * chart_height if max_value > 0 else 0
                bar_x = self.x + margin_left + i * (bar_width + spacing) + spacing/2
                bar_y = self.y + margin_bottom
                
                # Color de barra
                colors = [
                    (0.2, 0.6, 1, 1),    # Azul
                    (1, 0.5, 0.2, 1),    # Naranja
                    (0.2, 0.8, 0.2, 1),  # Verde
                ]
                color = colors[i % len(colors)]
                Color(*color)
                Rectangle(pos=(bar_x, bar_y), size=(bar_width, bar_height))
                
                # Borde de barra
                Color(0, 0, 0, 1)
                Line(rectangle=(bar_x, bar_y, bar_width, bar_height), width=1)

                # ---- TEXTO DE VALOR ENCIMA ----
                if value is not None:
                    label_val = CoreLabel(text=f"{value:.5f}", font_size=12)
                    label_val.refresh()
                    texture = label_val.texture
                    Rectangle(texture=texture, pos=(bar_x + bar_width/2 - texture.size[0]/2,
                                                    bar_y + bar_height + 5),
                              size=texture.size)

                # ---- TEXTO DE ETIQUETA ABAJO ----
                lbl = CoreLabel(text=label, font_size=12)
                lbl.refresh()
                texture = lbl.texture
                Rectangle(texture=texture, pos=(bar_x + bar_width/2 - texture.size[0]/2,
                                                self.y + margin_bottom - 30),
                          size=texture.size)

            # ---- Título arriba ----
            title_label = CoreLabel(text=self.title, font_size=16)
            title_label.refresh()
            Rectangle(texture=title_label.texture,
                      pos=(self.center_x - title_label.texture.size[0]/2,
                           self.y + self.height - margin_top + 20),
                      size=title_label.texture.size)

            # ---- Etiqueta eje Y ----
            y_label = CoreLabel(text=self.y_label, font_size=14)
            y_label.refresh()
            Rectangle(texture=y_label.texture,
                      pos=(self.x + 10, self.center_y - y_label.texture.size[1]/2),
                      size=y_label.texture.size)

class PuzzleApp(App):
    def build(self):
        self.title = "8-Puzzle Solver"
        self.solution_path = None
        self.current_step = 0
        self.anim_event = None
        self.animating = False

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Título
        title = Label(
            text='8-Puzzle Solver',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height='50dp',
            color=(0.2, 0.2, 0.8, 1)
        )

        # Botones de animación
        anim_buttons = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='50dp')

        play_btn = Button(text='Play', background_color=(1, 0.5, 0, 1), font_size='16sp')
        play_btn.bind(on_press=self.start_animation)

        pause_btn = Button(text='Pausa', background_color=(1, 0, 0, 1), font_size='16sp')
        pause_btn.bind(on_press=self.pause_animation)

        resume_btn = Button(text='Reanudar', background_color=(0.2, 0.8, 0.6, 1), font_size='16sp')
        resume_btn.bind(on_press=self.resume_animation)

        anim_buttons.add_widget(play_btn)
        anim_buttons.add_widget(pause_btn)
        anim_buttons.add_widget(resume_btn)
        
        # Grid del puzzle
        self.puzzle_grid = PuzzleGrid(size_hint_y=None, height='300dp')
        
        # Controles
        controls_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height='200dp')
        
        # Selector de algoritmo
        algorithm_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        algorithm_label = Label(text='Algoritmo:', size_hint_x=None, width='100dp')
        self.algorithm_spinner = Spinner(
            text='BFS',
            values=[
                'BFS',
                'DFS',
                'UCS',
                'Greedy Manhattan',
                'Greedy Misplaced',
                'Greedy Linear Conflict',
                'IDA* Manhattan',
                'IDA* Misplaced',
                'IDA* Linear Conflict',
                'Weighted A* Manhattan',
                'Weighted A* Misplaced',
                'Weighted A* Linear Conflict',
                'RBFS Manhattan',
                'RBFS Misplaced',
                'RBFS Linear Conflict',
                'A* Manhattan',
                'A* Misplaced',
                'A* Linear Conflict',
                'Bidirectional Search'
            ],
            size_hint_x=None,
            width='250dp'
        )
        algorithm_layout.add_widget(algorithm_label)
        algorithm_layout.add_widget(self.algorithm_spinner)
        algorithm_layout.add_widget(Widget())  # Spacer
        
        # Botones de control
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='50dp')
        
        solve_btn = Button(
            text='Resolver',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='16sp'
        )
        solve_btn.bind(on_press=self.solve_puzzle)
        
        reset_btn = Button(
            text='Reiniciar',
            background_color=(0.8, 0.6, 0.2, 1),
            font_size='16sp'
        )
        reset_btn.bind(on_press=self.reset_puzzle)
        
        random_btn = Button(
            text='Aleatorio',
            background_color=(0.6, 0.2, 0.8, 1),
            font_size='16sp'
        )
        random_btn.bind(on_press=self.randomize_puzzle)

        compare_btn = Button(
            text='Comparar',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size='16sp',
            size_hint_x=0.6
        )
        compare_btn.bind(on_press=self.show_comparison)

        buttons_layout.add_widget(compare_btn)

        buttons_layout.add_widget(solve_btn)
        buttons_layout.add_widget(reset_btn)
        buttons_layout.add_widget(random_btn)
        
        # Barra de progreso
        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height='20dp')
        
        # Status label
        self.status_label = Label(
            text='Listo para resolver',
            size_hint_y=None,
            height='30dp',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        # Ensamblar layout
        controls_layout.add_widget(algorithm_layout)
        controls_layout.add_widget(buttons_layout)
        controls_layout.add_widget(self.progress_bar)
        controls_layout.add_widget(self.status_label)
        
        main_layout.add_widget(title)
        main_layout.add_widget(anim_buttons) 
        main_layout.add_widget(self.puzzle_grid)
        main_layout.add_widget(controls_layout)
        
        return main_layout
    
    def solve_puzzle(self, instance):
        self.status_label.text = 'Resolviendo...'
        self.progress_bar.value = 0
        
        # Ejecutar en hilo separado para no bloquear UI
        thread = threading.Thread(target=self._solve_in_background)
        thread.daemon = True
        thread.start()
    
    def _solve_in_background(self):
        initial_state = PuzzleState(self.puzzle_grid.get_board())
        goal_state = PuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        
        algorithm = self.algorithm_spinner.text
        
        # Simular progreso
        Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 25), 0.1)
        
        try:
            if algorithm == 'BFS':
                path, nodes, exec_time = bfs(initial_state, goal_state)
            elif algorithm == 'DFS':
                path, nodes, exec_time = dfs(initial_state, goal_state)
            elif algorithm == 'UCS':
                path, nodes, exec_time = ucs(initial_state, goal_state)
            elif algorithm == 'Greedy Manhattan':
                path, nodes, exec_time = greedy(initial_state, goal_state, manhattan_distance)
            elif algorithm == 'Greedy Misplaced':
                path, nodes, exec_time = greedy(initial_state, goal_state, misplaced_tiles)
            elif algorithm == 'IDA* Manhattan':
                path, nodes, exec_time = ida_star(initial_state, goal_state, manhattan_distance)
            elif algorithm == 'IDA* Misplaced':
                path, nodes, exec_time = ida_star(initial_state, goal_state, misplaced_tiles)
            elif algorithm == 'Weighted A* Manhattan':
                path, nodes, exec_time = weighted_a_star(initial_state, goal_state, manhattan_distance, weight=1.5)
            elif algorithm == 'Weighted A* Misplaced':
                path, nodes, exec_time = weighted_a_star(initial_state, goal_state, misplaced_tiles, weight=1.5)
            elif algorithm == 'RBFS Manhattan':
                path, nodes, exec_time = rbfs(initial_state, goal_state, manhattan_distance)
            elif algorithm == 'RBFS Misplaced':
                path, nodes, exec_time = rbfs(initial_state, goal_state, misplaced_tiles)
            elif algorithm == 'A* Manhattan':
                path, nodes, exec_time = a_star(initial_state, goal_state, manhattan_distance)
            elif algorithm == 'Greedy Linear Conflict':
                path, nodes, exec_time = greedy(initial_state, goal_state, linear_conflict)
            elif algorithm == 'IDA* Linear Conflict':
                path, nodes, exec_time = ida_star(initial_state, goal_state, linear_conflict)
            elif algorithm == 'Weighted A* Linear Conflict':
                path, nodes, exec_time = weighted_a_star(initial_state, goal_state, linear_conflict, weight=1.5)
            elif algorithm == 'RBFS Linear Conflict':
                path, nodes, exec_time = rbfs(initial_state, goal_state, linear_conflict)
            elif algorithm == 'A* Linear Conflict':
                path, nodes, exec_time = a_star(initial_state, goal_state, linear_conflict)
            elif algorithm == 'Bidirectional Search':
                path, nodes, exec_time = bidirectional_search(initial_state, goal_state)
            else:  # A* Misplaced
                path, nodes, exec_time = a_star(initial_state, goal_state, misplaced_tiles)
            
            # Mostrar resultados
            Clock.schedule_once(lambda dt: self._show_results(algorithm, path, nodes, exec_time), 0.3)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._show_error(str(e)), 0.1)
    
    def _show_results(self, algorithm, path, nodes, exec_time):
        self.progress_bar.value = 0

        if path:
            result_text = f"¡Solución encontrada!\n\n"
            result_text += f"Algoritmo: {algorithm}\n"
            result_text += f"Pasos necesarios: {len(path) - 1}\n"
            result_text += f"Nodos expandidos: {nodes}\n"
            result_text += f"Tiempo: {exec_time:.4f} segundos"

            self.status_label.text = f'Resuelto en {len(path) - 1} pasos'
            # Guardar path para animación
            self.solution_path = path
            self.current_step = 0
        else:
            result_text = "No se encontró solución para este puzzle."
            self.status_label.text = 'Sin solución'

        popup = ResultPopup("Resultado", result_text)
        popup.open()

    def show_comparison(self, instance):
        # Use instance parameter to avoid warning
        _ = instance
        
        initial_state = PuzzleState(self.puzzle_grid.get_board())
        goal_state = PuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        results = compare_heuristics(initial_state, goal_state)

        # --- Texto comparativo con mejor formato ---
        table_text = "COMPARACIÓN DE HEURÍSTICAS (A*)\n"
        table_text += "=" * 60 + "\n\n"
        table_text += f"{'HEURÍSTICA':<20}{'NODOS':<12}{'TIEMPO(s)':<15}{'PASOS':<10}\n"
        table_text += "-" * 60 + "\n"

        for name, nodes, exec_time, steps in results:
            table_text += f"{name:<20}{nodes:<10}{exec_time:<12.4f}{steps or 'N/A':<8}\n"

        popup = ResultPopup("Comparación", table_text)
        popup.open()

        # --- Datos para gráficos ---
        nodes_data = [(r[0], r[1]) for r in results]
        times_data = [(r[0], r[2]) for r in results]

        # --- Popup con gráfico de nodos ---
        content_nodes = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # Título del gráfico
        title_nodes = Label(
            text="Nodos Expandidos por Heurística", 
            size_hint_y=None, 
            height=dp(40), 
            color=(0, 0, 0, 1), 
            font_size='18sp',
            bold=True
        )
        content_nodes.add_widget(title_nodes)
        
        # Crear el gráfico
        chart_nodes = BarChart(nodes_data, "Nodos Expandidos", "Nodos", 
                            size_hint_y=None, height=dp(300))
        content_nodes.add_widget(chart_nodes)
        
        # Información de las barras con valores
        info_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        
        # Mostrar valores de cada heurística
        values_text = "Valores:\n"
        for name, value in nodes_data:
            values_text += f"• {name}: {value} nodos\n"
        
        values_label = Label(
            text=values_text,
            color=(0, 0, 0, 1), 
            font_size='12sp',
            text_size=(dp(400), None),
            halign='left',
            valign='top'
        )
        info_layout.add_widget(values_label)
        content_nodes.add_widget(info_layout)

        close_btn_nodes = Button(
            text='Cerrar',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        content_nodes.add_widget(close_btn_nodes)

        popup_nodes = Popup(
            title="Gráfico: Nodos Expandidos",
            content=content_nodes,
            size_hint=(0.95, 0.9)
        )
        close_btn_nodes.bind(on_press=popup_nodes.dismiss)
        popup_nodes.open()

        # --- Popup con gráfico de tiempos ---
        content_times = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # Título del gráfico
        title_times = Label(
            text="Tiempo de Ejecución por Heurística", 
            size_hint_y=None, 
            height=dp(40), 
            color=(0, 0, 0, 1), 
            font_size='18sp',
            bold=True
        )
        content_times.add_widget(title_times)
        
        # Crear el gráfico
        chart_times = BarChart(times_data, "Tiempo de Ejecución", "Segundos", 
                            size_hint_y=None, height=dp(300))
        content_times.add_widget(chart_times)
        
        # Información de las barras con valores
        info_layout_times = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        
        # Mostrar valores de cada heurística
        values_text_times = "Valores:\n"
        for name, value in times_data:
            values_text_times += f"• {name}: {value:.4f} segundos\n"
        
        values_label_times = Label(
            text=values_text_times,
            color=(0, 0, 0, 1), 
            font_size='12sp',
            text_size=(dp(400), None),
            halign='left',
            valign='top'
        )
        info_layout_times.add_widget(values_label_times)
        content_times.add_widget(info_layout_times)

        close_btn_times = Button(
            text='Cerrar',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        content_times.add_widget(close_btn_times)

        popup_times = Popup(
            title="Gráfico: Tiempo de Ejecución",
            content=content_times,
            size_hint=(0.95, 0.9)
        )
        close_btn_times.bind(on_press=popup_times.dismiss)
        popup_times.open()

    
    def start_animation(self, instance):
        if not self.solution_path or self.animating:
            return
        self.current_step = 0
        self.anim_event = Clock.schedule_interval(self._animate_step, 0.5)
        self.animating = True

    def pause_animation(self, instance):
        if self.anim_event:
            self.anim_event.cancel()
        self.animating = False

    def resume_animation(self, instance):
        if not self.solution_path or self.animating:
            return
        self.anim_event = Clock.schedule_interval(self._animate_step, 0.5)
        self.animating = True

    def _animate_step(self, dt):
        if self.current_step < len(self.solution_path):
            self.puzzle_grid.set_board(self.solution_path[self.current_step].board)
            self.current_step += 1
        else:
            if self.anim_event:
                self.anim_event.cancel()
            self.animating = False


    
    def _show_error(self, error_msg):
        self.progress_bar.value = 0
        self.status_label.text = 'Error al resolver'
        popup = ResultPopup("Error", f"Error: {error_msg}")
        popup.open()
    
    def _animate_solution(self, path):
        if len(path) <= 1:
            return
        
        def show_next_step(dt, step_index=[0]):
            if step_index[0] < len(path):
                self.puzzle_grid.set_board(path[step_index[0]].board)
                step_index[0] += 1
                if step_index[0] < len(path):
                    Clock.schedule_once(lambda dt: show_next_step(dt, step_index), 0.5)
        
        Clock.schedule_once(lambda dt: show_next_step(dt), 1.0)
    
    def reset_puzzle(self, instance):
        initial_board = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
        self.puzzle_grid.set_board(initial_board)
        self.status_label.text = 'Puzzle reiniciado'
        self.progress_bar.value = 0
    
    def randomize_puzzle(self, instance):
        # Crear una mezcla válida del puzzle
        board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        flat = [item for row in board for item in row]
        
        # Realizar movimientos aleatorios válidos
        current_state = PuzzleState(board)
        for _ in range(50):
            neighbors = current_state.get_neighbors()
            if neighbors:
                current_state = random.choice(neighbors)
        
        self.puzzle_grid.set_board(current_state.board)
        self.status_label.text = 'Puzzle mezclado'
        self.progress_bar.value = 0