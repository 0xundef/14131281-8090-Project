import sys
import os
import yaml

# Ensure src directory is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from application import Application
from screen_knocker import ScreenKnocker

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("Config file not found. Using empty config.")
        return {}
    except yaml.YAMLError as exc:
        print(f"Error parsing config file: {exc}")
        return {}

def main():
    print("Starting Relax Your Eyes...")
    
    # Load configuration
    config = load_config()
    print(f"Configuration loaded: {config.get('app_name', 'Unknown App')}")
    
    # Initialize components with config
    knocker = ScreenKnocker(config)
    
    # Start UI Application with config
    app = Application(config)
    app.run()

if __name__ == "__main__":
    main()
