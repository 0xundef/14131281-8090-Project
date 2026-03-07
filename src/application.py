import tkinter as tk
import os

class Application:
    def __init__(self, config=None):
        self.config = config or {}
        # Silencing Tkinter deprecation warning on macOS
        if os.name == 'posix':
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            
        self.root = tk.Tk()
        self.root.title("Relax Your Eyes")
        self.root.geometry("400x300")
        
        # Basic label
        label = tk.Label(self.root, text="Relax Your Eyes Application", font=("Arial", 16))
        label.pack(pady=20)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
