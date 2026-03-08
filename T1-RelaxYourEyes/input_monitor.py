import time
from pynput import mouse, keyboard
import threading

class InputMonitor:
    def __init__(self, idle_threshold=60):
        self.idle_threshold = idle_threshold
        self.last_activity_time = time.time()
        self.usage_start_time = time.time()
        self.running = False
        
        # Listeners
        self.mouse_listener = mouse.Listener(
            on_move=self._on_activity,
            on_click=self._on_activity,
            on_scroll=self._on_activity
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_activity,
            on_release=self._on_activity
        )

    def _on_activity(self, *args):
        now = time.time()
        # If user was idle for too long, reset the session start time
        if now - self.last_activity_time > self.idle_threshold:
            # We don't print here to avoid spamming logs on first activity after break
            # But debugging might be useful. Let's keep it minimal.
            # print(f"User returned from break > {self.idle_threshold}s. Resetting usage timer.")
            self.usage_start_time = now
        
        self.last_activity_time = now

    def start(self):
        if not self.running:
            self.running = True
            # Listeners start their own threads
            self.mouse_listener.start()
            self.keyboard_listener.start()
            print("Input monitoring started.")

    def stop(self):
        if self.running:
            self.running = False
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            print("Input monitoring stopped.")

    def get_continuous_usage_duration(self):
        """
        Returns the duration of continuous usage in seconds.
        If user is currently idle (no activity for > idle_threshold), returns 0.
        """
        now = time.time()
        # If currently idle, the session is technically broken/paused
        if now - self.last_activity_time > self.idle_threshold:
            return 0
        return now - self.usage_start_time

    def reset_usage(self):
        """Resets the continuous usage timer manually."""
        print("Usage timer reset manually.")
        now = time.time()
        self.usage_start_time = now
        self.last_activity_time = now
