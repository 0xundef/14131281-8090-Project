import sys
import os
import yaml
import logging

# Suppress Tkinter deprecation warning on macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Add current directory to path so imports work
sys.path.append(os.path.dirname(__file__))

from application import Application
from screen_locker import create_screen_locker
from input_monitor import InputMonitor

def load_config():
    current_dir = os.path.dirname(__file__)
    local_config_path = os.path.join(current_dir, "config.yaml")
    legacy_config_path = os.path.join(current_dir, "..", "config.yaml")
    config_path = local_config_path if os.path.exists(local_config_path) else legacy_config_path
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

    level_name = (config.get("logging") or {}).get("level", "INFO")
    logging.basicConfig(
        level=getattr(logging, str(level_name).upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    
    # Initialize components with config
    locker = create_screen_locker(config)
    
    # Start Input Monitor
    # Get idle threshold from config (default 60s)
    idle_threshold = config.get('usage_monitor', {}).get('idle_threshold_seconds', 60)
    input_monitor = InputMonitor(idle_threshold=idle_threshold)
    input_monitor.start()
    
    # Start UI Application with config and dependencies
    try:
        app = Application(config, input_monitor=input_monitor, screen_locker=locker)
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        input_monitor.stop()

if __name__ == "__main__":
    main()
