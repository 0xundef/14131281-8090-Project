import sys
import os
import yaml

# Add current directory to path so imports work
sys.path.append(os.path.dirname(__file__))

from application import Application
from screen_locker import ScreenLocker
from input_monitor import InputMonitor

def load_config():
    # Look for config.yaml in project root (2 levels up)
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')
    try:
        with open(config_path, 'r') as file:
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
    locker = ScreenLocker(config)
    
    # Start Input Monitor
    input_monitor = InputMonitor()
    input_monitor.start()
    
    # Start UI Application with config
    try:
        app = Application(config)
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        input_monitor.stop()

if __name__ == "__main__":
    main()
