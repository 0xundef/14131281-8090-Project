import platform
import os
import ctypes
import sys
import subprocess

class ScreenLocker:
    def __init__(self, config=None):
        self.platform = platform.system()
        self.config = config or {}
    
    def lock_screen(self):
        """Locks the screen based on the operating system."""
        if self.platform == "Windows":
            self._lock_windows()
        elif self.platform == "Darwin": # macOS
            self._lock_macos()
        else:
            print(f"Lock screen not supported on {self.platform}")

    def _lock_windows(self):
        try:
            ctypes.windll.user32.LockWorkStation()
            print("Windows screen locked.")
        except Exception as e:
            print(f"Failed to lock Windows screen: {e}")

    def _lock_macos(self):
        try:
            # Method 1: Use login framework (cleanest)
            login_framework = ctypes.CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
            login_framework.SACLockScreenImmediate()
            print("macOS screen locked (via login framework).")
        except OSError:
            print("Login framework not found, falling back to display sleep...")
            try:
                # Method 2: Fallback to pmset
                subprocess.run(["pmset", "displaysleepnow"], check=True)
                print("macOS display put to sleep.")
            except Exception as e:
                print(f"Failed to lock macOS screen via fallback: {e}")
        except Exception as e:
            print(f"Failed to lock macOS screen: {e}")

if __name__ == "__main__":
    locker = ScreenLocker()
    locker.lock_screen()
