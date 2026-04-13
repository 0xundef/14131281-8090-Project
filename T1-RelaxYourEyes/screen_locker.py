import platform
import ctypes
import subprocess
from abc import ABC, abstractmethod


class ScreenLocker(ABC):
    def __init__(self, config=None, platform_name=None):
        self.config = config or {}
        self.platform = platform_name or platform.system()

    @abstractmethod
    def lock_screen(self):
        """Lock the screen for the current platform."""


class WindowsScreenLocker(ScreenLocker):
    def __init__(self, config=None):
        super().__init__(config=config, platform_name="Windows")

    def lock_screen(self):
        try:
            ctypes.windll.user32.LockWorkStation()
            print("Windows screen locked.")
        except Exception as e:
            print(f"Failed to lock Windows screen: {e}")


class MacOSScreenLocker(ScreenLocker):
    def __init__(self, config=None):
        super().__init__(config=config, platform_name="Darwin")

    def lock_screen(self):
        try:
            # Method 1: Use login framework (cleanest)
            login_framework = ctypes.CDLL("/System/Library/PrivateFrameworks/login.framework/Versions/Current/login")
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


class UnsupportedScreenLocker(ScreenLocker):
    def __init__(self, config=None, platform_name=None):
        super().__init__(config=config, platform_name=platform_name)

    def lock_screen(self):
        print(f"Lock screen not supported on {self.platform}")


def create_screen_locker(config=None, platform_name=None):
    detected_platform = platform_name or platform.system()
    if detected_platform == "Windows":
        return WindowsScreenLocker(config=config)
    if detected_platform == "Darwin":
        return MacOSScreenLocker(config=config)
    return UnsupportedScreenLocker(config=config, platform_name=detected_platform)


if __name__ == "__main__":
    locker = create_screen_locker()
    locker.lock_screen()
