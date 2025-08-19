from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from puzzle.ui import PuzzleApp
from maze.ui import MazeApp

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        title = Label(text='Algoritmos de Búsqueda IA', font_size='28sp', bold=True,
                      size_hint_y=None, height='80dp', color=(0.2, 0.2, 0.8, 1))

        puzzle_btn = Button(text='8-Puzzle Solver', font_size='20sp',
                            size_hint_y=None, height='80dp', background_color=(0.2, 0.6, 1, 1))
        puzzle_btn.bind(on_press=self.go_to_puzzle)

        maze_btn = Button(text='Maze Solver', font_size='20sp',
                            size_hint_y=None, height='80dp', background_color=(0.6, 0.2, 1, 1))
        maze_btn.bind(on_press=self.go_to_maze)

        layout.add_widget(title)
        layout.add_widget(puzzle_btn)
        layout.add_widget(maze_btn)
        self.add_widget(layout)
    
    def go_to_puzzle(self, instance):
        self.manager.current = 'puzzle'

    def go_to_maze(self, instance):
        self.manager.current = 'maze'

class PuzzleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.puzzle_app = PuzzleApp()  # Crear una instancia de PuzzleApp
        self.add_widget(self.puzzle_app.build())  # Llamar al método build de PuzzleApp

class MazeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.maze_app = MazeApp()  # Crear una instancia de MazeApp
        self.add_widget(self.maze_app.build())  # Llamar al método build de MazeApp

class MainMenuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(PuzzleScreen(name='puzzle'))
        sm.add_widget(MazeScreen(name='maze'))
        return sm

if __name__ == "__main__":
    MainMenuApp().run()
