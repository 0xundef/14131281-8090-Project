import tkinter as tk
import time
import os

class Application:
    def __init__(self, config=None, input_monitor=None, screen_locker=None):
        self.config = config or {}
        self.input_monitor = input_monitor
        self.screen_locker = screen_locker
        
        # Get usage thresholds from config
        self.max_usage_seconds = self.config.get('usage_monitor', {}).get('max_continuous_usage_seconds', 1200)
        self.warning_duration = self.config.get('usage_monitor', {}).get('warning_duration_seconds', 10)

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

        # Flag to prevent multiple warnings
        self.is_warning = False

        # Start checking usage
        self.check_usage()

    def reset_timer(self):
        if self.input_monitor:
            self.input_monitor.reset_usage()
            self.status_label.config(text="Monitoring usage...", fg="black")
            self.check_usage() # Update UI immediately

    def show_lock_warning(self):
        """Shows a modal dialog with a countdown before locking."""
        if self.is_warning:
            return
            
        self.is_warning = True
        
        # Create modal window
        warning_window = tk.Toplevel(self.root)
        warning_window.title("Break Time!")
        warning_window.geometry("400x200")
        
        # 1. Force Topmost
        warning_window.attributes('-topmost', True) 
        
        # 2. Deiconify and Lift
        warning_window.deiconify()
        warning_window.lift()
        
        # 3. Focus Force
        warning_window.focus_force()

        # 4. macOS Specific: Force app activation
        if self.screen_locker and self.screen_locker.platform == "Darwin":
            try:
                # Use osascript to activate the application
                # This ensures the window comes to the very front even if other apps are focused
                cmd = """osascript -e 'tell application "Python" to activate'"""
                os.system(cmd)
            except Exception as e:
                print(f"Could not force focus on macOS: {e}")

        # Center the window
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        warning_window.geometry(f"+{x+50}+{y+50}")

        # Warning Labels
        tk.Label(warning_window, text="Usage Limit Reached!", font=("Helvetica", 16, "bold"), fg="red").pack(pady=15)
        tk.Label(warning_window, text="Please take a break.", font=("Helvetica", 14)).pack(pady=5)
        
        countdown_label = tk.Label(warning_window, text=f"Locking screen in {self.warning_duration}s...", font=("Helvetica", 12))
        countdown_label.pack(pady=10)
        
        # Disable close button (protocol)
        def on_close():
            pass # Ignore close attempts
        warning_window.protocol("WM_DELETE_WINDOW", on_close)
        
        # Countdown logic
        remaining_time = self.warning_duration
        
        def update_countdown():
            nonlocal remaining_time
            if remaining_time > 0:
                # Re-force topmost every second just in case
                warning_window.lift()
                warning_window.attributes('-topmost', True)
                
                countdown_label.config(text=f"Locking screen in {remaining_time}s...")
                remaining_time -= 1
                warning_window.after(1000, update_countdown)
            else:
                # Time's up
                warning_window.destroy()
                self.perform_lock()
                self.is_warning = False

        # Start countdown
        update_countdown()
        
        # Make it modal
        warning_window.transient(self.root)
        warning_window.grab_set()
        self.root.wait_window(warning_window)

    def perform_lock(self):
        """Executes the lock screen action and resets usage."""
        self.status_label.config(text="Usage limit exceeded! Locking...", fg="red")
        if self.screen_locker:
            print("Max continuous usage exceeded. Locking screen.")
            self.screen_locker.lock_screen()
            # Reset the usage timer after locking
            self.input_monitor.reset_usage()
        
        # Reset UI status
        self.status_label.config(text="Monitoring usage...", fg="black")

    def check_usage(self):
        # If we are in warning state, stop the main loop checks to avoid interference
        # The warning modal loop will handle the transition to lock
        if self.is_warning:
            # We still schedule the next check, but do nothing
            self.root.after(1000, self.check_usage)
            return

        if self.input_monitor:
            duration = self.input_monitor.get_continuous_usage_duration()
            
            # Update UI
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            self.timer_label.config(text=f"{minutes}m {seconds}s")
            
            # Check threshold
            if duration > self.max_usage_seconds:
                # Instead of locking immediately, show warning
                self.show_lock_warning()
            else:
                self.status_label.config(text="Monitoring usage...", fg="black")
        
        # Schedule next check in 1 second
        self.root.after(1000, self.check_usage)

    def run(self):
        self.root.mainloop()
