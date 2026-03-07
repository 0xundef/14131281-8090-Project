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
        
        # Center the window
        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        
        # Basic label
        label = tk.Label(self.root, text="Relax Your Eyes Application", font=("Arial", 16))
        label.pack(pady=20)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
