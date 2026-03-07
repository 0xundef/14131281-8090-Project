import time
import threading
from pynput import mouse, keyboard
import platform

class InputMonitor:
    def __init__(self):
        self.last_activity_time = time.time()
        self._running = False
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Sampling for mouse move
        self.last_mouse_log_time = 0
        self.mouse_log_interval = 0.5 # Log mouse move at most every 0.5s

    def start(self):
        if self._running:
            return
        
        self._running = True
        
        # Setup listeners
        self.mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll)
        
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_press)
            
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        print(f"Input monitoring started using pynput on {platform.system()}.")

    def stop(self):
        self._running = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print("Input monitoring stopped.")

    def get_last_activity_time(self):
        return self.last_activity_time

    def _on_move(self, x, y):
        self.last_activity_time = time.time()
        now = time.time()
        if now - self.last_mouse_log_time > self.mouse_log_interval:
            print(f"Mouse moved to ({x}, {y}) [Sampled]")
            self.last_mouse_log_time = now

    def _on_click(self, x, y, button, pressed):
        self.last_activity_time = time.time()
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")

    def _on_scroll(self, x, y, dx, dy):
        self.last_activity_time = time.time()
        print(f"Mouse scrolled at ({x}, {y})")

    def _on_press(self, key): 
        self.last_activity_time = time.time()
        try:
            print(f"Keyboard event: '{key.char}' pressed")
        except AttributeError:
            print(f"Keyboard event: {key} pressed")


