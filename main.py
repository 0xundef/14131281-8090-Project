import sys
import os

# Ensure src directory is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from application import Application
from screen_knocker import ScreenKnocker

def main():
    print("Starting Relax Your Eyes...")
    
    # Initialize components
    knocker = ScreenKnocker()
    
    # Start UI Application
    app = Application()
    app.run()

if __name__ == "__main__":
    main()
