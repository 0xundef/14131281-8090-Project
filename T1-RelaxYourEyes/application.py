import tkinter as tk
import os
import logging
import subprocess

class Application:
    def __init__(self, config=None, input_monitor=None, screen_locker=None):
        self.config = config or {}
        self.input_monitor = input_monitor
        self.screen_locker = screen_locker
        self.logger = logging.getLogger("RelaxYourEyes")
        
        # Get usage thresholds from config
        self.max_usage_seconds = self.config.get('usage_monitor', {}).get('max_continuous_usage_seconds', 1200)
        self.warning_duration = self.config.get('usage_monitor', {}).get('warning_duration_seconds', 10)
        self.lock_enabled = (self.config.get("lock_screen") or {}).get("enabled", True)

        self.root = tk.Tk()
        self.root.title("Relax Your Eyes")
        self.root.withdraw()
        
        self.is_warning = False
        self.warning_window = None

        self.check_usage()

    def show_lock_warning(self):
        """Shows a modal dialog with a countdown before locking."""
        if self.is_warning:
            return
            
        self.is_warning = True
        self.logger.warning(
            "Usage limit reached. Starting warning countdown. warning_duration_seconds=%s",
            self.warning_duration,
        )
        
        # Create modal window
        warning_window = tk.Toplevel(self.root)
        self.warning_window = warning_window
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
                subprocess.run(
                    ["osascript", "-e", 'tell application "Terminal" to activate'],
                    timeout=1.0,
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.TimeoutExpired:
                self.logger.warning("osascript activate timed out")
            except Exception as e:
                self.logger.exception("Could not force focus on macOS: %s", e)

        screen_w = warning_window.winfo_screenwidth()
        screen_h = warning_window.winfo_screenheight()
        win_w = 400
        win_h = 200
        x = max(0, int((screen_w - win_w) / 2))
        y = max(0, int((screen_h - win_h) / 3))
        warning_window.geometry(f"{win_w}x{win_h}+{x}+{y}")

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
            if not self.is_warning:
                return
            if not warning_window.winfo_exists():
                self.is_warning = False
                return
            if remaining_time > 0:
                # Re-force topmost every second just in case
                warning_window.lift()
                warning_window.attributes('-topmost', True)
                
                countdown_label.config(text=f"Locking screen in {remaining_time}s...")
                self.logger.info("lock_countdown_seconds_remaining=%s", remaining_time)
                remaining_time -= 1
                warning_window.after(1000, update_countdown)
            else:
                # Time's up
                self.is_warning = False
                try:
                    warning_window.destroy()
                finally:
                    self.warning_window = None
                    self.perform_lock()

        # Start countdown
        update_countdown()
        
        self.root.after(int(max(self.warning_duration, 0) * 1000 + 1500), self._ensure_lock_after_warning)

    def _ensure_lock_after_warning(self):
        if self.is_warning:
            self.logger.warning("Warning countdown timeout. Forcing lock attempt.")
            self.is_warning = False
            if self.warning_window is not None and self.warning_window.winfo_exists():
                try:
                    self.warning_window.destroy()
                finally:
                    self.warning_window = None
            self.perform_lock()

    def perform_lock(self):
        """Executes the lock screen action and resets usage."""
        self.logger.warning("Usage limit exceeded. Locking screen.")
        if not self.lock_enabled:
            self.logger.warning("lock_screen.enabled is false. Skipping lock.")
            return
        if self.screen_locker:
            self.screen_locker.lock_screen()
            # Reset the usage timer after locking
            # self.input_monitor.reset_usage()
        else:
            self.logger.warning("No screen_locker provided. Skipping lock.")

    def check_usage(self):
        if self.is_warning:
            self.root.after(1000, self.check_usage)
            return

        if self.input_monitor:
            duration = self.input_monitor.get_continuous_usage_duration()
            
            self.logger.info("continuous_usage_seconds=%.1f", duration)
            
            if duration > self.max_usage_seconds:
                self.show_lock_warning()
        
        self.root.after(1000, self.check_usage)

    def run(self):
        self.root.mainloop()
