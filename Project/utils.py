import sys, traceback
import heapq
from collections import deque
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Manejo de errores con Popup
def excepthook(exc_type, exc_value, exc_traceback):
    error_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    popup = Popup(
        title="Error en la app",
        content=Label(text=error_text, font_size="12sp"),
        size_hint=(0.95, 0.95),
        auto_dismiss=True
    )
    popup.open()

sys.excepthook = excepthook

# Estructuras de datos
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    
    def is_empty(self):
        return len(self.items) == 0

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        return self.items.popleft() if not self.is_empty() else None
    
    def is_empty(self):
        return len(self.items) == 0

class MinHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, item):
        heapq.heappush(self.heap, item)
    
    def pop(self):
        return heapq.heappop(self.heap) if self.heap else None
    
    def is_empty(self):
        return len(self.heap) == 0
