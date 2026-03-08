import tkinter as tk
import time

class Application:
    def __init__(self, config=None, input_monitor=None, screen_locker=None):
        self.config = config or {}
        self.input_monitor = input_monitor
        self.screen_locker = screen_locker
        
        # Get usage thresholds from config
        self.max_usage_seconds = self.config.get('usage_monitor', {}).get('max_continuous_usage_seconds', 1200)

        self.root = tk.Tk()
        self.root.title("Relax Your Eyes")
        self.root.geometry("400x250")
        
        # Main Frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # Status Label
        self.status_label = tk.Label(main_frame, text="Monitoring usage...", font=("Helvetica", 14))
        self.status_label.pack(pady=10)
        
        # Timer Label
        self.timer_label = tk.Label(main_frame, text="Continuous Usage: 0m 0s", font=("Helvetica", 18, "bold"))
        self.timer_label.pack(pady=10)
        
        # Info Label
        threshold_mins = self.max_usage_seconds // 60
        info_text = f"Limit: {threshold_mins} minutes"
        self.info_label = tk.Label(main_frame, text=info_text, font=("Helvetica", 10), fg="gray")
        self.info_label.pack(pady=5)
        
        # Reset Button (Optional, for testing)
        self.reset_btn = tk.Button(main_frame, text="Reset Timer", command=self.reset_timer)
        self.reset_btn.pack(pady=10)

        # Start checking usage
        self.check_usage()

    def reset_timer(self):
        if self.input_monitor:
            self.input_monitor.reset_usage()
            self.check_usage() # Update UI immediately

    def check_usage(self):
        if self.input_monitor:
            duration = self.input_monitor.get_continuous_usage_duration()
            
            # Update UI
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            self.timer_label.config(text=f"{minutes}m {seconds}s")
            
            # Check threshold
            if duration > self.max_usage_seconds:
                self.status_label.config(text="Usage limit exceeded! Locking...", fg="red")
                if self.screen_locker:
                    print("Max continuous usage exceeded. Locking screen.")
                    # Lock screen
                    self.screen_locker.lock_screen()
                    
                    # Reset the usage timer after locking so user can start fresh after unlocking
                    self.input_monitor.reset_usage()
            else:
                self.status_label.config(text="Monitoring usage...", fg="black")
        
        # Schedule next check in 1 second
        self.root.after(1000, self.check_usage)

    def run(self):
        self.root.mainloop()
